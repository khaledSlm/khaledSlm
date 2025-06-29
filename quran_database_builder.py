#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
برنامج بناء قاعدة بيانات القرآن الكريم
Quran Database Builder

هذا البرنامج يقوم بـ:
1. قراءة نصوص القرآن الكريم
2. تحليل الكلمات وفهرستها
3. بناء قاعدة البيانات
4. حساب الإحصائيات
"""

import sqlite3
import json
import re
import os
from typing import List, Dict, Tuple
from collections import defaultdict
import requests

class QuranDatabaseBuilder:
    def __init__(self, db_path: str = "quran_database.db"):
        """
        تهيئة بناء قاعدة البيانات
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        
        # قاموس لتنظيف النصوص
        self.arabic_diacritics = [
            'ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ّ', 'ْ', 'ٰ', 'ٱ', 'ٖ', 'ٗ', '٘', 'ٙ', 'ٚ', 'ٛ', 'ٜ', 'ٝ', 'ٞ', 'ٟ'
        ]
        
    def connect_database(self):
        """الاتصال بقاعدة البيانات"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            print("✅ تم الاتصال بقاعدة البيانات بنجاح")
        except Exception as e:
            print(f"❌ خطأ في الاتصال بقاعدة البيانات: {e}")
            
    def create_tables(self):
        """إنشاء جداول قاعدة البيانات"""
        try:
            # جدول السور
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS surahs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    surah_number INTEGER NOT NULL UNIQUE,
                    surah_name_arabic TEXT NOT NULL,
                    surah_name_english TEXT,
                    total_ayahs INTEGER NOT NULL,
                    revelation_place TEXT NOT NULL
                )
            ''')
            
            # جدول الآيات
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS ayahs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    surah_id INTEGER NOT NULL,
                    ayah_number INTEGER NOT NULL,
                    ayah_text TEXT NOT NULL,
                    ayah_text_simple TEXT,
                    FOREIGN KEY (surah_id) REFERENCES surahs(id),
                    UNIQUE(surah_id, ayah_number)
                )
            ''')
            
            # جدول الكلمات
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word_text TEXT NOT NULL UNIQUE,
                    word_root TEXT,
                    word_type TEXT
                )
            ''')
            
            # جدول مواضع الكلمات
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS word_occurrences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word_id INTEGER NOT NULL,
                    surah_id INTEGER NOT NULL,
                    ayah_id INTEGER NOT NULL,
                    position_in_ayah INTEGER NOT NULL,
                    FOREIGN KEY (word_id) REFERENCES words(id),
                    FOREIGN KEY (surah_id) REFERENCES surahs(id),
                    FOREIGN KEY (ayah_id) REFERENCES ayahs(id)
                )
            ''')
            
            # جدول إحصائيات الكلمات
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS word_statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word_id INTEGER NOT NULL UNIQUE,
                    total_count INTEGER NOT NULL DEFAULT 0,
                    surah_count INTEGER NOT NULL DEFAULT 0,
                    first_occurrence_surah INTEGER,
                    first_occurrence_ayah INTEGER,
                    FOREIGN KEY (word_id) REFERENCES words(id)
                )
            ''')
            
            # إنشاء فهارس
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_word_text ON words(word_text)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_word_occurrences ON word_occurrences(word_id)')
            
            self.connection.commit()
            print("✅ تم إنشاء الجداول بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء الجداول: {e}")
    
    def clean_arabic_text(self, text: str) -> str:
        """تنظيف النص العربي من التشكيل"""
        for diacritic in self.arabic_diacritics:
            text = text.replace(diacritic, '')
        return text.strip()
    
    def extract_words(self, text: str) -> List[str]:
        """استخراج الكلمات من النص"""
        # إزالة التشكيل
        clean_text = self.clean_arabic_text(text)
        
        # تقسيم النص إلى كلمات
        words = re.findall(r'[\u0600-\u06FF]+', clean_text)
        
        # تنظيف الكلمات
        cleaned_words = []
        for word in words:
            word = word.strip()
            if len(word) > 0:
                cleaned_words.append(word)
                
        return cleaned_words
    
    def insert_sample_data(self):
        """إدراج بيانات تجريبية"""
        try:
            # بيانات السور
            surahs_data = [
                (1, 'الفاتحة', 'Al-Fatiha', 7, 'مكية'),
                (2, 'البقرة', 'Al-Baqarah', 286, 'مدنية'),
                (3, 'آل عمران', 'Aal-E-Imran', 200, 'مدنية'),
                (4, 'النساء', 'An-Nisa', 176, 'مدنية'),
                (5, 'المائدة', 'Al-Maidah', 120, 'مدنية'),
            ]
            
            for surah in surahs_data:
                self.cursor.execute('''
                    INSERT OR IGNORE INTO surahs 
                    (surah_number, surah_name_arabic, surah_name_english, total_ayahs, revelation_place)
                    VALUES (?, ?, ?, ?, ?)
                ''', surah)
            
            # آيات سورة الفاتحة
            fatiha_ayahs = [
                "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
                "الرَّحْمَٰنِ الرَّحِيمِ",
                "مَالِكِ يَوْمِ الدِّينِ",
                "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
                "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
                "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ"
            ]
            
            # إدراج آيات الفاتحة
            for i, ayah_text in enumerate(fatiha_ayahs, 1):
                self.cursor.execute('''
                    INSERT OR IGNORE INTO ayahs 
                    (surah_id, ayah_number, ayah_text, ayah_text_simple)
                    VALUES (1, ?, ?, ?)
                ''', (i, ayah_text, self.clean_arabic_text(ayah_text)))
            
            self.connection.commit()
            print("✅ تم إدراج البيانات التجريبية")
            
        except Exception as e:
            print(f"❌ خطأ في إدراج البيانات: {e}")
    
    def process_ayahs(self):
        """معالجة الآيات واستخراج الكلمات"""
        try:
            # جلب جميع الآيات
            self.cursor.execute('SELECT id, surah_id, ayah_number, ayah_text FROM ayahs')
            ayahs = self.cursor.fetchall()
            
            print(f"🔄 معالجة {len(ayahs)} آية...")
            
            for ayah_id, surah_id, ayah_number, ayah_text in ayahs:
                # استخراج الكلمات
                words = self.extract_words(ayah_text)
                
                for position, word in enumerate(words, 1):
                    # إدراج الكلمة إذا لم تكن موجودة
                    self.cursor.execute('''
                        INSERT OR IGNORE INTO words (word_text) VALUES (?)
                    ''', (word,))
                    
                    # جلب معرف الكلمة
                    self.cursor.execute('SELECT id FROM words WHERE word_text = ?', (word,))
                    word_id = self.cursor.fetchone()[0]
                    
                    # إدراج موضع الكلمة
                    self.cursor.execute('''
                        INSERT INTO word_occurrences 
                        (word_id, surah_id, ayah_id, position_in_ayah)
                        VALUES (?, ?, ?, ?)
                    ''', (word_id, surah_id, ayah_id, position))
            
            self.connection.commit()
            print("✅ تم معالجة الآيات واستخراج الكلمات")
            
        except Exception as e:
            print(f"❌ خطأ في معالجة الآيات: {e}")
    
    def calculate_statistics(self):
        """حساب إحصائيات الكلمات"""
        try:
            # جلب جميع الكلمات
            self.cursor.execute('SELECT id, word_text FROM words')
            words = self.cursor.fetchall()
            
            print(f"📊 حساب إحصائيات {len(words)} كلمة...")
            
            for word_id, word_text in words:
                # حساب العدد الإجمالي
                self.cursor.execute('''
                    SELECT COUNT(*) FROM word_occurrences WHERE word_id = ?
                ''', (word_id,))
                total_count = self.cursor.fetchone()[0]
                
                # حساب عدد السور
                self.cursor.execute('''
                    SELECT COUNT(DISTINCT surah_id) FROM word_occurrences WHERE word_id = ?
                ''', (word_id,))
                surah_count = self.cursor.fetchone()[0]
                
                # أول ظهور
                self.cursor.execute('''
                    SELECT surah_id, ayah_id FROM word_occurrences 
                    WHERE word_id = ? 
                    ORDER BY surah_id, ayah_id 
                    LIMIT 1
                ''', (word_id,))
                first_occurrence = self.cursor.fetchone()
                
                # إدراج الإحصائيات
                self.cursor.execute('''
                    INSERT OR REPLACE INTO word_statistics 
                    (word_id, total_count, surah_count, first_occurrence_surah, first_occurrence_ayah)
                    VALUES (?, ?, ?, ?, ?)
                ''', (word_id, total_count, surah_count, 
                     first_occurrence[0] if first_occurrence else None,
                     first_occurrence[1] if first_occurrence else None))
            
            self.connection.commit()
            print("✅ تم حساب الإحصائيات")
            
        except Exception as e:
            print(f"❌ خطأ في حساب الإحصائيات: {e}")
    
    def search_word(self, word: str) -> List[Dict]:
        """البحث عن كلمة"""
        try:
            self.cursor.execute('''
                SELECT 
                    w.word_text,
                    ws.total_count,
                    s.surah_name_arabic,
                    a.ayah_number,
                    a.ayah_text
                FROM words w
                JOIN word_statistics ws ON w.id = ws.word_id
                JOIN word_occurrences wo ON w.id = wo.word_id
                JOIN surahs s ON wo.surah_id = s.id
                JOIN ayahs a ON wo.ayah_id = a.id
                WHERE w.word_text LIKE ?
                ORDER BY s.surah_number, a.ayah_number
            ''', (f'%{word}%',))
            
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    'word': row[0],
                    'total_count': row[1],
                    'surah_name': row[2],
                    'ayah_number': row[3],
                    'ayah_text': row[4]
                })
            
            return results
            
        except Exception as e:
            print(f"❌ خطأ في البحث: {e}")
            return []
    
    def build_database(self):
        """بناء قاعدة البيانات الكاملة"""
        print("🚀 بدء بناء قاعدة بيانات القرآن الكريم...")
        
        self.connect_database()
        self.create_tables()
        self.insert_sample_data()
        self.process_ayahs()
        self.calculate_statistics()
        
        print("✅ تم بناء قاعدة البيانات بنجاح!")
        
        # عرض إحصائيات
        self.cursor.execute('SELECT COUNT(*) FROM words')
        word_count = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM ayahs')
        ayah_count = self.cursor.fetchone()[0]
        
        print(f"📊 الإحصائيات:")
        print(f"   - عدد الكلمات: {word_count}")
        print(f"   - عدد الآيات: {ayah_count}")
    
    def close_connection(self):
        """إغلاق الاتصال"""
        if self.connection:
            self.connection.close()
            print("🔒 تم إغلاق الاتصال بقاعدة البيانات")

def main():
    """الدالة الرئيسية"""
    builder = QuranDatabaseBuilder()
    
    try:
        # بناء قاعدة البيانات
        builder.build_database()
        
        # تجربة البحث
        print("\n🔍 تجربة البحث:")
        results = builder.search_word("الله")
        print(f"نتائج البحث عن 'الله': {len(results)} نتيجة")
        
        if results:
            print("أول 3 نتائج:")
            for i, result in enumerate(results[:3], 1):
                print(f"{i}. {result['surah_name']} - آية {result['ayah_number']}")
                print(f"   العدد الإجمالي: {result['total_count']}")
                print(f"   النص: {result['ayah_text'][:50]}...")
                print()
        
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
    
    finally:
        builder.close_connection()

if __name__ == "__main__":
    main()
