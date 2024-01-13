package com.example.realtime_mahjong_trainer;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.hardware.HardwareBuffer;
import android.media.Image;
import android.util.Base64;
import io.flutter.Log;
import java.io.ByteArrayOutputStream;
import java.io.ByteArrayOutputStream;
import java.nio.ByteBuffer;

public class ImageEncoder {

  private static final String TAG = "ImageEncoder";

  public static String encodeImageToBase64(Image image) {
    Bitmap bitmap = imageToBitmap(image);
    byte[] bytes = bitmapToByteArray(bitmap);
    return Base64.encodeToString(bytes, Base64.DEFAULT);
  }

  private static Bitmap imageToBitmap(Image image) {
    int width = image.getWidth();
    int height = image.getHeight();

    Log.i(TAG, String.format("Format: %s", image.getFormat()));
    // This class is hardcoded to only able to accept this format.
    if (image.getFormat() != HardwareBuffer.RGBA_8888) {
      return null;
    }

    Image.Plane[] planes = image.getPlanes();
    ByteBuffer buffer = planes[0].getBuffer();
    int pixelStride = planes[0].getPixelStride();
    int rowStride = planes[0].getRowStride();
    int rowPadding = rowStride - pixelStride * width;
    Bitmap bitmap = Bitmap.createBitmap(
      width + rowPadding / pixelStride,
      height,
      Bitmap.Config.ARGB_8888
    );
    bitmap.copyPixelsFromBuffer(buffer);
    return bitmap;
  }

  private static byte[] bitmapToByteArray(Bitmap bitmap) {
    ByteArrayOutputStream stream = new ByteArrayOutputStream();
    Assert.assertNotNull(bitmap);
    bitmap.compress(Bitmap.CompressFormat.JPEG, 50, stream);
    return stream.toByteArray();
  }
}
