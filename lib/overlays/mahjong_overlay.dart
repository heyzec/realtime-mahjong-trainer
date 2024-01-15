import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter_overlay_window/flutter_overlay_window.dart';
import 'package:realtime_mahjong_trainer/server.dart';

void startServer() {
  Future<ServerSocket> serverFuture = ServerSocket.bind('0.0.0.0', 12345);
  serverFuture.then((ServerSocket server) {
    server.listen((Socket client) {
      client.listen((List<int> data) {
        String result = new String.fromCharCodes(data);
        print(result.substring(0, result.length - 1));
      });
    });
  });
}

class MahjongOverlay extends StatefulWidget {
  @override
  State<MahjongOverlay> createState() => _MahjongOverlayState();
}

class _MahjongOverlayState extends State<MahjongOverlay> {
  List<String> logs = [];

  Image? image;

  @override
  void initState() {
    super.initState();

    FlutterOverlayWindow.overlayListener.listen((event) {
      print(event);
      // setState(() {
      //   toDisplay = event;
      // });
    });

    Server(
      callback: (data) {
        print("Received data of ${data.length}");
        setState(() {
          image = Image.memory(Uint8List.fromList(data));
        });
      },
      host: "0.0.0.0",
      port: 12345,
    );
  }

  @override
  Widget build(BuildContext context) {
    print("Build overlay");
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
              image ?? Text("Nothing"),
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
