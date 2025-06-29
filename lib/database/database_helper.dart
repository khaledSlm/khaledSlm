import 'dart:async';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/quran_word.dart';

class DatabaseHelper {
  static final DatabaseHelper _instance = DatabaseHelper._internal();
  factory DatabaseHelper() => _instance;
  DatabaseHelper._internal();

  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    String path = join(await getDatabasesPath(), 'quran_database.db');
    return await openDatabase(
      path,
      version: 1,
      onCreate: _onCreate,
    );
  }

  Future<void> _onCreate(Database db, int version) async {
    await db.execute('''
      CREATE TABLE quran_words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        count_in_quran INTEGER NOT NULL,
        surah_name TEXT NOT NULL,
        ayah_number INTEGER NOT NULL
      )
    ''');

    // إدراج بيانات تجريبية
    await _insertSampleData(db);
  }

  Future<void> _insertSampleData(Database db) async {
    List<Map<String, dynamic>> sampleData = [
      {'word': 'الله', 'count_in_quran': 2699, 'surah_name': 'الفاتحة', 'ayah_number': 2},
      {'word': 'الله', 'count_in_quran': 2699, 'surah_name': 'البقرة', 'ayah_number': 7},
      {'word': 'الرحمن', 'count_in_quran': 57, 'surah_name': 'الفاتحة', 'ayah_number': 3},
      {'word': 'الرحيم', 'count_in_quran': 114, 'surah_name': 'الفاتحة', 'ayah_number': 3},
      {'word': 'الحمد', 'count_in_quran': 38, 'surah_name': 'الفاتحة', 'ayah_number': 2},
      {'word': 'رب', 'count_in_quran': 980, 'surah_name': 'الفاتحة', 'ayah_number': 2},
      {'word': 'العالمين', 'count_in_quran': 73, 'surah_name': 'الفاتحة', 'ayah_number': 2},
      {'word': 'الدين', 'count_in_quran': 92, 'surah_name': 'الفاتحة', 'ayah_number': 4},
      {'word': 'الصراط', 'count_in_quran': 45, 'surah_name': 'الفاتحة', 'ayah_number': 6},
      {'word': 'المستقيم', 'count_in_quran': 5, 'surah_name': 'الفاتحة', 'ayah_number': 6},
    ];

    for (var data in sampleData) {
      await db.insert('quran_words', data);
    }
  }

  // البحث عن كلمة
  Future<List<QuranWord>> searchWord(String word) async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      'quran_words',
      where: 'word LIKE ?',
      whereArgs: ['%$word%'],
    );

    return List.generate(maps.length, (i) {
      return QuranWord.fromMap(maps[i]);
    });
  }

  // إضافة كلمة جديدة
  Future<int> insertWord(QuranWord word) async {
    final db = await database;
    return await db.insert('quran_words', word.toMap());
  }

  // الحصول على جميع الكلمات
  Future<List<QuranWord>> getAllWords() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query('quran_words');

    return List.generate(maps.length, (i) {
      return QuranWord.fromMap(maps[i]);
    });
  }

  // حذف كلمة
  Future<void> deleteWord(int id) async {
    final db = await database;
    await db.delete(
      'quran_words',
      where: 'id = ?',
      whereArgs: [id],
    );
  }
}
