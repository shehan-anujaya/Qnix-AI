import 'package:flutter/material.dart';
import 'package:frontend_flutter/core/constants/app_colors.dart';

/// Document card widget
class DocumentCard extends StatelessWidget {
  final String filename;
  final String uploadDate;
  final double sizeMb;
  final VoidCallback? onDelete;

  const DocumentCard({
    super.key,
    required this.filename,
    required this.uploadDate,
    required this.sizeMb,
    this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            // PDF Icon
            Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                color: AppColors.error.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(
                Icons.picture_as_pdf,
                color: AppColors.error,
                size: 24,
              ),
            ),
            
            const SizedBox(width: 16),
            
            // Document Info
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    filename,
                    style: const TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.w600,
                      color: AppColors.textPrimary,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 4),
                  Row(
                    children: [
                      Icon(
                        Icons.calendar_today,
                        size: 12,
                        color: AppColors.textTertiary,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        _formatDate(uploadDate),
                        style: const TextStyle(
                          fontSize: 12,
                          color: AppColors.textSecondary,
                        ),
                      ),
                      const SizedBox(width: 16),
                      const Icon(
                        Icons.storage,
                        size: 12,
                        color: AppColors.textTertiary,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        '${sizeMb.toStringAsFixed(2)} MB',
                        style: const TextStyle(
                          fontSize: 12,
                          color: AppColors.textSecondary,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            
            // Actions
            if (onDelete != null)
              IconButton(
                onPressed: onDelete,
                icon: const Icon(Icons.delete_outline),
                color: AppColors.error,
                tooltip: 'Delete document',
              ),
          ],
        ),
      ),
    );
  }

  String _formatDate(String dateStr) {
    try {
      // Parse YYYYMMDD_HHMMSS format
      if (dateStr.length >= 8) {
        final year = dateStr.substring(0, 4);
        final month = dateStr.substring(4, 6);
        final day = dateStr.substring(6, 8);
        return '$day/$month/$year';
      }
      return dateStr;
    } catch (e) {
      return dateStr;
    }
  }
}
