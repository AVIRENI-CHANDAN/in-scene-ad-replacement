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
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppNavigationBar(title: widget.appTitle),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [const Text("User home page")],
        ),
      ),
    );
  }
}
