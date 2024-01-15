import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_overlay_window/flutter_overlay_window.dart';
import 'package:realtime_mahjong_trainer/channel.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String? latestMessageFromOverlay;

  static const channel = MethodChannel(CHANNEL_NAME);

  String _python = 'Python result not ready';

  @override
  void initState() {
    super.initState();

    channel.setMethodCallHandler((MethodCall call) async {
      if (call.method == 'deliverAnalysis') {
        // Note: It is only possible to shareData from main to overlay with thi
        await FlutterOverlayWindow.shareData(call.arguments);
        return 0;
      }
      return null;
    });
  }

  Future<void> recordForAWhile() async {
    try {
      await channel.invokeMethod<int>('startStream');
    } on Exception catch (e) {
      print(e);
    }
  }

  void start() async {
    if (await FlutterOverlayWindow.isActive()) {
      print("Overlay already open.");
      return;
    }
    if (await FlutterOverlayWindow.isPermissionGranted() != true) {
      if (await FlutterOverlayWindow.requestPermission() != true) {
        print("Permission not granted");
        return;
      }
    }

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
              onPressed: () async {
                await channel.invokeMethod('startPython');
                // var result = await Chaquopy.executeCode("print('hello world')");
                // print(result);
              },
              child: Text(_python),
            ),
          ],
        ),
      ),
    );
  }
}
