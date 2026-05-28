import 'package:flutter/material.dart';

import '../services/app_session.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool _busy = false;
  String? _errorText;

  Future<void> _ensureAuth() async {
    if (AppSession.instance.accessToken != null) {
      return;
    }
    setState(() {
      _busy = true;
      _errorText = null;
    });
    try {
      final auth = await AppSession.instance.api.guestAuth();
      AppSession.instance.accessToken = auth['access_token'] as String;
      AppSession.instance.userId = auth['user_id'] as String;
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
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF0F172A), Color(0xFF1D4ED8), Color(0xFF0EA5E9)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: SafeArea(
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 520),
              child: Card(
                elevation: 18,
                color: Colors.white.withValues(alpha: 0.9),
                margin: const EdgeInsets.all(24),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 32),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Text(
                        'Dice Chess',
                        style: TextStyle(
                          fontSize: 38,
                          fontWeight: FontWeight.w800,
                          color: Color(0xFF0F172A),
                          letterSpacing: -1,
                        ),
                      ),
                      const SizedBox(height: 8),
                      const Text(
                        'Play tactical chess with dice-based turns.',
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 16, color: Color(0xFF334155)),
                      ),
                      const SizedBox(height: 28),
                      SizedBox(
                        width: double.infinity,
                        child: FilledButton.icon(
                          style: FilledButton.styleFrom(
                            backgroundColor: const Color(0xFF1D4ED8),
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                          ),
                          onPressed: _busy
                              ? null
                              : () async {
                                  try {
                                    await _ensureAuth();
                                    if (mounted) {
                                      Navigator.pushNamed(context, '/lobby');
                                    }
                                  } catch (e) {
                                    if (!mounted) return;
                                    setState(() {
                                      _errorText = e.toString();
                                    });
                                  }
                                },
                          icon: const Icon(Icons.groups_rounded),
                          label: Text(_busy ? 'Connecting...' : 'Enter Lobby'),
                        ),
                      ),
                      const SizedBox(height: 12),
                      SizedBox(
                        width: double.infinity,
                        child: OutlinedButton.icon(
                          style: OutlinedButton.styleFrom(
                            foregroundColor: const Color(0xFF0F172A),
                            side: const BorderSide(color: Color(0xFF1D4ED8), width: 1.4),
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                          ),
                          onPressed: _busy
                              ? null
                              : () async {
                                  try {
                                    await _ensureAuth();
                                    final token = AppSession.instance.accessToken!;
                                    final match = await AppSession.instance.api.createLocalMatch(token);
                                    AppSession.instance.currentMatchId = match['match_id'] as String;
                                    if (mounted) {
                                      Navigator.pushNamed(context, '/match');
                                    }
                                  } catch (e) {
                                    if (!mounted) return;
                                    setState(() {
                                      _errorText = e.toString();
                                    });
                                  }
                                },
                          icon: const Icon(Icons.casino_rounded),
                          label: const Text('Local Pass-and-Play'),
                        ),
                      ),
                      if (_errorText != null) ...[
                        const SizedBox(height: 16),
                        Container(
                          width: double.infinity,
                          decoration: BoxDecoration(
                            color: const Color(0xFFFEE2E2),
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(color: const Color(0xFFF87171)),
                          ),
                          padding: const EdgeInsets.all(12),
                          child: Text(
                            _errorText!,
                            style: const TextStyle(color: Color(0xFF991B1B), fontSize: 13),
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
