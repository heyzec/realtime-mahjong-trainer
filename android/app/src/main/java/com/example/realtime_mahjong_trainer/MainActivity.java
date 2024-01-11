package com.example.realtime_mahjong_trainer;

import androidx.annotation.NonNull;
import io.flutter.embedding.android.FlutterActivity;
import io.flutter.embedding.engine.FlutterEngine;
import io.flutter.plugins.GeneratedPluginRegistrant;

import io.flutter.plugin.common.MethodChannel;
import java.io.IOException;

import android.media.MediaRecorder;


public class MainActivity extends FlutterActivity {
  private static final String CHANNEL = "samples.flutter.dev/battery";

  private MediaRecorder mMediaRecorder;

  @Override
  public void configureFlutterEngine(@NonNull FlutterEngine flutterEngine) {
  super.configureFlutterEngine(flutterEngine);
    new MethodChannel(flutterEngine.getDartExecutor().getBinaryMessenger(), CHANNEL)
        .setMethodCallHandler(
          (call, result) -> {
            // This method is invoked on the main thread.
            if (call.method.equals("startRecording")) {
              int batteryLevel = startRecording();
            } else if (call.method.equals("stopRecording")) {
              System.out.println("ok we stop");
              stopRecording();
            } else {
              result.notImplemented();
            }
          }
        );
  }

  private int startRecording() {

    try {


      mMediaRecorder = new MediaRecorder();

      mMediaRecorder.setVideoSource(MediaRecorder.VideoSource.SURFACE);
      mMediaRecorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);

      String localFilePath = getContext().getExternalCacheDir().getAbsolutePath() + "/video.mp4";
      System.out.println(localFilePath);
      mMediaRecorder.setOutputFile(localFilePath);

      mMediaRecorder.setVideoSize(720, 1200);
      // mMediaRecorder.setVideoEncoder(MediaRecorder.VideoEncoder.MPEG_4_SP);
      mMediaRecorder.setVideoEncoder(MediaRecorder.VideoEncoder.H264);
      mMediaRecorder.setVideoFrameRate(30);
      mMediaRecorder.prepare();

      mMediaRecorder.start();

    } catch (IOException e) {
      System.out.println(e.toString());
    }
    return 0;
  }

  private int stopRecording() {
    mMediaRecorder.stop();
    return 0;
  }


}