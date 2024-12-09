import 'package:cookie_jar/cookie_jar.dart';
import 'package:dio/dio.dart';
import 'package:dio_cookie_manager/dio_cookie_manager.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:mobile/NavigationBar/navigationbar.dart';
import 'package:mobile/app_config.dart';

class LoginPage extends StatefulWidget {
  final String appTitle;

  const LoginPage({super.key, required this.appTitle});

  @override
  State<StatefulWidget> createState() {
    return LoginPageState();
  }
}

class LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _isLoading = false;

  final Dio dio = Dio();
  final CookieJar cookieJar = CookieJar();

  @override
  void initState() {
    super.initState();
    dio.interceptors.add(CookieManager(cookieJar));
  }

  String? _extractIdToken(List<Cookie> cookies) {
    try {
      final idTokenCookie = cookies.firstWhere(
        (cookie) => cookie.name == 'id_token',
        orElse: () => Cookie('id_token', ''),
      );
      return idTokenCookie.value.isNotEmpty ? idTokenCookie.value : null;
    } catch (e) {
      if (kDebugMode) {
        print('Error extracting id_token: $e');
      }
      return null;
    }
  }

  Future<void> _login() async {
    if (_formKey.currentState!.validate()) {
      setState(() {
        _isLoading = true;
      });

      final url = '${AppConfig.baseUrl}/auth/login';
      try {
        final response = await dio.post(
          url,
          data: {
            'username': _usernameController.text,
            'password': _passwordController.text,
          },
        );

        setState(() {
          _isLoading = false;
        });

        if (response.statusCode == 200) {
          // Get cookies for the domain
          final cookies = await cookieJar.loadForRequest(
            Uri.parse(AppConfig.baseUrl),
          );
          final idToken = _extractIdToken(cookies);

          if (idToken != null) {
            if (kDebugMode) {
              print('ID Token retrieved successfully');
            }

            _passwordController.clear();
            // Navigate to home screen with the token
            Navigator.pushReplacementNamed(
              context,
              "/user/home",
              arguments: {'idToken': idToken},
            );
          } else {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('Failed to get authentication token'),
              ),
            );
          }
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error: ${response.statusMessage}')),
          );
        }
      } catch (error) {
        setState(() {
          _isLoading = false;
        });
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('An error occurred: $error')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppNavigationBar(title: widget.appTitle),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              const Text(
                "Login Page",
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 20),
              TextFormField(
                controller: _usernameController,
                decoration: const InputDecoration(
                  labelText: 'Username',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter your username';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              TextFormField(
                controller: _passwordController,
                decoration: const InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                ),
                obscureText: true,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter your password';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              _isLoading
                  ? const CircularProgressIndicator()
                  : ElevatedButton(
                    onPressed: _login,
                    child: const Text('Login'),
                  ),
            ],
          ),
        ),
      ),
    );
  }
}
