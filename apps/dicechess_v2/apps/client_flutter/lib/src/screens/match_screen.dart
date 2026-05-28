import 'package:flutter/material.dart';

import '../services/app_session.dart';
import '../services/websocket_service.dart';

class MatchScreen extends StatefulWidget {
  const MatchScreen({super.key});

  @override
  State<MatchScreen> createState() => _MatchScreenState();
}

class _MatchScreenState extends State<MatchScreen> {
  final WsService _ws = WsService();
  final Map<String, String> _board = {};

  String _turn = 'white';
  String _dice = '--';
  String _status = 'Connecting...';
  String? _selectedSquare;
  bool _connected = false;
  bool _connecting = false;

  @override
  void initState() {
    super.initState();
    _boot();
  }

  @override
  void dispose() {
    _ws.dispose();
    super.dispose();
  }

  Future<void> _boot() async {
    if (_connecting) return;
    _connecting = true;
    try {
      await _ensureSessionAndMatch();
      await _connectWs();
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _status = 'Init error: $e';
        _connected = false;
      });
    } finally {
      _connecting = false;
    }
  }

  Future<void> _ensureSessionAndMatch() async {
    if (AppSession.instance.accessToken == null) {
      final auth = await AppSession.instance.api.guestAuth();
      AppSession.instance.accessToken = auth['access_token'] as String;
      AppSession.instance.userId = auth['user_id'] as String;
    }
    final token = AppSession.instance.accessToken!;
    if (AppSession.instance.currentMatchId == null) {
      final match = await AppSession.instance.api.createLocalMatch(token);
      AppSession.instance.currentMatchId = match['match_id'] as String;
    }
    final matchId = AppSession.instance.currentMatchId!;
    final match = await AppSession.instance.api.getMatch(token, matchId);
    final state = (match['state'] as Map).cast<String, dynamic>();
    _applySerializedState(state);
  }

  Future<void> _connectWs() async {
    final token = AppSession.instance.accessToken!;
    final matchId = AppSession.instance.currentMatchId!;
    final wsUrl = '${AppSession.wsBaseUrl}/ws/match/$matchId?token=$token';
    _ws.dispose();
    _ws.connect(wsUrl);
    _ws.messages.listen(
      (event) {
        final type = event['type'] as String? ?? '';
        final payload = (event['payload'] as Map?)?.cast<String, dynamic>() ?? {};
        _onEvent(type, payload);
      },
      onError: (err) {
        if (!mounted) return;
        setState(() {
          _status = 'WS error: $err';
          _connected = false;
        });
      },
      onDone: () {
        if (!mounted) return;
        setState(() {
          _status = 'Disconnected';
          _connected = false;
        });
      },
    );
    if (mounted) {
      setState(() {
        _connected = true;
      });
    }
  }

  void _applySerializedState(Map<String, dynamic> state) {
    final turn = (state['turn'] as Map?)?.cast<String, dynamic>() ?? {};
    final boardItems = (state['board'] as List?) ?? [];
    final nextBoard = <String, String>{};
    for (final item in boardItems) {
      final p = (item as Map).cast<String, dynamic>();
      final x = p['x'];
      final y = p['y'];
      nextBoard['$x,$y'] = _pieceGlyph(
        p['kind'] as String? ?? 'pawn',
        p['color'] as String? ?? 'white',
      );
    }
    setState(() {
      _board
        ..clear()
        ..addAll(nextBoard);
      _turn = turn['active_color'] as String? ?? 'white';
      _dice = turn['rolled_piece_type'] as String? ?? '--';
    });
  }

  Future<void> _recoverLocalMatchAndReconnect() async {
    try {
      final token = AppSession.instance.accessToken!;
      final match = await AppSession.instance.api.createLocalMatch(token);
      AppSession.instance.currentMatchId = match['match_id'] as String;
      await _ensureSessionAndMatch();
      await _connectWs();
      if (!mounted) return;
      setState(() {
        _status = 'Recovered with new local match';
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _status = 'Recovery failed: $e';
      });
    }
  }

  void _onEvent(String type, Map<String, dynamic> payload) {
    if (!mounted) return;
    if (type == 'match.state') {
      final state = (payload['state'] as Map?)?.cast<String, dynamic>() ?? {};
      _applySerializedState(state);
      setState(() {
        _status = 'Connected';
      });
      return;
    }
    if (type == 'match.roll_result') {
      setState(() {
        _dice = payload['piece_type'] as String? ?? _dice;
      });
      return;
    }
    if (type == 'match.end') {
      setState(() {
        _status = 'Game Over: ${payload['reason']} (${payload['result']})';
      });
      return;
    }
    if (type == 'error') {
      final code = payload['code'] as String? ?? 'UNKNOWN';
      setState(() {
        _status = 'Error: $code';
      });
      if (code == 'UNAUTHORIZED' || code == 'MATCH_NOT_FOUND' || code == 'FORBIDDEN') {
        _recoverLocalMatchAndReconnect();
      }
    }
  }

  String _pieceGlyph(String kind, String color) {
    const white = {
      'king': 'K',
      'queen': 'Q',
      'rook': 'R',
      'bishop': 'B',
      'knight': 'N',
      'pawn': 'P',
    };
    const black = {
      'king': 'k',
      'queen': 'q',
      'rook': 'r',
      'bishop': 'b',
      'knight': 'n',
      'pawn': 'p',
    };
    return (color == 'white' ? white : black)[kind] ?? '?';
  }

  void _onTapSquare(int x, int y) {
    final key = '$x,$y';
    if (_selectedSquare == null) {
      setState(() {
        _selectedSquare = key;
      });
      return;
    }
    final parts = _selectedSquare!.split(',');
    final src = [int.parse(parts[0]), int.parse(parts[1])];
    final dst = [x, y];
    _ws.send({
      'type': 'match.move_submit',
      'payload': {'from': src, 'to': dst, 'promotion': null},
    });
    setState(() {
      _selectedSquare = null;
    });
  }

  void _rollDice() {
    _ws.send({'type': 'match.roll_request', 'payload': {}});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Match')),
      body: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Turn: $_turn'),
                Text('Dice: $_dice'),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(_status),
                Text(_connected ? 'online' : 'offline'),
              ],
            ),
          ),
          const SizedBox(height: 8),
          Expanded(
            child: AspectRatio(
              aspectRatio: 1,
              child: GridView.builder(
                physics: const NeverScrollableScrollPhysics(),
                itemCount: 64,
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 8),
                itemBuilder: (context, index) {
                  final x = index % 8;
                  final y = index ~/ 8;
                  final isDark = (x + y).isEven;
                  final key = '$x,$y';
                  final piece = _board[key] ?? '';
                  final selected = _selectedSquare == key;
                  return GestureDetector(
                    onTap: () => _onTapSquare(x, y),
                    child: Container(
                      decoration: BoxDecoration(
                        color: isDark ? const Color(0xFF475569) : const Color(0xFFE2E8F0),
                        border: Border.all(color: selected ? Colors.yellow : Colors.black12, width: selected ? 3 : 1),
                      ),
                      child: Center(
                        child: Text(
                          piece,
                          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: _rollDice,
                    child: const Text('Roll Dice'),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
