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

  late Image image;

  bool ready = false;

  int imageWidth = 0;
  int imageHeight = 0;

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
          ready = true;
        });
        image.image
            .resolve(ImageConfiguration())
            .addListener(ImageStreamListener((ImageInfo info, bool _) {
          setState(() {
            imageWidth = info.image.width;
            imageHeight = info.image.height;
          });
        }));
      },
      host: "0.0.0.0",
      port: 12345,
    );
  }

  @override
  Widget build(BuildContext context) {
    print("Build overlay");

    return LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
      return Container(
        decoration: BoxDecoration(
          border: Border.all(
            color: Colors.red, //                   <--- border color
            width: 1,
          ),
        ),
        child: FittedBox(
          fit: BoxFit.fill,
          // child:

          //     // width: constraints.maxWidth,
          //     // height: constraints.maxHeight,
          //     !ready ? Text("No image") : image
          // child: Stack(
          //   fit: StackFit.expand,
          //   children: [
          //     !ready
          //         ? Text("No image")
          //         : SizedBox(
          //             width: constraints.maxWidth,
          //             height: constraints.maxHeight,
          //             child: image,
          //           ),
          //     Center(
          //       child: Column(
          //         mainAxisSize: MainAxisSize.min,
          //         children: [
          //           Text(ready.toString()),
          //           Text("Image: $imageHeight x $imageWidth"),
          //           Text(
          //               "Box: ${constraints.maxHeight} x ${constraints.maxWidth}"),
          //         ],
          //       ),
          //     ),
          //   ],
          // ),
        ),
      );
    });
  }
}
