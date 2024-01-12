package com.example.realtime_mahjong_trainer;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import androidx.core.app.NotificationCompat;

public class MediaProjectionService extends Service {

    // public int onStartCommand(Intent intent, int flags, int startId) {
    //     // Start the service in the foreground
    //     startForeground(1, new Notification()); // You may customize the notification
    //     // Your service logic here
    //     return START_STICKY;
    // }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        createNotificationChannel();

        Intent intent1 = new Intent(this, MainActivity.class);

        PendingIntent pendingIntent1 = PendingIntent.getActivity(this, 0, intent1,  PendingIntent.FLAG_MUTABLE);

        Notification notification1 = new NotificationCompat.Builder(this, "ScreenRecorder")
                .setContentTitle("yNote studios")
                .setContentText("Filming...")
                .setContentIntent(pendingIntent1).build();


        startForeground(1, notification1);

        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    private void createNotificationChannel() {
        NotificationChannel channel = new NotificationChannel("ScreenRecorder", "Foreground notification",
                NotificationManager.IMPORTANCE_DEFAULT);
        NotificationManager manager = getSystemService(NotificationManager.class);
        manager.createNotificationChannel(channel);
    }

    @Override
    public void onDestroy() {
        stopForeground(true);
        stopSelf();

        super.onDestroy();
    }

}
