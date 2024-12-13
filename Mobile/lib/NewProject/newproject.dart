import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

class NewProject extends StatefulWidget {
  const NewProject({super.key});

  @override
  _NewProjectState createState() => _NewProjectState();
}

class _NewProjectState extends State<NewProject> {
  final _formKey = GlobalKey<FormState>();
  String _projectTitle = '';
  String _projectDescription = '';
  final String _error = '';
  bool _isSubmitting = false;
  final String _user = 'Anonymous User';
  PlatformFile? _file;

  void _submitForm() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _isSubmitting = true;
    });

    // Mock a network call for submission
    await Future.delayed(const Duration(seconds: 2), () {
      // Reset state on success
      setState(() {
        _isSubmitting = false;
        _projectTitle = '';
        _projectDescription = '';
        _file = null;
      });

      // Navigate to another screen if needed
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Project created successfully!')));
    });
  }

  void _pickFile() async {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(SnackBar(content: Text('Project file browse')));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Create New Project")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Greeting Section
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  "Welcome",
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                Text(
                  _user,
                  style: const TextStyle(fontSize: 18, color: Colors.grey),
                ),
              ],
            ),
            const SizedBox(height: 20),

            // Instructions Section
            const Text(
              "Create a project to explore logo placement model",
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 10),
            Container(
              padding: const EdgeInsets.all(8.0),
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey.shade300),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  Text(
                    "Instructions:",
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  SizedBox(height: 5),
                  Text("1. Create a project if not created."),
                  Text("2. Give a proper name for your project."),
                  Text("3. Choose a video for logo placement."),
                  Text(
                    "4. Delete the project if you want to start with a new one.",
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Form Section
            Form(
              key: _formKey,
              child: Column(
                children: [
                  // Project Title
                  TextFormField(
                    decoration: const InputDecoration(
                      labelText: "Project Name",
                      border: OutlineInputBorder(),
                    ),
                    initialValue: _projectTitle,
                    validator: (value) {
                      if (value == null || value.trim().isEmpty) {
                        return "Project title is required.";
                      }
                      return null;
                    },
                    onChanged: (value) {
                      setState(() {
                        _projectTitle = value;
                      });
                    },
                  ),
                  const SizedBox(height: 20),

                  // Project Description
                  TextFormField(
                    decoration: const InputDecoration(
                      labelText: "Project Description",
                      border: OutlineInputBorder(),
                    ),
                    initialValue: _projectDescription,
                    maxLines: 3,
                    validator: (value) {
                      if (value == null || value.trim().isEmpty) {
                        return "Project description is required.";
                      }
                      return null;
                    },
                    onChanged: (value) {
                      setState(() {
                        _projectDescription = value;
                      });
                    },
                  ),
                  const SizedBox(height: 20),

                  // File Picker
                  Row(
                    children: [
                      ElevatedButton(
                        onPressed: _pickFile,
                        child: const Text("Browse..."),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          _file?.name ?? "No file selected.",
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(color: Colors.grey),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 20),

                  // Submit Button
                  ElevatedButton(
                    onPressed: _isSubmitting ? null : _submitForm,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16.0),
                      minimumSize: const Size(double.infinity, 50),
                    ),
                    child: Text(
                      _isSubmitting ? "Creating..." : "Create Project",
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
