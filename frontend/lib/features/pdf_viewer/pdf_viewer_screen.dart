import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_pdfviewer/pdfviewer.dart';
import '../../core/constants/app_colors.dart';
import 'dart:io';

/// Modern PDF Viewer Screen with Controls
class PdfViewerScreen extends StatefulWidget {
  final String filePath;
  final String filename;

  const PdfViewerScreen({
    super.key,
    required this.filePath,
    required this.filename,
  });

  @override
  State<PdfViewerScreen> createState() => _PdfViewerScreenState();
}

class _PdfViewerScreenState extends State<PdfViewerScreen> {
  final PdfViewerController _pdfViewerController = PdfViewerController();
  int _currentPage = 1;
  int _totalPages = 0;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _pdfViewerController.addListener(() {
      setState(() {
        _currentPage = _pdfViewerController.pageNumber;
      });
    });
  }

  @override
  void dispose() {
    _pdfViewerController.dispose();
    super.dispose();
  }

  void _zoomIn() {
    setState(() {
      _pdfViewerController.zoomLevel = _pdfViewerController.zoomLevel + 0.25;
    });
  }

  void _zoomOut() {
    setState(() {
      if (_pdfViewerController.zoomLevel > 1) {
        _pdfViewerController.zoomLevel = _pdfViewerController.zoomLevel - 0.25;
      }
    });
  }

  void _previousPage() {
    if (_currentPage > 1) {
      _pdfViewerController.previousPage();
    }
  }

  void _nextPage() {
    if (_currentPage < _totalPages) {
      _pdfViewerController.nextPage();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Column(
        children: [
          // Modern Header with Controls
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
            decoration: BoxDecoration(
              color: AppColors.surface,
              border: Border(
                bottom: BorderSide(color: AppColors.divider, width: 1),
              ),
            ),
            child: Row(
              children: [
                // Back Button
                IconButton(
                  onPressed: () => Navigator.pop(context),
                  icon: const Icon(Icons.arrow_back_rounded),
                  color: AppColors.textPrimary,
                  tooltip: 'Back',
                ),
                const SizedBox(width: 12),
                
                // File Icon & Name
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [
                        AppColors.primary.withOpacity(0.2),
                        AppColors.accent.withOpacity(0.15),
                      ],
                    ),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Icon(
                    Icons.picture_as_pdf_rounded,
                    color: AppColors.primary,
                    size: 20,
                  ),
                ),
                const SizedBox(width: 12),
                
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        widget.filename,
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textPrimary,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      if (_totalPages > 0)
                        Text(
                          'Page $_currentPage of $_totalPages',
                          style: const TextStyle(
                            fontSize: 12,
                            color: AppColors.textSecondary,
                          ),
                        ),
                    ],
                  ),
                ),
                
                // Control Buttons
                _buildControlButton(
                  icon: Icons.remove_rounded,
                  onPressed: _zoomOut,
                  tooltip: 'Zoom Out',
                ),
                const SizedBox(width: 8),
                _buildControlButton(
                  icon: Icons.add_rounded,
                  onPressed: _zoomIn,
                  tooltip: 'Zoom In',
                ),
                const SizedBox(width: 8),
                _buildControlButton(
                  icon: Icons.chevron_left_rounded,
                  onPressed: _previousPage,
                  tooltip: 'Previous Page',
                  enabled: _currentPage > 1,
                ),
                const SizedBox(width: 8),
                _buildControlButton(
                  icon: Icons.chevron_right_rounded,
                  onPressed: _nextPage,
                  tooltip: 'Next Page',
                  enabled: _currentPage < _totalPages,
                ),
              ],
            ),
          ),
          
          // PDF Viewer
          Expanded(
            child: Container(
              margin: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.surfaceLight,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppColors.border, width: 1),
                boxShadow: [
                  BoxShadow(
                    color: AppColors.shadowDark,
                    blurRadius: 20,
                    spreadRadius: 5,
                  ),
                ],
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: Stack(
                  children: [
                    SfPdfViewer.file(
                      File(widget.filePath),
                      controller: _pdfViewerController,
                      onDocumentLoaded: (PdfDocumentLoadedDetails details) {
                        setState(() {
                          _totalPages = details.document.pages.count;
                          _isLoading = false;
                        });
                      },
                      canShowScrollHead: true,
                      canShowScrollStatus: true,
                      enableDoubleTapZooming: true,
                      canShowPaginationDialog: true,
                    ),
                    
                    // Loading Indicator
                    if (_isLoading)
                      Container(
                        color: AppColors.surface.withOpacity(0.9),
                        child: Center(
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              CircularProgressIndicator(
                                color: AppColors.primary,
                              ),
                              const SizedBox(height: 16),
                              Text(
                                'Loading PDF...',
                                style: TextStyle(
                                  color: AppColors.textSecondary,
                                  fontSize: 14,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildControlButton({
    required IconData icon,
    required VoidCallback onPressed,
    required String tooltip,
    bool enabled = true,
  }) {
    return Tooltip(
      message: tooltip,
      child: Container(
        decoration: BoxDecoration(
          color: enabled ? AppColors.surfaceLight : AppColors.backgroundElevated,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(
            color: enabled ? AppColors.border : AppColors.divider,
            width: 1,
          ),
        ),
        child: IconButton(
          onPressed: enabled ? onPressed : null,
          icon: Icon(icon),
          color: enabled ? AppColors.textPrimary : AppColors.textTertiary,
          iconSize: 20,
          constraints: const BoxConstraints(
            minWidth: 40,
            minHeight: 40,
          ),
          padding: EdgeInsets.zero,
        ),
      ),
    );
  }
}
