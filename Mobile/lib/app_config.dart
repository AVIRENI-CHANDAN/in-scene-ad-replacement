class AppConfig {
  // Localhost for development (use 10.0.2.2 for Android emulator)
  static const String developmentBaseUrl = "http://10.0.2.2:5000";
  static const String productionBaseUrl = "https://your-production-backend-url";

  // Base URL dynamically selected based on the environment
  static String get baseUrl {
    const bool isProduction = bool.fromEnvironment("dart.vm.product");
    return isProduction ? productionBaseUrl : developmentBaseUrl;
  }
}
