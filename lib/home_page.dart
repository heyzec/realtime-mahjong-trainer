import 'dart:developer';

import 'dart:isolate';
import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_overlay_window/flutter_overlay_window.dart';

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

  static const platform =
      MethodChannel('com.example.realtime_mahjong_trainer/stream');

  String _python = 'Python result not ready';

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

  Future<void> recordForAWhile() async {
    try {
      print("Going to start");
      await platform.invokeMethod<int>('startStream');
      print("start");
      // await Future.delayed(Duration(seconds: 10), () async {
      //   print("going to stop");
      //   await platform.invokeMethod<int>('stopRecording');
      //   print("stop");
      // });
    } on PlatformException catch (e) {
      print(e);
    } on Exception catch (e) {
      print(e);
    }
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

    // loopRecord();
  }

  void loopRecord() async {
    while (true) {
      // await FlutterScreenRecording.startRecordScreen("video");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Mahjong"),
      ),
      body: Center(
        child: Column(
          children: [
            TextButton(
              onPressed: start,
              child: const Text("Show Overlay"),
            ),
            TextButton(
              onPressed: recordForAWhile,
              child: Text("Start Streaming"),
            ),
            TextButton(
              onPressed: () async {},
              child: Text(_python),
            ),
          ],
        ),
      ),
    );
  }
}
