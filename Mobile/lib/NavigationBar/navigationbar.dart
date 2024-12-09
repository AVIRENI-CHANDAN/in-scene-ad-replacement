import 'package:flutter/material.dart';
import 'package:mobile/theme/colors.dart';

import 'actionbuttons.dart';

class AppNavigationBar extends StatelessWidget implements PreferredSizeWidget {
  final String title;
  bool isAuthentiated = false;

  AppNavigationBar({
    super.key,
    required this.title,
    this.isAuthentiated = false,
  });

  @override
  Widget build(BuildContext context) {
    return AppBar(
      leading: Container(width: 0),
      title: GestureDetector(
        onTap: () {
          Navigator.pushNamed(context, "/");
        },
        child: Text(
          title,
          style: TextStyle(
            fontStyle: FontStyle.italic,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      backgroundColor: AppColors.primary,
      actions: [
        if (!isAuthentiated) UserRegistrationActionButton(),
        if (!isAuthentiated) UserLoginActionButton(),
        if (isAuthentiated) ProfileActionButton(),
      ],
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(kToolbarHeight);
}
