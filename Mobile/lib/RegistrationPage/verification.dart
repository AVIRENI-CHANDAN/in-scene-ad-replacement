import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:mobile/NavigationBar/navigationbar.dart';
import 'package:mobile/app_config.dart';

class VerificationPage extends StatefulWidget {
  final String appTitle;

  const VerificationPage({super.key, required this.appTitle});

  @override
  State<StatefulWidget> createState() {
    return VerificationPageState();
  }
}

class VerificationPageState extends State<VerificationPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _codeController = TextEditingController();
  bool _isLoading = false;

  final Dio dio = Dio();

  // Function to verify the sign-up
  Future<void> _verifySignUp(String username) async {
    if (_formKey.currentState!.validate()) {
      setState(() {
        _isLoading = true;
      });

      final url = '${AppConfig.baseUrl}/auth/verify_sign_up';
      try {
        final response = await dio.post(
          url,
          data: {'username': username, 'code': _codeController.text},
        );

        setState(() {
          _isLoading = false;
        });

        if (response.statusCode == 200) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Verification Successful!')),
          );
          Navigator.pushNamed(context, "/user/home");
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

  // Function to resend the verification code
  Future<void> _resendVerificationCode(String username) async {
    setState(() {
      _isLoading = true;
    });
    final url = '${AppConfig.baseUrl}/auth/resend-verification';
    try {
      final response = await dio.post(url, data: {'username': username});
      setState(() {
        _isLoading = false;
      });
      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Verification code resent!')),
        );
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

  @override
  Widget build(BuildContext context) {
    // Retrieve the username from arguments
    final String username =
        ModalRoute.of(context)!.settings.arguments as String;

    return Scaffold(
      appBar: AppNavigationBar(title: widget.appTitle),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text(
                "Verification Page",
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 20),
              Text("Verifying User: $username", style: TextStyle(fontSize: 16)),
              const SizedBox(height: 20),
              TextFormField(
                controller: _codeController,
                decoration: const InputDecoration(
                  labelText: 'Verification Code',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter the verification code';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              _isLoading
                  ? const CircularProgressIndicator()
                  : ElevatedButton(
                    onPressed: () => _verifySignUp(username),
                    child: const Text('Verify'),
                  ),
              const SizedBox(height: 20),
              TextButton(
                onPressed: () => _resendVerificationCode(username),
                child: const Text('Resend Verification Code'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
