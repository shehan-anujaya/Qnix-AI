import 'package:flutter/material.dart';
import '../core/constants/app_colors.dart';

/// Modern Minimal Sidebar Navigation - Black Matte Design
class SidebarNavigation extends StatefulWidget {
  final int selectedIndex;
  final Function(int) onNavigationChanged;

  const SidebarNavigation({
    super.key,
    required this.selectedIndex,
    required this.onNavigationChanged,
  });

  @override
  State<SidebarNavigation> createState() => _SidebarNavigationState();
}

class _SidebarNavigationState extends State<SidebarNavigation> {
  int? _hoveredIndex;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 72,
      decoration: BoxDecoration(
        color: AppColors.surface,
        border: Border(
          right: BorderSide(color: AppColors.divider, width: 1),
        ),
      ),
      child: Column(
        children: [
          const SizedBox(height: 20),
          
          // App Logo
          Container(
            width: 44,
            height: 44,
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                colors: [AppColors.primary, AppColors.accent],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              borderRadius: BorderRadius.circular(14),
              boxShadow: [
                BoxShadow(
                  color: AppColors.primaryGlow,
                  blurRadius: 12,
                  spreadRadius: 2,
                ),
              ],
            ),
            child: const Icon(
              Icons.auto_awesome_rounded,
              color: Colors.white,
              size: 24,
            ),
          ),
          
          const SizedBox(height: 32),
          const Divider(height: 1, indent: 16, endIndent: 16),
          const SizedBox(height: 16),
          
          // Navigation Items
          _buildNavItem(
            index: 0,
            icon: Icons.chat_bubble_rounded,
            label: 'Chat',
          ),
          const SizedBox(height: 8),
          _buildNavItem(
            index: 1,
            icon: Icons.description_rounded,
            label: 'Documents',
          ),
          const SizedBox(height: 8),
          _buildNavItem(
            index: 2,
            icon: Icons.settings_rounded,
            label: 'Settings',
          ),
          
          const Spacer(),
          
          // Status Indicator
          Container(
            margin: const EdgeInsets.only(bottom: 20),
            child: Column(
              children: [
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppColors.backgroundElevated,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(
                    Icons.check_circle_rounded,
                    color: AppColors.success,
                    size: 20,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildNavItem({
    required int index,
    required IconData icon,
    required String label,
  }) {
    final isSelected = widget.selectedIndex == index;
    final isHovered = _hoveredIndex == index;

    return MouseRegion(
      onEnter: (_) => setState(() => _hoveredIndex = index),
      onExit: (_) => setState(() => _hoveredIndex = null),
      child: Tooltip(
        message: label,
        preferBelow: false,
        child: GestureDetector(
          onTap: () => widget.onNavigationChanged(index),
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            curve: Curves.easeInOut,
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              gradient: isSelected
                  ? LinearGradient(
                      colors: [
                        AppColors.primary.withOpacity(0.2),
                        AppColors.accent.withOpacity(0.15),
                      ],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    )
                  : null,
              color: isHovered && !isSelected
                  ? AppColors.surfaceHover
                  : Colors.transparent,
              borderRadius: BorderRadius.circular(14),
              border: isSelected
                  ? Border.all(color: AppColors.primary, width: 1.5)
                  : null,
              boxShadow: isSelected
                  ? [
                      BoxShadow(
                        color: AppColors.primaryGlow,
                        blurRadius: 8,
                        spreadRadius: 1,
                      ),
                    ]
                  : null,
            ),
            child: Icon(
              icon,
              size: 24,
              color: isSelected
                  ? AppColors.primary
                  : isHovered
                      ? AppColors.textPrimary
                      : AppColors.textSecondary,
            ),
          ),
        ),
      ),
    );
  }
}
