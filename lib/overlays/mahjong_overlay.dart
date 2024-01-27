import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter_overlay_window/flutter_overlay_window.dart';
import 'package:realtime_mahjong_trainer/overlays/tiles_painter.dart';
import 'package:realtime_mahjong_trainer/server.dart';

parseEngineResult(List<int> b) {
  int sepIndex = b.indexOf(10); // refers to \n

  String jsonString = String.fromCharCodes(b.sublist(0, sepIndex));
  var json = jsonDecode(jsonString);

  Image image = Image.memory(Uint8List.fromList(b.sublist(sepIndex + 1)));

  return (json, image);
}

class AnalysisOverlay extends StatelessWidget {
  final dynamic analysis;
  const AnalysisOverlay(this.analysis);

  @override
  Widget build(BuildContext context) {
    int shanten = analysis['shanten'];
    String hand = analysis['hand'];
    List<dynamic> tiles = analysis['tiles'];

    double devicePixelRatio = MediaQuery.of(context).devicePixelRatio;

    return Stack(
      children: [
        LayoutBuilder(
          builder: (_, constraints) => CustomPaint(
            painter: TilesPainter(tiles, devicePixelRatio),
            size: Size(constraints.maxWidth, constraints.maxHeight),
          ),
        ),
        Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(shanten.toString()),
          ],
        ),
      ],
    );
  }
}

class MahjongOverlay extends StatefulWidget {
  @override
  State<MahjongOverlay> createState() => _MahjongOverlayState();
}

class _MahjongOverlayState extends State<MahjongOverlay> {
  List<String> logs = [];

  late Image image;
  late dynamic analysis;

  bool ready = false;

  int imageWidth = 0;
  int imageHeight = 0;

  @override
  void initState() {
    super.initState();

    Server(
      callback: (data) {
        var tup = parseEngineResult(data);
        var json = tup.$1;
        Image im = tup.$2;
        setState(() {
          image = im;
          analysis = json;
          ready = true;
        });
        im.image
            .resolve(ImageConfiguration())
            .addListener(ImageStreamListener((ImageInfo info, bool _) {
          setState(() {
            imageWidth = info.image.width;
            imageHeight = info.image.height;
            print("=====================================================IMG");
            print(imageHeight);
            print(imageWidth);
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
      double devicePixelRatio = MediaQuery.of(context).devicePixelRatio;
      print(
          "=====================================================Constrtraints");
      print(constraints.maxHeight * devicePixelRatio);
      print(constraints.maxWidth * devicePixelRatio);

      if (!ready) {
        return Text("");
      }

      return AnalysisOverlay(analysis);
      return RainbowBorder(child: AnalysisOverlay(analysis));
      return Container(
          decoration: BoxDecoration(
            border: Border.all(
              color: Colors.red,
              width: 0,
            ),
          ),
          child: Stack(
            fit: StackFit.expand,
            children: [
              AnalysisOverlay(analysis),
            ],
          ));
    });
  }
}

class RainbowBorder extends StatelessWidget {
  final Widget child;

  RainbowBorder({required this.child});

  @override
  Widget build(BuildContext context) {
      Widget boxesInBoxes = Container();

      int n = 5;
      for (int i = 0; i < n; i++) {
        boxesInBoxes = Container(
          decoration: BoxDecoration(
            border: Border.all(
              color: Colors.primaries[i],
              width: 2,
            ),
          ),
          child: boxesInBoxes,
        );
      }

    return SizedBox.expand(
      child: Stack(
        children: [
          child,
          boxesInBoxes,
        ],
      ),
    );
  }
}