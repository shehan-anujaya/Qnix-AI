import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/constants/api_constants.dart';

/// API Service for backend communication
class ApiService {
  /// Check backend health
  Future<Map<String, dynamic>> checkHealth() async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConstants.baseUrl}${ApiConstants.healthEndpoint}'),
      ).timeout(ApiConstants.connectionTimeout);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Health check failed: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Cannot connect to backend: $e');
    }
  }

  /// Upload a PDF document
  Future<Map<String, dynamic>> uploadDocument(String filePath) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('${ApiConstants.baseUrl}${ApiConstants.uploadEndpoint}'),
      );

      request.files.add(await http.MultipartFile.fromPath('file', filePath));

      final streamedResponse = await request.send().timeout(
        const Duration(minutes: 5),
      );

      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        final error = json.decode(response.body);
        throw Exception(error['detail'] ?? 'Upload failed');
      }
    } catch (e) {
      throw Exception('Failed to upload document: $e');
    }
  }

  /// List all documents
  Future<Map<String, dynamic>> listDocuments() async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConstants.baseUrl}${ApiConstants.listDocumentsEndpoint}'),
      ).timeout(ApiConstants.connectionTimeout);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to list documents: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to list documents: $e');
    }
  }

  /// Ask a question
  Future<Map<String, dynamic>> askQuestion({
    required String question,
    List<Map<String, String>>? conversationHistory,
    int maxSources = 3,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConstants.baseUrl}${ApiConstants.chatEndpoint}'),
        headers: ApiConstants.headers,
        body: json.encode({
          'question': question,
          'conversation_history': conversationHistory ?? [],
          'max_sources': maxSources,
        }),
      ).timeout(ApiConstants.receiveTimeout);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        final error = json.decode(response.body);
        throw Exception(error['detail'] ?? 'Failed to get answer');
      }
    } catch (e) {
      throw Exception('Failed to ask question: $e');
    }
  }

  /// Delete a document
  Future<void> deleteDocument(String fileId) async {
    try {
      final response = await http.delete(
        Uri.parse('${ApiConstants.baseUrl}/api/documents/$fileId'),
      ).timeout(ApiConstants.connectionTimeout);

      if (response.statusCode != 200) {
        final error = json.decode(response.body);
        throw Exception(error['detail'] ?? 'Failed to delete document');
      }
    } catch (e) {
      throw Exception('Failed to delete document: $e');
    }
  }
}
