import 'package:flutter/material.dart';

import '../services/app_session.dart';

class LobbyScreen extends StatefulWidget {
  const LobbyScreen({super.key});

  @override
  State<LobbyScreen> createState() => _LobbyScreenState();
}

class _LobbyScreenState extends State<LobbyScreen> {
  bool _busy = false;

  Future<void> _quickMatch() async {
    setState(() {
      _busy = true;
    });
    try {
      final token = AppSession.instance.accessToken!;
      final result = await AppSession.instance.api.enqueue(token);
      if ((result['matched'] as bool?) == true) {
        AppSession.instance.currentMatchId = result['match_id'] as String;
        if (mounted) {
          Navigator.pushNamed(context, '/match');
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Queued. Open another client and queue there too.')),
          );
        }
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
    } finally {
      if (mounted) {
        setState(() {
          _busy = false;
        });
      }
    }
  }

  Future<void> _openLatestMatch() async {
    setState(() {
      _busy = true;
    });
    try {
      final token = AppSession.instance.accessToken!;
      final matches = await AppSession.instance.api.listMatches(token);
      if (matches.isEmpty) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('No matches yet.')));
        }
        return;
      }
      final latest = matches.last as Map<String, dynamic>;
      AppSession.instance.currentMatchId = latest['match_id'] as String;
      if (mounted) {
        Navigator.pushNamed(context, '/match');
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
    } finally {
      if (mounted) {
        setState(() {
          _busy = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Lobby')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            ElevatedButton(
              onPressed: () => Navigator.pushNamed(context, '/room'),
              child: const Text('Create / Join Room Code'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: _busy ? null : _quickMatch,
              child: Text(_busy ? 'Working...' : 'Quick Matchmaking'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: _busy ? null : _openLatestMatch,
              child: const Text('Open Latest Match'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: () => Navigator.pushNamed(context, '/history'),
              child: const Text('Match History'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: () => Navigator.pushNamed(context, '/profile'),
              child: const Text('Profile'),
            ),
          ],
        ),
      ),
    );
  }
}
