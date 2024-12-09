import 'package:flutter/material.dart';
import 'package:mobile/theme/colors.dart';

class UserRegistrationActionButton extends StatelessWidget {
  const UserRegistrationActionButton({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 4),
      child: ElevatedButton.icon(
        label: Text(
          "Signup",
          style: TextStyle(fontSize: 10, color: AppColors.textPrimary),
        ),
        icon: Icon(Icons.person_add, color: AppColors.textPrimary),
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
        label: Text(
          "Signin",
          style: TextStyle(fontSize: 10, color: AppColors.textPrimary),
        ),
        icon: Icon(Icons.login, color: AppColors.textPrimary),
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

class ProfileActionButton extends StatelessWidget {
  const ProfileActionButton({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 8),
      child: ElevatedButton.icon(
        label: Text(
          "Profile",
          style: TextStyle(fontSize: 10, color: AppColors.textPrimary),
        ),
        icon: Icon(Icons.account_circle, color: AppColors.textPrimary),
        onPressed: () {
          // Define notifications action
          // ScaffoldMessenger.of(
          //   context,
          // ).showSnackBar(SnackBar(content: Text('Login action pressed')));
          Navigator.pushNamed(context, "/profile");
        },
      ),
    );
  }
}
