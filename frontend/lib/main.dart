import 'package:flutter/material.dart';
import 'package:window_manager/window_manager.dart';
import 'package:provider/provider.dart';
import 'app.dart';
import 'core/theme/theme_provider.dart';

/// Main entry point for Qnix AI Desktop Application
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Configure desktop window
  await windowManager.ensureInitialized();
  
  const windowOptions = WindowOptions(
    size: Size(1400, 900),
    minimumSize: Size(1000, 700),
    center: true,
    backgroundColor: Colors.transparent,
    skipTaskbar: false,
    titleBarStyle: TitleBarStyle.normal,
    title: 'Qnix AI - Knowledge Archive',
  );
  
  await windowManager.waitUntilReadyToShow(windowOptions, () async {
    await windowManager.show();
    await windowManager.focus();
  });
  
  runApp(
    ChangeNotifierProvider(
      create: (_) => ThemeProvider(),
      child: const QnixApp(),
    ),
  );
}
