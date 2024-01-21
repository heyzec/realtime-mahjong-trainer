import 'package:flutter/material.dart';

class TilesPainter extends CustomPainter {
  List<dynamic> tiles;
  double devicePixelRatio;

  TilesPainter(this.tiles, this.devicePixelRatio);

  @override
  void paint(Canvas canvas, Size size) {
    Paint paint = Paint()
      ..color = Colors.blue.withAlpha(50)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.5;

    for (var tile in tiles) {
      var rect = tile[0];
      var tileName = tile[1];
      double x = rect[0] / devicePixelRatio;
      double y = rect[1] / devicePixelRatio;
      double w = rect[2] / devicePixelRatio;
      double h = rect[3] / devicePixelRatio;
      canvas.drawRect(Rect.fromLTWH(x, y, w, h), paint);
      TextSpan span =
          TextSpan(style: TextStyle(color: Colors.red[600]), text: tileName);
      TextPainter tp = TextPainter(
          text: span,
          textAlign: TextAlign.left,
          textDirection: TextDirection.ltr);
      tp.layout();
      tp.paint(canvas, Offset(x, y - 40));
    }
  }

  @override
  bool shouldRepaint(covariant TilesPainter oldPainter) {
    return true;
  }
}