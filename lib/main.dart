import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const QuranDatabaseApp());
}

class QuranDatabaseApp extends StatelessWidget {
  const QuranDatabaseApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'قاعدة بيانات القرآن الكريم',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.green,
        fontFamily: 'Arial', // يمكن تغييرها لخط عربي أفضل
        textTheme: const TextTheme(
          bodyLarge: TextStyle(fontSize: 16),
          bodyMedium: TextStyle(fontSize: 14),
        ),
        // إعدادات للنصوص العربية
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const HomeScreen(),
      // إعداد اتجاه النص للعربية
      builder: (context, child) {
        return Directionality(
          textDirection: TextDirection.rtl,
          child: child!,
        );
      },
    );
  }
}
