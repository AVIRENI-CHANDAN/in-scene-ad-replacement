import 'package:flutter/material.dart';

import '../NavigationBar/navigationbar.dart';

class LandingPage extends StatefulWidget {
  final String appTitle;
  const LandingPage({super.key, required this.appTitle});

  @override
  State<StatefulWidget> createState() => LandingPageState();
}

class LandingPageState extends State<LandingPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppNavigationBar(title: widget.appTitle),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text("Hello world"),
            const Text("How are you doing today?"),
          ],
        ),
      ),
    );
  }
}
