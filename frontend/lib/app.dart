import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'core/theme/app_theme.dart';
import 'core/theme/theme_provider.dart';
import 'features/chat/chat_screen.dart';
import 'features/documents/documents_screen.dart';
import 'features/settings/settings_screen.dart';
import 'widgets/sidebar_navigation.dart';

/// Root application widget
class QnixApp extends StatelessWidget {
  const QnixApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<ThemeProvider>(
      builder: (context, theme, _) => MaterialApp(
        title: 'Qnix AI',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: theme.mode,
        home: const MainScreen(),
      ),
    );
  }
}

/// Main screen with sidebar navigation
class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _selectedIndex = 0;

  void _onNavigationChanged(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          // Sidebar Navigation
          SidebarNavigation(
            selectedIndex: _selectedIndex,
            onNavigationChanged: _onNavigationChanged,
          ),
          
          // Main Content Area
          Expanded(
            child: IndexedStack(
              index: _selectedIndex,
              children: const [
                ChatScreen(),
                DocumentsScreen(),
                SettingsScreen(),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
