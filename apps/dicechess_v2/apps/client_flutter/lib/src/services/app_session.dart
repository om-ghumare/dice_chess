import 'api_service.dart';

class AppSession {
  AppSession._();

  static final AppSession instance = AppSession._();

  static const String apiBaseUrl = 'http://127.0.0.1:8000';
  static const String wsBaseUrl = 'ws://127.0.0.1:8000';

  final ApiService api = ApiService(baseUrl: apiBaseUrl);

  String? accessToken;
  String? userId;
  String? currentMatchId;
}
