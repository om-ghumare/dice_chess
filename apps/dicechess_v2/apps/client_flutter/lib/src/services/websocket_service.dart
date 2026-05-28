import 'dart:convert';

import 'package:web_socket_channel/web_socket_channel.dart';

class WsService {
  WsService();

  WebSocketChannel? _channel;
  Stream<Map<String, dynamic>>? _messages;

  void connect(String url) {
    _channel = WebSocketChannel.connect(Uri.parse(url));
    _messages = _channel!.stream.map((raw) {
      try {
        if (raw is String) {
          return jsonDecode(raw) as Map<String, dynamic>;
        }
        if (raw is Map) {
          return Map<String, dynamic>.from(raw);
        }
      } catch (e) {
        return {
          'type': 'error',
          'payload': {
            'code': 'CLIENT_PARSE_ERROR',
            'message': e.toString(),
          },
        };
      }
      return {
        'type': 'error',
        'payload': {
          'code': 'UNSUPPORTED_WS_PAYLOAD',
          'message': raw.runtimeType.toString(),
        },
      };
    });
  }

  Stream<Map<String, dynamic>> get messages {
    final stream = _messages;
    if (stream == null) {
      throw StateError('WebSocket not connected');
    }
    return stream;
  }

  void send(Map<String, dynamic> payload) {
    _channel?.sink.add(jsonEncode(payload));
  }

  void dispose() {
    _channel?.sink.close();
    _channel = null;
    _messages = null;
  }
}
