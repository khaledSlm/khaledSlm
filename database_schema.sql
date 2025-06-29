-- مخطط قاعدة بيانات القرآن الكريم
-- Database Schema for Quran Database

-- إنشاء قاعدة البيانات
CREATE DATABASE IF NOT EXISTS quran_database;
USE quran_database;

-- جدول السور
CREATE TABLE IF NOT EXISTS surahs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    surah_number INT NOT NULL UNIQUE,
    surah_name_arabic VARCHAR(100) NOT NULL,
    surah_name_english VARCHAR(100),
    total_ayahs INT NOT NULL,
    revelation_place ENUM('مكية', 'مدنية') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول الآيات
CREATE TABLE IF NOT EXISTS ayahs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    surah_id INT NOT NULL,
    ayah_number INT NOT NULL,
    ayah_text TEXT NOT NULL,
    ayah_text_simple TEXT, -- نص مبسط بدون تشكيل
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (surah_id) REFERENCES surahs(id),
    UNIQUE KEY unique_ayah (surah_id, ayah_number)
);

-- جدول الكلمات
CREATE TABLE IF NOT EXISTS words (
    id INT PRIMARY KEY AUTO_INCREMENT,
    word_text VARCHAR(100) NOT NULL,
    word_root VARCHAR(50), -- الجذر
    word_type ENUM('اسم', 'فعل', 'حرف', 'أخرى'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_word (word_text)
);

-- جدول مواضع الكلمات في القرآن
CREATE TABLE IF NOT EXISTS word_occurrences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    word_id INT NOT NULL,
    surah_id INT NOT NULL,
    ayah_id INT NOT NULL,
    position_in_ayah INT NOT NULL, -- موضع الكلمة في الآية
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (surah_id) REFERENCES surahs(id),
    FOREIGN KEY (ayah_id) REFERENCES ayahs(id),
    INDEX idx_word_search (word_id),
    INDEX idx_surah_ayah (surah_id, ayah_id)
);

-- جدول إحصائيات الكلمات
CREATE TABLE IF NOT EXISTS word_statistics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    word_id INT NOT NULL,
    total_count INT NOT NULL DEFAULT 0,
    surah_count INT NOT NULL DEFAULT 0, -- عدد السور التي تحتوي على الكلمة
    first_occurrence_surah INT,
    first_occurrence_ayah INT,
    last_occurrence_surah INT,
    last_occurrence_ayah INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words(id),
    UNIQUE KEY unique_word_stats (word_id)
);

-- فهارس لتحسين الأداء
CREATE INDEX idx_ayah_text ON ayahs(ayah_text(100));
CREATE INDEX idx_word_text ON words(word_text);
CREATE INDEX idx_surah_name ON surahs(surah_name_arabic);

-- إدراج بيانات السور (أمثلة)
INSERT INTO surahs (surah_number, surah_name_arabic, surah_name_english, total_ayahs, revelation_place) VALUES
(1, 'الفاتحة', 'Al-Fatiha', 7, 'مكية'),
(2, 'البقرة', 'Al-Baqarah', 286, 'مدنية'),
(3, 'آل عمران', 'Aal-E-Imran', 200, 'مدنية'),
(4, 'النساء', 'An-Nisa', 176, 'مدنية'),
(5, 'المائدة', 'Al-Maidah', 120, 'مدنية'),
(6, 'الأنعام', 'Al-Anaam', 165, 'مكية'),
(7, 'الأعراف', 'Al-Araf', 206, 'مكية'),
(8, 'الأنفال', 'Al-Anfal', 75, 'مدنية'),
(9, 'التوبة', 'At-Tawbah', 129, 'مدنية'),
(10, 'يونس', 'Yunus', 109, 'مكية'),
(11, 'هود', 'Hud', 123, 'مكية'),
(12, 'يوسف', 'Yusuf', 111, 'مكية'),
(13, 'الرعد', 'Ar-Rad', 43, 'مدنية'),
(14, 'إبراهيم', 'Ibrahim', 52, 'مكية'),
(15, 'الحجر', 'Al-Hijr', 99, 'مكية');

-- إجراء مخزن لحساب إحصائيات الكلمة
DELIMITER //
CREATE PROCEDURE UpdateWordStatistics(IN word_id_param INT)
BEGIN
    DECLARE total_occurrences INT DEFAULT 0;
    DECLARE surah_count_val INT DEFAULT 0;
    DECLARE first_surah INT DEFAULT NULL;
    DECLARE first_ayah INT DEFAULT NULL;
    DECLARE last_surah INT DEFAULT NULL;
    DECLARE last_ayah INT DEFAULT NULL;
    
    -- حساب العدد الإجمالي
    SELECT COUNT(*) INTO total_occurrences
    FROM word_occurrences 
    WHERE word_id = word_id_param;
    
    -- حساب عدد السور
    SELECT COUNT(DISTINCT surah_id) INTO surah_count_val
    FROM word_occurrences 
    WHERE word_id = word_id_param;
    
    -- أول ظهور
    SELECT surah_id, ayah_id INTO first_surah, first_ayah
    FROM word_occurrences wo
    JOIN ayahs a ON wo.ayah_id = a.id
    WHERE wo.word_id = word_id_param
    ORDER BY wo.surah_id, a.ayah_number
    LIMIT 1;
    
    -- آخر ظهور
    SELECT surah_id, ayah_id INTO last_surah, last_ayah
    FROM word_occurrences wo
    JOIN ayahs a ON wo.ayah_id = a.id
    WHERE wo.word_id = word_id_param
    ORDER BY wo.surah_id DESC, a.ayah_number DESC
    LIMIT 1;
    
    -- تحديث الإحصائيات
    INSERT INTO word_statistics 
    (word_id, total_count, surah_count, first_occurrence_surah, first_occurrence_ayah, last_occurrence_surah, last_occurrence_ayah)
    VALUES 
    (word_id_param, total_occurrences, surah_count_val, first_surah, first_ayah, last_surah, last_ayah)
    ON DUPLICATE KEY UPDATE
    total_count = total_occurrences,
    surah_count = surah_count_val,
    first_occurrence_surah = first_surah,
    first_occurrence_ayah = first_ayah,
    last_occurrence_surah = last_surah,
    last_occurrence_ayah = last_ayah,
    updated_at = CURRENT_TIMESTAMP;
END //
DELIMITER ;

-- عرض للبحث السريع
CREATE VIEW word_search_view AS
SELECT 
    w.word_text,
    ws.total_count,
    ws.surah_count,
    s1.surah_name_arabic as first_surah_name,
    a1.ayah_number as first_ayah_number,
    s2.surah_name_arabic as last_surah_name,
    a2.ayah_number as last_ayah_number
FROM words w
LEFT JOIN word_statistics ws ON w.id = ws.word_id
LEFT JOIN surahs s1 ON ws.first_occurrence_surah = s1.id
LEFT JOIN ayahs a1 ON ws.first_occurrence_ayah = a1.id
LEFT JOIN surahs s2 ON ws.last_occurrence_surah = s2.id
LEFT JOIN ayahs a2 ON ws.last_occurrence_ayah = a2.id;
