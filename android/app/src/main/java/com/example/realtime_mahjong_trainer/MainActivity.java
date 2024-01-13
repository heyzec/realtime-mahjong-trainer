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
import java.util.Arrays;

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

        result.notImplemented();
      });
  }

  @Override
  public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    Activity activity = getActivity();

    // Bypass android.os.NetworkOnMainThreadException
    StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder()
      .permitAll()
      .build();
    StrictMode.setThreadPolicy(policy);

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
      2
    );

    imageReader.setOnImageAvailableListener(
      new ImageReader.OnImageAvailableListener() {
        @Override
        public void onImageAvailable(ImageReader reader) {
          Image image = reader.acquireLatestImage();
          if (image != null) {
            processCapturedImage(image);
            image.close(); // Release resources
          }
        }
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
    ImageEncoder encoder = new ImageEncoder();
    String encoded = encoder.encodeImageToBase64(image);

    Log.i(TAG, String.format("Length of encoded: %d", encoded.length()));

    // try {
    //   Socket socket = new Socket("192.168.1.1", 12345);
    //   // Request data
    //   DataOutputStream outputStream = new DataOutputStream(
    //     socket.getOutputStream()
    //   );

    //   outputStream.writeUTF(encoded);
    // } catch (IOException e) {
    //   String stackTrace = Log.getStackTraceString(e);
    //   Log.e(TAG, stackTrace);
    // }

    HttpURLConnection urlConnection;
    try {
      URL url = new URL("http://192.168.1.1:12345");
      urlConnection = (HttpURLConnection) url.openConnection();
    } catch (Exception e) {
      Log.e(TAG, Log.getStackTraceString(e));
      return;
    }

    try {
      urlConnection.setDoOutput(true);
      urlConnection.setChunkedStreamingMode(0);

      OutputStream out = new BufferedOutputStream(
        urlConnection.getOutputStream()
      );

      byte[] bytes = encoded.getBytes();

      byte[] slice = Arrays.copyOfRange(bytes, 0, 10);
      Log.i(TAG, "First 10: " + new String(slice, "UTF-8"));

      slice = Arrays.copyOfRange(bytes, bytes.length - 10, bytes.length);
      Log.i(TAG, "Last 10: " + new String(slice, "UTF-8"));

      out.write(encoded.getBytes());
      out.flush();
    } catch (Exception e) {
      Log.e(TAG, Log.getStackTraceString(e));
      return;
    } finally {
      urlConnection.disconnect();
    }
  }
}
