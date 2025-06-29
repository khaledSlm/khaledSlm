class QuranWord {
  final int? id;
  final String word;
  final int countInQuran;
  final String surahName;
  final int ayahNumber;

  QuranWord({
    this.id,
    required this.word,
    required this.countInQuran,
    required this.surahName,
    required this.ayahNumber,
  });

  // تحويل من Map إلى Object
  factory QuranWord.fromMap(Map<String, dynamic> map) {
    return QuranWord(
      id: map['id'],
      word: map['word'],
      countInQuran: map['count_in_quran'],
      surahName: map['surah_name'],
      ayahNumber: map['ayah_number'],
    );
  }

  // تحويل من Object إلى Map
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'word': word,
      'count_in_quran': countInQuran,
      'surah_name': surahName,
      'ayah_number': ayahNumber,
    };
  }

  @override
  String toString() {
    return 'QuranWord{id: $id, word: $word, countInQuran: $countInQuran, surahName: $surahName, ayahNumber: $ayahNumber}';
  }
}
