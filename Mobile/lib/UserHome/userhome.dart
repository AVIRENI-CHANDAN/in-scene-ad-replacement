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
  final Map<int, String> _steps = {
    1: "https://gyrus.ai/isar2d/assets/1.jpg",
    2: "https://gyrus.ai/isar2d/assets/2.jpg",
    3: "https://gyrus.ai/isar2d/assets/3.jpg",
  };

  @override
  void initState() {
    super.initState();
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
      appBar: AppNavigationBar(title: widget.appTitle, isAuthentiated: true),
      body: Stack(
        children: [
          // Scrollable content
          SingleChildScrollView(
            padding: const EdgeInsets.only(bottom: 70.0), // Space for button
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                // Welcome message
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Text(
                    "Welcome, ${_username ?? 'User'}!",
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),

                // Title for the steps
                const Padding(
                  padding: EdgeInsets.symmetric(vertical: 8.0),
                  child: Text(
                    "Simple steps you can follow for ISAR Demo",
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.w600),
                  ),
                ),

                // Steps images in a grid
                GridView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  padding: const EdgeInsets.all(16.0),
                  itemCount: _steps.length,
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 1,
                    crossAxisSpacing: 10,
                    mainAxisSpacing: 10,
                  ),
                  itemBuilder: (context, index) {
                    final step = _steps.entries.elementAt(index);
                    return Card(
                      child: Column(
                        children: [
                          Expanded(
                            child: Image.network(step.value, fit: BoxFit.cover),
                          ),
                          Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: Text(
                              "Step ${step.key}",
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),
                    );
                  },
                ),
              ],
            ),
          ),

          // Full-width fixed button
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              width: double.infinity,
              padding: const EdgeInsets.all(8.0),
              child: ElevatedButton(
                onPressed: () {
                  Navigator.pushNamed(context, "/new/project");
                },
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16.0),
                ),
                child: const Text(
                  "Try now",
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
