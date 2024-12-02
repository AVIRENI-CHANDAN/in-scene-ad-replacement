import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:mobile/NavigationBar/navigationbar.dart';

class UserHome extends StatefulWidget {
  final String appTitle;

  const UserHome({super.key, required this.appTitle});

  @override
  State<StatefulWidget> createState() {
    return UserHomeState();
  }
}

class UserHomeState extends State<UserHome> {
  String? _username;

  @override
  void initState() {
    super.initState();
    // Get username in initState to avoid rebuilding
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _extractUsernameFromToken();
    });
  }

  void _extractUsernameFromToken() {
    final arguments =
        ModalRoute.of(context)?.settings.arguments as Map<String, dynamic>?;
    final idToken = arguments?['idToken'] as String?;

    if (idToken != null) {
      try {
        final parts = idToken.split('.');
        if (parts.length == 3) {
          final payload = parts[1];
          final normalized = base64Url.normalize(payload);
          final decoded = utf8.decode(base64Url.decode(normalized));
          final decodedToken = json.decode(decoded);

          setState(() {
            // Try different possible claims for username
            _username =
                decodedToken['cognito:username'] ??
                decodedToken['email'] ??
                decodedToken['preferred_username'] ??
                'User';
          });
        }
      } catch (e) {
        debugPrint('Error decoding token: $e');
        setState(() {
          _username = 'User';
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppNavigationBar(title: widget.appTitle),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              "Welcome, ${_username ?? 'User'}!",
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            const Text("User home page"),
          ],
        ),
      ),
    );
  }
}
