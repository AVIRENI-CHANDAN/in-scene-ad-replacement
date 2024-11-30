import 'package:flutter/material.dart';
import 'package:mobile/theme/colors.dart';
import 'package:mobile/NavigationBar/navigationbar.dart';

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
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Header Section
            Container(
              color: AppColors.primary,
              padding: const EdgeInsets.symmetric(vertical: 40, horizontal: 20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Text(
                    "Elevate Your Videos with Seamless Logo Integration",
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: AppColors.accent,
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    "Transform ordinary scenes into dynamic branding opportunities.",
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 16, color: AppColors.accent),
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () {
                      Navigator.pushNamed(context, "/login");
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.accent,
                      foregroundColor: AppColors.primary,
                      padding: const EdgeInsets.symmetric(
                        vertical: 10,
                        horizontal: 20,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                    ),
                    child: const Text("Get Started Now"),
                  ),
                ],
              ),
            ),

            // Features Section
            Container(
              padding: const EdgeInsets.all(20),
              color: AppColors.secondary,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "Why Choose Our Video Enhancement Tool?",
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: AppColors.textPrimary,
                    ),
                  ),
                  const SizedBox(height: 10),
                  const FeatureListTile(
                    title: "Easy Logo Placement",
                    description:
                        "Upload your video and logo, select the scene, and let our tool handle the rest.",
                  ),
                  const FeatureListTile(
                    title: "Advanced Scene Replacement",
                    description:
                        "Replace screens or billboards with custom content, perfect for targeted placements.",
                  ),
                  const FeatureListTile(
                    title: "High-Quality Rendering",
                    description:
                        "Supports up to 4K resolution, preserving video quality.",
                  ),
                  const FeatureListTile(
                    title: "User-Friendly Interface",
                    description:
                        "No technical skills required, ideal for all users.",
                  ),
                  const FeatureListTile(
                    title: "Fast Processing",
                    description: "Get your video ready in minutes.",
                  ),
                ],
              ),
            ),

            // How It Works Section
            Container(
              color: Colors.grey[100],
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "How It Works",
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 10),
                  const StepListTile(
                    step: "1",
                    title: "Upload Your Video",
                    description: "Choose any video you want to enhance.",
                  ),
                  const StepListTile(
                    step: "2",
                    title: "Select the Scene",
                    description:
                        "Navigate to the scene or screen you want to modify.",
                  ),
                  const StepListTile(
                    step: "3",
                    title: "Add Your Logo",
                    description:
                        "Upload your branding or ad image, adjust size and position.",
                  ),
                  const StepListTile(
                    step: "4",
                    title: "Preview and Adjust",
                    description: "Watch a live preview and make any tweaks.",
                  ),
                  const StepListTile(
                    step: "5",
                    title: "Download and Share",
                    description:
                        "Export your video and share it across platforms.",
                  ),
                ],
              ),
            ),

            // Testimonials Section
            Container(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "What Our Users Are Saying",
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 10),
                  const TestimonialTile(
                    quote:
                        "This tool has revolutionized our marketing efforts. It's incredibly easy to use and the results are phenomenal!",
                    author: "Alex Martinez, Digital Marketer",
                  ),
                  const TestimonialTile(
                    quote:
                        "I was amazed at how quickly I could add our company logo to our promotional videos. Highly recommend!",
                    author: "Sarah Lee, Content Creator",
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

// Reusable Widget for Features List
class FeatureListTile extends StatelessWidget {
  final String title;
  final String description;

  const FeatureListTile({
    super.key,
    required this.title,
    required this.description,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.check_circle, color: AppColors.primary, size: 20),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 5),
                Text(description, style: const TextStyle(fontSize: 14)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// Reusable Widget for Steps List
class StepListTile extends StatelessWidget {
  final String step;
  final String title;
  final String description;

  const StepListTile({
    super.key,
    required this.step,
    required this.title,
    required this.description,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          CircleAvatar(
            backgroundColor: AppColors.primary,
            foregroundColor: AppColors.accent,
            child: Text(step),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 5),
                Text(description, style: const TextStyle(fontSize: 14)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// Reusable Widget for Testimonials
class TestimonialTile extends StatelessWidget {
  final String quote;
  final String author;

  const TestimonialTile({super.key, required this.quote, required this.author});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            "\"$quote\"",
            style: const TextStyle(fontSize: 16, fontStyle: FontStyle.italic),
          ),
          const SizedBox(height: 5),
          Text(
            author,
            style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }
}
