/// API Configuration Constants
class ApiConstants {
  // Base URL for backend API
  static const String baseUrl = 'http://localhost:8000';
  
  // API Endpoints
  static const String healthEndpoint = '/api/health';
  static const String uploadEndpoint = '/api/documents/upload';
  static const String listDocumentsEndpoint = '/api/documents/list';
  static const String chatEndpoint = '/api/chat/ask';
  static const String summarizeEndpoint = '/api/chat/summarize';
  static const String generateMcqEndpoint = '/api/chat/generate-mcq';
  
  // Timeouts
  static const Duration connectionTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 60);
  
  // Request Headers
  static Map<String, String> get headers => {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };
}
