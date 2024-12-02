import 'package:flutter/material.dart';
import 'package:mobile/LoginPage/loginpage.dart';
import 'package:mobile/RegistrationPage/registrationpage.dart';
import 'package:mobile/RegistrationPage/verification.dart';
import 'package:mobile/UserHome/userhome.dart';

import 'LandingPage/landingpage.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Gyrus Flutter Application',
      initialRoute: "/login",
      routes: {
        "/": (context) => LandingPage(appTitle: "Gyrus"),
        "/login": (context) => LoginPage(appTitle: "Gyrus"),
        "/register": (context) => RegistrationPage(appTitle: "Gyrus"),
        "/user/home": (context) => UserHome(appTitle: "Gyrus"),
        '/verify_sign_up': (context) => VerificationPage(appTitle: 'Gyrus'),
      },
    );
  }
}