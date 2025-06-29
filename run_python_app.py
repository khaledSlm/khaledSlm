#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق قاعدة بيانات القرآن الكريم - واجهة بسيطة
Simple Quran Database Application Interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
from quran_database_builder import QuranDatabaseBuilder

class QuranDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("قاعدة بيانات القرآن الكريم")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f8ff')
        
        # إعداد قاعدة البيانات
        self.db_builder = QuranDatabaseBuilder()
        self.setup_database()
        
        # إنشاء الواجهة
        self.create_widgets()
        
    def setup_database(self):
        """إعداد قاعدة البيانات"""
        try:
            # التحقق من وجود قاعدة البيانات
            import os
            if not os.path.exists("quran_database.db"):
                print("🔄 بناء قاعدة البيانات لأول مرة...")
                self.db_builder.build_database()
            else:
                print("✅ قاعدة البيانات موجودة")
                self.db_builder.connect_database()
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في إعداد قاعدة البيانات: {e}")
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # العنوان الرئيسي
        title_frame = tk.Frame(self.root, bg='#2e8b57', height=80)
        title_frame.pack(fill='x', padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="قاعدة بيانات القرآن الكريم",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#2e8b57'
        )
        title_label.pack(expand=True)
        
        # إطار البحث
        search_frame = tk.Frame(self.root, bg='#f0f8ff')
        search_frame.pack(fill='x', padx=20, pady=10)
        
        # تسمية حقل البحث
        search_label = tk.Label(
            search_frame,
            text="ادخل الكلمة للبحث:",
            font=('Arial', 14),
            bg='#f0f8ff'
        )
        search_label.pack(anchor='e', pady=5)
        
        # حقل البحث
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Arial', 14),
            width=40,
            justify='right'
        )
        self.search_entry.pack(pady=5)
        self.search_entry.bind('<Return>', lambda e: self.search_word())
        
        # زر البحث
        search_button = tk.Button(
            search_frame,
            text="🔍 بحث",
            font=('Arial', 14, 'bold'),
            bg='#2e8b57',
            fg='white',
            command=self.search_word,
            width=15
        )
        search_button.pack(pady=10)
        
        # إطار النتائج
        results_frame = tk.Frame(self.root, bg='#f0f8ff')
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # تسمية النتائج
        self.results_label = tk.Label(
            results_frame,
            text="النتائج ستظهر هنا",
            font=('Arial', 12),
            bg='#f0f8ff'
        )
        self.results_label.pack(anchor='e', pady=5)
        
        # منطقة عرض النتائج
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            font=('Arial', 11),
            wrap=tk.WORD,
            height=20,
            bg='white',
            relief='sunken',
            borderwidth=2
        )
        self.results_text.pack(fill='both', expand=True)
        
        # شريط الحالة
        self.status_bar = tk.Label(
            self.root,
            text="جاهز للبحث",
            relief='sunken',
            anchor='w',
            bg='#e0e0e0'
        )
        self.status_bar.pack(side='bottom', fill='x')
    
    def search_word(self):
        """تنفيذ البحث"""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            messagebox.showwarning("تحذير", "يرجى إدخال كلمة للبحث")
            return
        
        try:
            self.status_bar.config(text="جاري البحث...")
            self.root.update()
            
            # تنفيذ البحث
            results = self.db_builder.search_word(search_term)
            
            # عرض النتائج
            self.display_results(search_term, results)
            
            self.status_bar.config(text=f"تم العثور على {len(results)} نتيجة")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في البحث: {e}")
            self.status_bar.config(text="خطأ في البحث")
    
    def display_results(self, search_term, results):
        """عرض نتائج البحث"""
        # مسح النتائج السابقة
        self.results_text.delete(1.0, tk.END)
        
        if not results:
            self.results_label.config(text="لم يتم العثور على نتائج")
            self.results_text.insert(tk.END, f"لم يتم العثور على نتائج للكلمة: {search_term}\n\n")
            self.results_text.insert(tk.END, "تأكد من:\n")
            self.results_text.insert(tk.END, "• كتابة الكلمة بشكل صحيح\n")
            self.results_text.insert(tk.END, "• أن الكلمة موجودة في قاعدة البيانات\n")
            self.results_text.insert(tk.END, "• جرب البحث عن جزء من الكلمة\n")
            return
        
        # عرض عدد النتائج
        self.results_label.config(text=f"تم العثور على {len(results)} نتيجة للكلمة: {search_term}")
        
        # تجميع النتائج حسب الكلمة
        word_groups = {}
        for result in results:
            word = result['word']
            if word not in word_groups:
                word_groups[word] = {
                    'total_count': result['total_count'],
                    'occurrences': []
                }
            word_groups[word]['occurrences'].append(result)
        
        # عرض النتائج
        for word, data in word_groups.items():
            # عنوان الكلمة
            self.results_text.insert(tk.END, f"🔸 الكلمة: {word}\n", 'word_title')
            self.results_text.insert(tk.END, f"📊 عدد مرات الذكر في القرآن: {data['total_count']}\n\n", 'count')
            
            # المواضع
            self.results_text.insert(tk.END, "📍 المواضع:\n", 'locations_title')
            
            for i, occurrence in enumerate(data['occurrences'][:10], 1):  # أول 10 نتائج
                self.results_text.insert(tk.END, f"{i}. ", 'number')
                self.results_text.insert(tk.END, f"سورة {occurrence['surah_name']} - ", 'surah')
                self.results_text.insert(tk.END, f"آية {occurrence['ayah_number']}\n", 'ayah')
                
                # عرض جزء من النص
                ayah_text = occurrence['ayah_text']
                if len(ayah_text) > 100:
                    ayah_text = ayah_text[:100] + "..."
                self.results_text.insert(tk.END, f"   {ayah_text}\n\n", 'ayah_text')
            
            if len(data['occurrences']) > 10:
                remaining = len(data['occurrences']) - 10
                self.results_text.insert(tk.END, f"... و {remaining} موضع آخر\n\n", 'more')
            
            self.results_text.insert(tk.END, "─" * 60 + "\n\n")
        
        # تنسيق النص
        self.setup_text_tags()
    
    def setup_text_tags(self):
        """إعداد تنسيق النص"""
        self.results_text.tag_config('word_title', font=('Arial', 14, 'bold'), foreground='#2e8b57')
        self.results_text.tag_config('count', font=('Arial', 12, 'bold'), foreground='#1e90ff')
        self.results_text.tag_config('locations_title', font=('Arial', 12, 'bold'), foreground='#ff6347')
        self.results_text.tag_config('number', font=('Arial', 10, 'bold'))
        self.results_text.tag_config('surah', font=('Arial', 11, 'bold'), foreground='#8b4513')
        self.results_text.tag_config('ayah', font=('Arial', 11), foreground='#4682b4')
        self.results_text.tag_config('ayah_text', font=('Arial', 10), foreground='#2f4f4f')
        self.results_text.tag_config('more', font=('Arial', 10, 'italic'), foreground='#696969')

def main():
    """تشغيل التطبيق"""
    print("🚀 بدء تشغيل تطبيق قاعدة بيانات القرآن الكريم...")
    
    root = tk.Tk()
    app = QuranDatabaseApp(root)
    
    # تشغيل التطبيق
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n👋 تم إغلاق التطبيق")
    except Exception as e:
        print(f"❌ خطأ في التطبيق: {e}")

if __name__ == "__main__":
    main()
