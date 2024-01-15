package com.example.realtime_mahjong_trainer;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.PixelFormat;
import android.media.Image;
import android.media.projection.MediaProjectionManager;
import android.os.Bundle;
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

public class MainActivity extends FlutterActivity {

  // For logging
  private static final String TAG = "MainActivity";

  // For calls from Flutter
  private static final String CHANNEL =
    "com.example.realtime_mahjong_trainer/stream";

  private static final int REQUEST_MEDIA_PROJECTION = 1;

  MediaProjectionManager mMediaProjectionManager;
  private ScreenStreamer streamer;
  private PyObject engine;

  @Override
  public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    Activity activity = getActivity();

    DisplayMetrics metrics = new DisplayMetrics();
    activity.getWindowManager().getDefaultDisplay().getMetrics(metrics);

    mMediaProjectionManager =
      (MediaProjectionManager) activity.getSystemService(
        Context.MEDIA_PROJECTION_SERVICE
      );

    streamer =
      new ScreenStreamer(
        metrics,
        mMediaProjectionManager,
        (Image img) -> processCapturedImage(img)
      );
  }

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
      streamer.startStream(resultCode, intent);
    }
  }

  // Effective entry point from Flutter
  private int startStream() {
    Intent serviceIntent = new Intent(this, MediaProjectionService.class);

    Log.i(TAG, "Start foreground service");
    startForegroundService(serviceIntent);

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
