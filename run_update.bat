@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   تحديث المشروع تلقائياً
echo   Automatic Project Update
echo ========================================
echo.

python update_project.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   ✅ تم التحديث بنجاح!
    echo   ✅ Update Complete!
    echo ========================================
    echo.
    echo 📝 الخطوات التالية:
    echo    1. git diff - لمراجعة التغييرات
    echo    2. git add . - لإضافة التغييرات
    echo    3. git commit -m "Update URLs and references"
    echo    4. git push - لرفع التحديثات
    echo.
) else (
    echo.
    echo ❌ حدث خطأ في التحديث
    echo.
)

pause
