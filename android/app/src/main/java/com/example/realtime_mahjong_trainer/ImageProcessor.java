package com.example.realtime_mahjong_trainer;


import android.media.Image;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Timer;
import java.util.TimerTask;
import com.chaquo.python.PyObject;
import java.util.Arrays;
import java.util.function.Supplier;

public class ImageProcessor {
    private static final String TAG = "ImageProcessor" ;
    ArrayList<Image> images = new ArrayList<>();
    private PyObject engine;

    private NetworkClient client = new NetworkClient("127.0.0.1", 55555);
    private NetworkClient debugClient = new NetworkClient("192.168.1.1", 55555);

    private Supplier<Image> callback;

    public ImageProcessor(PyObject engine, Supplier<Image> callback) {
        this.engine = engine;
        this.callback = callback;
    }

    public void addImage(Image image) {
        TimedLog.i(TAG, "Added new image");
        images.add(image);
    }

    public void start() {
        Timer timer = new Timer();

        timer.schedule( new TimerTask() {
            public void run() {
                Image image = callback.get();
                if (image == null) {
                    return;
                }
                processCapturedImage(image);
            }
        }, 0, 500);


    }

    public void processCapturedImage(Image image) {
        TimedLog.i(TAG, "Got a new image, encoding...");
        byte[] encoded = ImageEncoder.encodeImageToByteArray(image);
        image.close();
        TimedLog.i(TAG, String.format("Length of encoded: %d, begin python processing...", encoded.length));

        byte[] bytes;
        PyObject engineResult = engine.callAttr("process_bytes", encoded);
        TimedLog.i(TAG, String.format("Done python processing"));

        bytes = engineResult.callAttr("to_bytes").toJava(byte[].class);
        TimedLog.i(TAG, "Sending bytes to localhost:" + bytes.length);
        client.send(bytes);

        bytes = engineResult.callAttr("dumps").toJava(byte[].class);
//        bytes = Arrays.copyOfRange(bytes, 0, 1000);
        TimedLog.i(TAG, "Sending bytes to debug server:" + bytes.length);
        debugClient.send(bytes);

        return;
    }
}
