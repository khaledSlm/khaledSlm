# تعليمات إعداد وتشغيل تطبيق قاعدة بيانات القرآن الكريم

## المتطلبات الأساسية

### 1. تثبيت Flutter
```bash
# تحميل Flutter SDK من الموقع الرسمي
# https://flutter.dev/docs/get-started/install

# التحقق من التثبيت
flutter doctor
```

### 2. إعداد بيئة التطوير

#### للأندرويد:
- تثبيت Android Studio
- تثبيت Android SDK
- إنشاء محاكي Android أو توصيل جهاز حقيقي

#### للكمبيوتر:
- **Windows**: تثبيت Visual Studio مع C++ tools
- **Linux**: تثبيت المكتبات المطلوبة
- **macOS**: تثبيت Xcode

## خطوات التشغيل

### 1. تحضير المشروع
```bash
# الانتقال إلى مجلد المشروع
cd quran_database_app

# تثبيت المكتبات
flutter pub get

# التحقق من عدم وجود مشاكل
flutter doctor
```

### 2. تشغيل التطبيق

#### على الأندرويد:
```bash
# عرض الأجهزة المتاحة
flutter devices

# تشغيل على الأندرويد
flutter run
```

#### على الكمبيوتر:
```bash
# Windows
flutter run -d windows

# Linux
flutter run -d linux

# macOS
flutter run -d macos
```

### 3. بناء التطبيق للإنتاج

#### Android APK:
```bash
flutter build apk --release
```

#### Android App Bundle:
```bash
flutter build appbundle --release
```

#### Windows:
```bash
flutter build windows --release
```

#### Linux:
```bash
flutter build linux --release
```

#### macOS:
```bash
flutter build macos --release
```

## استكشاف الأخطاء

### مشاكل شائعة:

1. **خطأ في pub get**:
   ```bash
   flutter clean
   flutter pub get
   ```

2. **مشاكل في المحاكي**:
   - تأكد من تشغيل المحاكي
   - تحقق من إعدادات USB debugging للأجهزة الحقيقية

3. **مشاكل في قاعدة البيانات**:
   - احذف التطبيق وأعد تثبيته لإعادة إنشاء قاعدة البيانات

4. **مشاكل في الخطوط العربية**:
   - تأكد من دعم النظام للخطوط العربية

## إضافة بيانات جديدة

لإضافة المزيد من بيانات القرآن:

1. افتح ملف `lib/database/database_helper.dart`
2. عدّل دالة `_insertSampleData`
3. أضف البيانات الجديدة بالتنسيق:
   ```dart
   {'word': 'الكلمة', 'count_in_quran': العدد, 'surah_name': 'اسم السورة', 'ayah_number': رقم_الآية}
   ```

## تخصيص التطبيق

### تغيير الألوان:
- عدّل ملف `lib/main.dart` في قسم `ThemeData`

### تغيير الخطوط:
- أضف ملفات الخطوط في مجلد `assets/fonts/`
- عدّل ملف `pubspec.yaml` لتضمين الخطوط

### تغيير الأيقونة:
- استبدل الملفات في `android/app/src/main/res/mipmap/`

## الدعم والمساعدة

إذا واجهت أي مشاكل:
1. تحقق من ملف `README.md`
2. راجع وثائق Flutter الرسمية
3. تأكد من تحديث Flutter إلى أحدث إصدار

```bash
flutter upgrade
```

## ملاحظات مهمة

- التطبيق يحتوي على بيانات تجريبية محدودة
- لاستخدام حقيقي، يجب إضافة قاعدة بيانات شاملة لجميع كلمات القرآن
- يمكن تحسين الأداء بإضافة فهرسة لقاعدة البيانات
- يُنصح بإضافة نسخ احتياطي لقاعدة البيانات
