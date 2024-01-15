import 'dart:io';

enum ServerState {
  empty,
  partial,
}

class Server {
  void Function(List<int>) callback;

  List<int> buffer = [];

  ServerState state = ServerState.empty;

  int remaining = 0;

  Server({
    required this.callback,
    required String host,
    required int port,
  }) {
    print("server started");
    Future<ServerSocket> serverFuture = ServerSocket.bind('0.0.0.0', 55555);
    serverFuture.then((ServerSocket server) {
      server.listen((Socket socket) {
        socket.listen((List<int> data) {
          if (state == ServerState.empty) {
            int? dataLength =
                int.tryParse(String.fromCharCodes(data.sublist(0, 8)));
            if (dataLength == null) {
              print("Invalid data length");
              return;
            }
            print("Incoming connection of $dataLength");
            data = data.sublist(8);
            remaining = dataLength;
          }
          buffer.addAll(data);
          remaining -= data.length;
          if (remaining > 0) {
            state = ServerState.partial;
          } else {
            socket.close();
            callback(buffer);
            state = ServerState.empty;
            buffer = [];
          }
        });
      });
    });
  }
}
