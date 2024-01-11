import 'package:flutter/material.dart';
import 'package:flutter_overlay_window/flutter_overlay_window.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class MahjongOverlay extends StatefulWidget {
  @override
  State<MahjongOverlay> createState() => _MahjongOverlayState();
}

class _MahjongOverlayState extends State<MahjongOverlay> {
  List<String> logs = [];
  static const platform = MethodChannel('samples.flutter.dev/battery');

  String _batteryLevel = 'Unknown battery level.';

  Future<void> _getBatteryLevel() async {
    try {
      final result = await platform.invokeMethod<int>('startRecording');
    } on PlatformException catch (e) {}
  }

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: Center(
        child: Container(
          color: Colors.blue,
          height: 200,
          width: 200,
          child: Stack(
            children: [
              ElevatedButton(
                onPressed: _getBatteryLevel,
                child: const Text('Get Battery Level'),
              ),
              Text(_batteryLevel),
              Positioned(
                top: 0,
                right: 0,
                child: IconButton(
                  onPressed: () async {
                    await FlutterOverlayWindow.closeOverlay();
                  },
                  icon: const Icon(
                    Icons.close,
                    color: Colors.black,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
