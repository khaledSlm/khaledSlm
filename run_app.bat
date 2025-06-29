@echo off
echo ========================================
echo    تطبيق قاعدة بيانات القرآن الكريم
echo ========================================
echo.

echo التحقق من تثبيت Flutter...
flutter --version >nul 2>&1
if %errorlevel% neq 0 (
    echo خطأ: Flutter غير مثبت!
    echo يرجى تثبيت Flutter أولاً من: https://flutter.dev
    echo.
    echo خطوات التثبيت:
    echo 1. اذهب إلى https://flutter.dev
    echo 2. اضغط على Get Started
    echo 3. اختر Windows
    echo 4. حمّل وثبّت Flutter SDK
    echo 5. أضف Flutter للمتغيرات البيئية
    echo.
    pause
    exit /b 1
)

echo Flutter مثبت بنجاح!
echo.

echo تحميل المكتبات المطلوبة...
flutter pub get
if %errorlevel% neq 0 (
    echo خطأ في تحميل المكتبات!
    pause
    exit /b 1
)

echo.
echo التحقق من الأجهزة المتاحة...
flutter devices

echo.
echo بدء تشغيل التطبيق...
echo اختر الجهاز المطلوب عند السؤال
echo.

flutter run

echo.
echo انتهى تشغيل التطبيق
pause
