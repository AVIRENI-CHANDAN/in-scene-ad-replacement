import 'package:flutter/material.dart';

class UserRegistrationActionButton extends StatelessWidget {
  const UserRegistrationActionButton({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 4),
      child: ElevatedButton.icon(
        label: Text("Signup", style: TextStyle(fontSize: 10)),
        icon: Icon(Icons.person_add),
        onPressed: () {
          // ScaffoldMessenger.of(context).showSnackBar(
          //   SnackBar(content: Text('Registration Button pressed')),
          // );
          Navigator.pushNamed(context, "/register");
        },
      ),
    );
  }
}

class UserLoginActionButton extends StatelessWidget {
  const UserLoginActionButton({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 8),
      child: ElevatedButton.icon(
        label: Text("Signin", style: TextStyle(fontSize: 10)),
        icon: Icon(Icons.login),
        onPressed: () {
          // Define notifications action
          // ScaffoldMessenger.of(
          //   context,
          // ).showSnackBar(SnackBar(content: Text('Login action pressed')));
          Navigator.pushNamed(context, "/login");
        },
      ),
    );
  }
}
