package com.example.realtime_mahjong_trainer;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.PixelFormat;
import android.hardware.display.DisplayManager;
import android.hardware.display.VirtualDisplay;
import android.media.Image;
import android.media.ImageReader;
import android.media.projection.MediaProjection;
import android.media.projection.MediaProjectionManager;
import android.os.Bundle;
import android.os.StrictMode;
import android.util.DisplayMetrics;
import androidx.annotation.NonNull;
import com.chaquo.python.PyException;
import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import io.flutter.Log;
import io.flutter.embedding.android.FlutterActivity;
import io.flutter.embedding.engine.FlutterEngine;
import io.flutter.plugin.common.MethodChannel;
import java.io.BufferedOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.Socket;
import java.net.URL;
import java.time.Instant;
import java.util.Arrays;
import java.util.concurrent.Semaphore;

public class MainActivity extends FlutterActivity {

  // For logging
  private static final String TAG = "MainActivity";

  // For calls from Flutter
  private static final String CHANNEL =
    "com.example.realtime_mahjong_trainer/stream";

  private static final int REQUEST_MEDIA_PROJECTION = 1;

  // Objects required for capturing screen
  private DisplayMetrics metrics;
  private MediaProjectionManager mMediaProjectionManager;
  private MediaProjection mMediaProjection;

  // Results to be passed around from onActivityResult
  private int mResultCode;
  private Intent mResultData;

  private Semaphore semaphore = new Semaphore(1);

  private PyObject engine;

  @Override
  public void configureFlutterEngine(@NonNull FlutterEngine flutterEngine) {
    super.configureFlutterEngine(flutterEngine);

    new MethodChannel(
      flutterEngine.getDartExecutor().getBinaryMessenger(),
      CHANNEL
    )
      .setMethodCallHandler((call, result) -> {
        // This method is invoked on the main thread.
        if (call.method.equals("startStream")) {
          result.success(startStream());
          return;
        }
        if (call.method.equals("startPython")) {
          result.success(startPython());
          return;
        }

        result.notImplemented();
      });
  }

  @Override
  public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    Activity activity = getActivity();

    metrics = new DisplayMetrics();
    activity.getWindowManager().getDefaultDisplay().getMetrics(metrics);

    mMediaProjectionManager =
      (MediaProjectionManager) activity.getSystemService(
        Context.MEDIA_PROJECTION_SERVICE
      );
  }

  @Override
  public void onActivityResult(int requestCode, int resultCode, Intent intent) {
    Log.i(
      TAG,
      String.format(
        "onActivityResult: requestCode %d, resultCode %d, intent %s",
        requestCode,
        resultCode,
        intent.toString()
      )
    );

    if (requestCode == REQUEST_MEDIA_PROJECTION) {
      mResultCode = resultCode;
      mResultData = intent;
      startStreamPart2();
    }
  }

  // Effective entry point from Flutter
  private int startStream() {
    Intent serviceIntent = new Intent(this, MediaProjectionService.class);

    Log.i(TAG, "Start foreground service");
    startForegroundService(serviceIntent);

    MediaProjectionManager mMediaProjectionManager = (MediaProjectionManager) getActivity()
      .getSystemService(Context.MEDIA_PROJECTION_SERVICE);

    Log.i(TAG, "Requesting confirmation");
    // This initiates a prompt dialog for the user to confirm screen projection.
    // Looks like this is the legacy approach, the recommended one is
    // https://developer.android.com/guide/topics/large-screens/media-projection
    startActivityForResult(
      mMediaProjectionManager.createScreenCaptureIntent(),
      REQUEST_MEDIA_PROJECTION
    );

    return 0;
  }

  // Called upon getting confirmation from user
  private void startStreamPart2() {
    Log.i(TAG, "Starting screen capture");
    setUpMediaProjection();
    setUpVirtualDisplay();
  }

  private void setUpMediaProjection() {
    Log.i(TAG, "setting up media projection");
    mMediaProjection =
      mMediaProjectionManager.getMediaProjection(mResultCode, mResultData);
    Assert.assertNotNull(mMediaProjection);
  }

  private void setUpVirtualDisplay() {
    int width = metrics.widthPixels;
    int height = metrics.heightPixels;
    int density = metrics.densityDpi;

    Log.i(
      TAG,
      "Setting up a VirtualDisplay: " +
      width +
      "x" +
      height +
      " (" +
      density +
      ")"
    );
    ImageReader imageReader = ImageReader.newInstance(
      width,
      height,
      PixelFormat.RGBA_8888,
      // Consider making this 1, then no semaphore needed (?)
      2
    );

    imageReader.setOnImageAvailableListener(
      (ImageReader reader) -> {
        new Thread(() -> {
          final String TIME = Instant.now().toString();

          Log.i(TAG + TIME, "Image available");

          semaphore.acquireUninterruptibly();

          Image image = reader.acquireLatestImage();
          if (image == null) {
            Log.i(TAG + TIME, "Image is null");
            semaphore.release();
            return;
          }
          try {
            processCapturedImage(image);
          } catch (Exception e) {
            e.printStackTrace();
          } finally {
            Log.i(TAG + TIME, "Releasing semaphore");
            image.close(); // Release resources
            semaphore.release();
          }
        })
          .start();
      },
      null
    );

    VirtualDisplay mVirtualDisplay = mMediaProjection.createVirtualDisplay(
      "ScreenCapture",
      width,
      height,
      density,
      DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,
      imageReader.getSurface(),
      null,
      null
    );
  }

  void processCapturedImage(Image image) {
    Log.i(TAG, "We got a new image!");
    byte[] encoded = ImageEncoder.encodeImageToByteArray(image);
    Log.i(TAG, String.format("Length of encoded: %d", encoded.length));

    Python python = Python.getInstance();
    PyObject bytes = python.getModule("numpy").callAttr("array", encoded);
    engine.callAttr("process", bytes);

    return;
  }

  int startPython() {
    if (Python.isStarted()) {
      return 1;
    }
    Python.start(new AndroidPlatform(getContext()));
    Python python = Python.getInstance();
    try {
      engine = python.getModule("engine").get("Engine").callThrows();
    } catch (Throwable e) {
      Log.i(TAG, e.toString());
      return 2;
    }
    Log.i(TAG, "started Python");

    return 0;
  }
}
