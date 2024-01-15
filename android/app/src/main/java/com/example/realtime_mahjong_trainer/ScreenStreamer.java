package com.example.realtime_mahjong_trainer;

import android.content.Intent;
import android.graphics.PixelFormat;
import android.hardware.display.DisplayManager;
import android.hardware.display.VirtualDisplay;
import android.media.Image;
import android.media.ImageReader;
import android.media.projection.MediaProjection;
import android.media.projection.MediaProjectionManager;
import android.util.DisplayMetrics;
import androidx.core.util.Consumer;
import com.example.realtime_mahjong_trainer.Assert;
import io.flutter.Log;
import java.time.Instant;
import java.util.concurrent.Semaphore;

public class ScreenStreamer {

  private static final String TAG = "ScreenStreamer";

  private DisplayMetrics metrics;
  private MediaProjectionManager mMediaProjectionManager;
  private MediaProjection mMediaProjection;

  private Consumer<Image> callback;

  private Semaphore semaphore;

  private static int MAX_RATE = 5000;

  private Instant previous;

  public ScreenStreamer(
    DisplayMetrics metrics,
    MediaProjectionManager mMediaProjectionManager,
    Consumer<Image> callback
  ) {
    this.metrics = metrics;
    this.mMediaProjectionManager = mMediaProjectionManager;
    this.callback = callback;
    this.semaphore = new Semaphore(1);
  }

  public void startStream(int mResultCode, Intent mResultData) {
    mMediaProjection =
      mMediaProjectionManager.getMediaProjection(mResultCode, mResultData);
    Assert.assertNotNull(mMediaProjection);
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
            if (previous != null) {
              long delta =
                Instant.now().toEpochMilli() - previous.toEpochMilli();
              Log.i(TAG + TIME, "" + delta);
              if (delta < MAX_RATE) {
                Log.i(TAG + TIME, "Sleep for" + delta);
                Thread.sleep(delta);
              }
            }
            this.callback.accept(image);
            previous = Instant.now();
          } catch (Exception e) {
            Log.i(TAG + TIME, "Exception occured" + e.toString());
            e.printStackTrace();
          } finally {
            // Log.i(TAG + TIME, "Releasing semaphore");
            image.close(); // Release resources
            semaphore.release();
          }
        })
          .start();
      },
      null
    );

    mMediaProjection.createVirtualDisplay(
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
}
