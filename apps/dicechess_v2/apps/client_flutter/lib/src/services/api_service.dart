import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiService {
  ApiService({required this.baseUrl});

  final String baseUrl;

  Future<Map<String, dynamic>> guestAuth() async {
    final res = await http.post(Uri.parse('$baseUrl/auth/guest'));
    if (res.statusCode != 200) {
      throw Exception('guest auth failed: ${res.statusCode} ${res.body}');
    }
    return jsonDecode(res.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> createLocalMatch(String accessToken) async {
    final res = await http.post(
      Uri.parse('$baseUrl/matches/local'),
      headers: {'Authorization': 'Bearer $accessToken'},
    );
    if (res.statusCode != 200) {
      throw Exception('create local match failed: ${res.statusCode} ${res.body}');
    }
    return jsonDecode(res.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> enqueue(String accessToken) async {
    final res = await http.post(
      Uri.parse('$baseUrl/matchmaking/enqueue'),
      headers: {
        'Authorization': 'Bearer $accessToken',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({'queue': 'casual'}),
    );
    if (res.statusCode != 200) {
      throw Exception('enqueue failed: ${res.statusCode} ${res.body}');
    }
    return jsonDecode(res.body) as Map<String, dynamic>;
  }

  Future<List<dynamic>> listMatches(String accessToken) async {
    final res = await http.get(
      Uri.parse('$baseUrl/matches'),
      headers: {'Authorization': 'Bearer $accessToken'},
    );
    if (res.statusCode != 200) {
      throw Exception('list matches failed: ${res.statusCode} ${res.body}');
    }
    return jsonDecode(res.body) as List<dynamic>;
  }

  Future<Map<String, dynamic>> getMatch(String accessToken, String matchId) async {
    final res = await http.get(
      Uri.parse('$baseUrl/matches/$matchId'),
      headers: {'Authorization': 'Bearer $accessToken'},
    );
    if (res.statusCode != 200) {
      throw Exception('get match failed: ${res.statusCode} ${res.body}');
    }
    return jsonDecode(res.body) as Map<String, dynamic>;
  }
}
