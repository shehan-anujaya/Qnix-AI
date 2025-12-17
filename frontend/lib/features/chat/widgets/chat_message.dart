import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:frontend_flutter/core/constants/app_colors.dart';

/// Chat message widget
class ChatMessage extends StatelessWidget {
  final String message;
  final bool isUser;
  final List<Map<String, dynamic>>? sources;
  final DateTime timestamp;

  const ChatMessage({
    super.key,
    required this.message,
    required this.isUser,
    this.sources,
    required this.timestamp,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        children: [
          if (!isUser) ...[
            _buildAvatar(),
            const SizedBox(width: 12),
          ],
          Flexible(
            child: Column(
              crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: BoxDecoration(
                    color: isUser ? AppColors.primary.withOpacity(0.1) : AppColors.background,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(
                      color: isUser 
                          ? AppColors.primary.withOpacity(0.3)
                          : AppColors.border,
                      width: 1,
                    ),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      MarkdownBody(
                        data: message,
                        styleSheet: MarkdownStyleSheet(
                          p: const TextStyle(
                            color: AppColors.textPrimary,
                            fontSize: 14,
                            height: 1.5,
                          ),
                          strong: const TextStyle(
                            color: AppColors.textPrimary,
                            fontWeight: FontWeight.bold,
                          ),
                          em: const TextStyle(
                            color: AppColors.textPrimary,
                            fontStyle: FontStyle.italic,
                          ),
                          code: TextStyle(
                            backgroundColor: AppColors.background,
                            color: AppColors.accent,
                            fontFamily: 'monospace',
                            fontSize: 13,
                          ),
                          codeblockDecoration: BoxDecoration(
                            color: AppColors.background,
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: AppColors.border),
                          ),
                          blockquote: const TextStyle(
                            color: AppColors.textSecondary,
                            fontStyle: FontStyle.italic,
                          ),
                          h1: const TextStyle(
                            color: AppColors.textPrimary,
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                          ),
                          h2: const TextStyle(
                            color: AppColors.textPrimary,
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                          h3: const TextStyle(
                            color: AppColors.textPrimary,
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                          ),
                          listBullet: const TextStyle(
                            color: AppColors.accent,
                          ),
                        ),
                        selectable: true,
                      ),
                      if (sources != null && sources!.isNotEmpty) ...[
                        const SizedBox(height: 12),
                        const Divider(height: 1),
                        const SizedBox(height: 8),
                        _buildSources(),
                      ],
                    ],
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  _formatTime(timestamp),
                  style: const TextStyle(
                    color: AppColors.textTertiary,
                    fontSize: 11,
                  ),
                ),
              ],
            ),
          ),
          if (isUser) ...[
            const SizedBox(width: 12),
            _buildAvatar(),
          ],
        ],
      ),
    );
  }

  Widget _buildAvatar() {
    return Container(
      width: 36,
      height: 36,
      decoration: BoxDecoration(
        color: isUser ? AppColors.primary : AppColors.accent,
        shape: BoxShape.circle,
      ),
      child: Icon(
        isUser ? Icons.person : Icons.smart_toy_outlined,
        color: Colors.white,
        size: 20,
      ),
    );
  }

  Widget _buildSources() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Sources:',
          style: TextStyle(
            color: AppColors.textSecondary,
            fontSize: 12,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 6),
        ...sources!.take(3).map((source) {
          return Padding(
            padding: const EdgeInsets.only(bottom: 4),
            child: Row(
              children: [
                const Icon(
                  Icons.description_outlined,
                  size: 14,
                  color: AppColors.accent,
                ),
                const SizedBox(width: 6),
                Expanded(
                  child: Text(
                    source['filename'] ?? 'Unknown',
                    style: const TextStyle(
                      color: AppColors.textSecondary,
                      fontSize: 11,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    color: AppColors.accent.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    '${((source['relevance_score'] ?? 0) * 100).toInt()}%',
                    style: const TextStyle(
                      color: AppColors.accent,
                      fontSize: 10,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
          );
        }).toList(),
      ],
    );
  }

  String _formatTime(DateTime time) {
    final now = DateTime.now();
    final difference = now.difference(time);

    if (difference.inMinutes < 1) {
      return 'Just now';
    } else if (difference.inHours < 1) {
      return '${difference.inMinutes}m ago';
    } else if (difference.inDays < 1) {
      return '${difference.inHours}h ago';
    } else {
      return '${time.hour.toString().padLeft(2, '0')}:${time.minute.toString().padLeft(2, '0')}';
    }
  }
}
