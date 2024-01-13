package com.example.realtime_mahjong_trainer;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.media.Image;
import android.util.Base64;
import io.flutter.Log;
import java.io.ByteArrayOutputStream;
import java.io.ByteArrayOutputStream;
import java.nio.ByteBuffer;

public class ImageEncoder {

  private static final String TAG = "ImageEncoder";

  public static String encodeImageToBase64(Image image) {
    // Convert Image to Bitmap
    // Convert Bitmap to byte array (JPEG encoding)
    Bitmap bitmap = imageToBitmap(image);

    byte[] bytes = bitmapToByteArray(bitmap);

    Log.i(TAG, String.format("Byte array length: %d", bytes.length));

    // Convert byte array to Base64
    String s = Base64.encodeToString(bytes, Base64.DEFAULT);
    Log.i(TAG, String.format("Base64: %d", s.length()));
    return s;
  }

  private static Bitmap imageToBitmap(Image image) {
    int width = image.getWidth();
    int height = image.getHeight();

    // https://binwaheed.blogspot.com/2015/03/how-to-correctly-take-screenshot-using.html
    final Image.Plane[] planes = image.getPlanes();
    final ByteBuffer buffer = planes[0].getBuffer();
    int pixelStride = planes[0].getPixelStride();
    int rowStride = planes[0].getRowStride();
    int rowPadding = rowStride - pixelStride * width;
    // create bitmap
    Bitmap bmp = Bitmap.createBitmap(
      width + rowPadding / pixelStride,
      height,
      Bitmap.Config.RGB_565
    );
    bmp.copyPixelsFromBuffer(buffer);
    image.close();

    return bmp;
  }

  private static byte[] bitmapToByteArray(Bitmap bitmap) {
    ByteArrayOutputStream stream = new ByteArrayOutputStream();
    Assert.assertNotNull(bitmap);
    bitmap.compress(Bitmap.CompressFormat.JPEG, 80, stream);
    return stream.toByteArray();
  }
}
