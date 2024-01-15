import 'package:flutter/material.dart';
import 'package:flutter_overlay_window/flutter_overlay_window.dart';

class MahjongOverlay extends StatefulWidget {
  @override
  State<MahjongOverlay> createState() => _MahjongOverlayState();
}

class _MahjongOverlayState extends State<MahjongOverlay> {
  List<String> logs = [];

  dynamic toDisplay;

  @override
  void initState() {
    super.initState();

    FlutterOverlayWindow.overlayListener.listen((event) {
      setState(() {
        toDisplay = event;
      });
    });
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
                onPressed: () {
                  FlutterOverlayWindow.shareData("Hello from the other side");
                },
                child: const Text('Start python'),
              ),
              Text(toDisplay ?? "Nothing to display"),
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
