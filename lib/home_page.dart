import 'dart:developer';
import 'dart:isolate';
import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_overlay_window/flutter_overlay_window.dart';
import 'package:flutter_screen_recording/flutter_screen_recording.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  static const String _kPortNameOverlay = 'OVERLAY';
  static const String _kPortNameHome = 'UI';
  final _receivePort = ReceivePort();
  SendPort? homePort;
  String? latestMessageFromOverlay;

  static const platform = MethodChannel('samples.flutter.dev/battery');

  String _batteryLevel = 'Unknown battery level.';

  @override
  void initState() {
    super.initState();
    if (homePort != null) return;
    final res = IsolateNameServer.registerPortWithName(
      _receivePort.sendPort,
      _kPortNameHome,
    );
    log("$res: OVERLAY");
    _receivePort.listen((message) {
      log("message from OVERLAY: $message");
      setState(() {
        latestMessageFromOverlay = 'Latest Message From Overlay: $message';
      });
    });
  }

  Future<void> _getBatteryLevel() async {
    String batteryLevel;
    setState(() {
      _batteryLevel = "maybe?";
    });
    try {
      final result = await platform.invokeMethod<int>('getBatteryLevel');
      batteryLevel = 'Battery level at $result % .';
    } on PlatformException catch (e) {
      batteryLevel = "Failed to get battery level: '${e.message}'.";
    }

    setState(() {
      _batteryLevel = batteryLevel;
    });
  }

  void start() async {
    if (await FlutterOverlayWindow.isActive()) return;

    await FlutterOverlayWindow.showOverlay(
      enableDrag: true,
      overlayTitle: "X-SLAYER",
      overlayContent: 'Overlay Enabled',
      flag: OverlayFlag.defaultFlag,
      visibility: NotificationVisibility.visibilityPublic,
      positionGravity: PositionGravity.auto,
      height: 500,
      width: WindowSize.matchParent,
    );

    loopRecord();
  }

  void loopRecord() async {
    while (true) {
      await FlutterScreenRecording.startRecordScreen("video");
      await Future.delayed(Duration(seconds: 10), () async {
        String path = await FlutterScreenRecording.stopRecordScreen;
        print(path);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text("Mahjong"),
        ),
        body: Center(
            child: Column(children: [
          TextButton(
            onPressed: start,
            child: const Text("Show Overlay"),
          ),
          TextButton(
            onPressed: _getBatteryLevel,
            child: Text(_batteryLevel),
          ),
        ])));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Plugin example app'),
      ),
      body: Center(
        child: Column(
          children: [
            TextButton(
              onPressed: () async {
                final status = await FlutterOverlayWindow.isPermissionGranted();
                log("Is Permission Granted: $status");
              },
              child: const Text("Check Permission"),
            ),
            const SizedBox(height: 10.0),
            TextButton(
              onPressed: () async {
                final bool? res =
                    await FlutterOverlayWindow.requestPermission();
                log("status: $res");
              },
              child: const Text("Request Permission"),
            ),
            const SizedBox(height: 10.0),
            TextButton(
              onPressed: () async {
                if (await FlutterOverlayWindow.isActive()) return;
                await FlutterOverlayWindow.showOverlay(
                  enableDrag: true,
                  overlayTitle: "X-SLAYER",
                  overlayContent: 'Overlay Enabled',
                  flag: OverlayFlag.defaultFlag,
                  visibility: NotificationVisibility.visibilityPublic,
                  positionGravity: PositionGravity.auto,
                  height: 500,
                  width: WindowSize.matchParent,
                );
              },
              child: const Text("Show Overlay"),
            ),
            const SizedBox(height: 10.0),
            TextButton(
              onPressed: () async {
                final status = await FlutterOverlayWindow.isActive();
                log("Is Active?: $status");
              },
              child: const Text("Is Active?"),
            ),
            const SizedBox(height: 10.0),
            TextButton(
              onPressed: () async {
                await FlutterOverlayWindow.shareData('update');
              },
              child: const Text("Update Overlay"),
            ),
            const SizedBox(height: 10.0),
            TextButton(
              onPressed: () {
                log('Try to close');
                FlutterOverlayWindow.closeOverlay()
                    .then((value) => log('STOPPED: alue: $value'));
              },
              child: const Text("Close Overlay"),
            ),
            const SizedBox(height: 20.0),
            TextButton(
              onPressed: () {
                homePort ??=
                    IsolateNameServer.lookupPortByName(_kPortNameOverlay);
                homePort?.send('Send to overlay: ${DateTime.now()}');
              },
              child: const Text("Send message to overlay"),
            ),
            const SizedBox(height: 20),
            Text(latestMessageFromOverlay ?? ''),
          ],
        ),
      ),
    );
  }
}
