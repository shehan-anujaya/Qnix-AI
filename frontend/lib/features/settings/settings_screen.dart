import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../core/constants/app_colors.dart';
import '../../services/api_service.dart';
import '../../core/theme/theme_provider.dart';

/// Settings screen
class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final ApiService _apiService = ApiService();
  Map<String, dynamic>? _healthStatus;
  bool _isCheckingHealth = false;

  @override
  void initState() {
    super.initState();
    _checkHealth();
  }

  Future<void> _checkHealth() async {
    setState(() => _isCheckingHealth = true);
    
    try {
      final health = await _apiService.checkHealth();
      setState(() {
        _healthStatus = health;
        _isCheckingHealth = false;
      });
    } catch (e) {
      setState(() {
        _healthStatus = {'status': 'error', 'error': e.toString()};
        _isCheckingHealth = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.background,
      body: Column(
        children: [
          // Header
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surface,
              border: Border(
                bottom: BorderSide(color: Theme.of(context).dividerColor, width: 1),
              ),
            ),
            child: Row(
              children: [
                const Icon(
                  Icons.settings_outlined,
                  color: AppColors.primary,
                  size: 28,
                ),
                const SizedBox(width: 12),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Settings',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w600,
                        color: Theme.of(context).colorScheme.onSurface,
                      ),
                    ),
                    Text(
                      'Configure your application',
                      style: TextStyle(
                        fontSize: 13,
                        color: Theme.of(context).textTheme.bodySmall?.color,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),

          // Content
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(24),
              children: [
                // Appearance
                _buildSection(
                  title: 'Appearance',
                  children: [
                    Card(
                      child: SwitchListTile(
                        title: const Text(
                          'Light Mode',
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                        subtitle: const Text('Enable bright interface'),
                        value: context.watch<ThemeProvider>().isLight,
                        onChanged: (val) => context.read<ThemeProvider>().toggleLight(val),
                        secondary: const Icon(Icons.light_mode),
                      ),
                    ),
                  ],
                ),

                // System Status
                _buildSection(
                  title: 'System Status',
                  children: [
                    _buildStatusCard(),
                  ],
                ),

                const SizedBox(height: 24),

                // About
                _buildSection(
                  title: 'About',
                  children: [
                    _buildInfoTile(
                      icon: Icons.info_outline,
                      title: 'Version',
                      subtitle: '1.0.0',
                    ),
                    _buildInfoTile(
                      icon: Icons.school_outlined,
                      title: 'Purpose',
                      subtitle: 'AI-Powered Knowledge Archive for Sri Lankan Students',
                    ),
                    _buildInfoTile(
                      icon: Icons.code,
                      title: 'Technology',
                      subtitle: 'Flutter Desktop + Python FastAPI + Ollama',
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSection({required String title, required List<Widget> children}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            color: Colors.black87,
          ),
        ),
        const SizedBox(height: 12),
        ...children,
      ],
    );
  }

  Widget _buildStatusCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Text(
                  'Backend Connection',
                  style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                    color: AppColors.textPrimary,
                  ),
                ),
                const Spacer(),
                TextButton.icon(
                  onPressed: _isCheckingHealth ? null : _checkHealth,
                  icon: const Icon(Icons.refresh, size: 16),
                  label: const Text('Refresh'),
                ),
              ],
            ),
            const SizedBox(height: 12),
            if (_isCheckingHealth)
              const Center(
                child: Padding(
                  padding: EdgeInsets.all(16.0),
                  child: CircularProgressIndicator(),
                ),
              )
            else if (_healthStatus != null) ...[
              _buildHealthItem(
                'Status',
                _healthStatus!['status'] ?? 'unknown',
                _healthStatus!['status'] == 'healthy',
              ),
              if (_healthStatus!['services'] != null) ...[
                const Divider(height: 24),
                _buildHealthItem(
                  'Ollama',
                  _healthStatus!['services']['ollama']?['status'] ?? 'unknown',
                  _healthStatus!['services']['ollama']?['status'] == 'connected',
                ),
                _buildHealthItem(
                  'Vector Store',
                  _healthStatus!['services']['vector_store']?['status'] ?? 'unknown',
                  _healthStatus!['services']['vector_store']?['status'] == 'initialized',
                ),
              ],
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildHealthItem(String label, String value, bool isHealthy) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Container(
            width: 8,
            height: 8,
            decoration: BoxDecoration(
              color: isHealthy ? AppColors.success : AppColors.error,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: 12),
          Text(
            '$label:',
            style: const TextStyle(
              fontSize: 13,
              color: AppColors.textSecondary,
            ),
          ),
          const SizedBox(width: 8),
          Text(
            value,
            style: const TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w500,
              color: AppColors.textPrimary,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoTile({
    required IconData icon,
    required String title,
    required String subtitle,
  }) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Icon(icon, color: AppColors.primary),
        title: Text(
          title,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w500,
            color: AppColors.textPrimary,
          ),
        ),
        subtitle: Text(
          subtitle,
          style: const TextStyle(
            fontSize: 13,
            color: AppColors.textSecondary,
          ),
        ),
      ),
    );
  }
}
