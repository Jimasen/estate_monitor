import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  // Change this once when you deploy
  static const String _devBaseUrl = "http://127.0.0.1:8000";
  static const String _prodBaseUrl = "https://api.estatemonitor.com";

  static String get baseUrl {
    // Auto-switch based on build mode
    return const bool.fromEnvironment('dart.vm.product')
        ? _prodBaseUrl
        : _devBaseUrl;
  }

  static const Duration _timeout = Duration(seconds: 15);

  // ---------------- GET ----------------
  static Future<http.Response> get(
    String endpoint, {
    String? token,
  }) async {
    try {
      final response = await http
          .get(
            Uri.parse("$baseUrl$endpoint"),
            headers: _headers(token),
          )
          .timeout(_timeout);

      return _handleResponse(response);
    } on SocketException {
      throw Exception("No internet connection");
    } on HttpException {
      throw Exception("Service not available");
    } on FormatException {
      throw Exception("Bad response format");
    } catch (e) {
      throw Exception("Unexpected error: $e");
    }
  }

  // ---------------- POST ----------------
  static Future<http.Response> post(
    String endpoint,
    Map<String, dynamic> body, {
    String? token,
  }) async {
    try {
      final response = await http
          .post(
            Uri.parse("$baseUrl$endpoint"),
            headers: _headers(token),
            body: jsonEncode(body),
          )
          .timeout(_timeout);

      return _handleResponse(response);
    } on SocketException {
      throw Exception("No internet connection");
    } catch (e) {
      throw Exception("Unexpected error: $e");
    }
  }

  // ---------------- HELPERS ----------------
  static Map<String, String> _headers(String? token) {
    final headers = <String, String>{
      "Content-Type": "application/json",
      "Accept": "application/json",
    };

    if (token != null && token.isNotEmpty) {
      headers["Authorization"] = "Bearer $token";
    }

    return headers;
  }

  static http.Response _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return response;
    } else {
      final body = response.body.isNotEmpty
          ? jsonDecode(response.body)
          : {"detail": "Unknown error"};

      throw Exception(
        body["detail"] ??
            "Request failed with status: ${response.statusCode}",
      );
    }
  }
}
