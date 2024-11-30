import 'package:flutter/material.dart';
import 'package:mobile/theme/colors.dart';

import 'actionbuttons.dart';

class AppNavigationBar extends StatelessWidget implements PreferredSizeWidget {
  final String title;

  const AppNavigationBar({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    final currentRoute = ModalRoute.of(context)?.settings.name;

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
        if (currentRoute != "/register") UserRegistrationActionButton(),
        if (currentRoute != "/login") UserLoginActionButton(),
      ],
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(kToolbarHeight);
}
