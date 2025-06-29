@echo off
chcp 65001 >nul
echo ========================================
echo    تطبيق قاعدة بيانات القرآن الكريم
echo ========================================
echo.

echo التحقق من تثبيت Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python غير مثبت!
    echo يرجى تثبيت Python من: https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python مثبت بنجاح!
echo.

echo 🔄 بناء قاعدة البيانات (إذا لم تكن موجودة)...
python quran_database_builder.py

echo.
echo 🚀 تشغيل التطبيق...
python run_python_app.py

echo.
echo 👋 تم إغلاق التطبيق
pause
