import 'package:flutter/material.dart';

/// Theme provider to manage light/dark ThemeMode
class ThemeProvider extends ChangeNotifier {
  ThemeMode _mode = ThemeMode.dark;

  ThemeMode get mode => _mode;
  bool get isLight => _mode == ThemeMode.light;

  void setMode(ThemeMode mode) {
    if (_mode != mode) {
      _mode = mode;
      notifyListeners();
    }
  }

  void toggleLight(bool enable) {
    setMode(enable ? ThemeMode.light : ThemeMode.dark);
  }
}
