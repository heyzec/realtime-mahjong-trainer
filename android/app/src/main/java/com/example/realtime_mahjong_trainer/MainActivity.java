package com.example.realtime_mahjong_trainer;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

import androidx.fragment.app.FragmentTransaction;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Check if the fragment is already added to avoid adding it multiple times
        if (savedInstanceState == null) {
            // Start the ScreenCaptureFragment
            startScreenCaptureFragment();
        }
    }

  private void startScreenCaptureFragment() {
      Intent serviceIntent = new Intent(this, MediaProjectionService.class);

      startForegroundService(serviceIntent);

      FragmentTransaction fragmentTransaction = getSupportFragmentManager().beginTransaction();

      // Create an instance of the ScreenCaptureFragment
      ScreenCaptureFragment screenCaptureFragment = new ScreenCaptureFragment();

      // Replace the content of the container with the new fragment
      fragmentTransaction.replace(R.id.fragment_container, screenCaptureFragment);

      // Commit the transaction
      fragmentTransaction.commit();
  }
}

// import android.os.Bundle;
// import androidx.appcompat.app.AppCompatActivity;

// import androidx.fragment.app.FragmentTransaction;



// public class MainActivity extends AppCompatActivity {

//     @Override
//     protected void onCreate(Bundle savedInstanceState) {
//         super.onCreate(savedInstanceState);
//         setContentView(R.layout.activity_main);

//         // Check if the fragment is already added to avoid adding it multiple times
//         // if (savedInstanceState == null) {
//         //     // Start the ScreenCaptureFragment
//         //     startScreenCaptureFragment();
//         // }
//     }

//     private void startScreenCaptureFragment() {
//         FragmentTransaction fragmentTransaction = getSupportFragmentManager().beginTransaction();

//         // Create an instance of the ScreenCaptureFragment
//         ScreenCaptureFragment screenCaptureFragment = new ScreenCaptureFragment();

//         // Replace the content of the container with the new fragment
//         fragmentTransaction.replace(R.id.fragment_container, screenCaptureFragment);

//         // Commit the transaction
//         fragmentTransaction.commit();
//     }
// }
