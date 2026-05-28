import 'package:flutter/material.dart';

import 'screens/history_screen.dart';
import 'screens/home_screen.dart';
import 'screens/lobby_screen.dart';
import 'screens/match_screen.dart';
import 'screens/profile_screen.dart';
import 'screens/room_screen.dart';

class DiceChessApp extends StatelessWidget {
  const DiceChessApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Dice Chess',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0D9488)),
        useMaterial3: true,
      ),
      initialRoute: '/',
      routes: {
        '/': (_) => const HomeScreen(),
        '/lobby': (_) => const LobbyScreen(),
        '/room': (_) => const RoomScreen(),
        '/match': (_) => const MatchScreen(),
        '/history': (_) => const HistoryScreen(),
        '/profile': (_) => const ProfileScreen(),
      },
    );
  }
}
