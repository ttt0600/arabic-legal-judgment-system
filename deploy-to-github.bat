@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   نشر المشروع على GitHub
echo   GitHub Deployment Script
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git غير مثبت! يرجى تثبيته أولاً
    echo ❌ Git is not installed! Please install it first
    echo.
    echo 📥 قم بتحميل Git من: https://git-scm.com/
    pause
    exit /b 1
)

echo ✅ Git مثبت
echo.

REM Check if already initialized
if exist .git (
    echo ℹ️  Git مهيأ بالفعل
    echo.
) else (
    echo 📝 تهيئة Git...
    git init
    echo ✅ تمت التهيئة
    echo.
)

REM Configure git (optional)
echo 🔧 إعداد Git (اختياري)...
set /p username="أدخل اسمك (Enter your name): "
if not "%username%"=="" (
    git config user.name "%username%"
)

set /p email="أدخل بريدك الإلكتروني (Enter your email): "
if not "%email%"=="" (
    git config user.email "%email%"
)
echo.

REM Add all files
echo 📦 إضافة الملفات...
git add .
echo ✅ تمت الإضافة
echo.

REM Commit
echo 💾 إنشاء Commit...
git commit -m "Initial commit: نظام إدارة الأحكام القانونية العربية v2.0"
if %errorlevel% neq 0 (
    echo ⚠️  لا توجد تغييرات للـ commit أو تم عمل commit بالفعل
    echo.
)
echo.

REM Get GitHub repository URL
echo 🔗 ربط بـ GitHub Repository
echo.
echo يرجى إنشاء Repository جديد على GitHub أولاً:
echo 1. اذهب إلى https://github.com/new
echo 2. اسم Repository: arabic-legal-judgment-system
echo 3. لا تختر "Initialize with README"
echo 4. اضغط "Create repository"
echo.

set /p repourl="الصق رابط Repository (Paste repository URL): "
if "%repourl%"=="" (
    echo ❌ لم تدخل رابط Repository!
    pause
    exit /b 1
)

REM Check if remote already exists
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo ℹ️  Remote موجود بالفعل، سيتم تحديثه...
    git remote set-url origin %repourl%
) else (
    git remote add origin %repourl%
)

echo ✅ تم الربط بـ GitHub
echo.

REM Set main branch
echo 🌿 إعداد Branch الرئيسي...
git branch -M main
echo ✅ تم
echo.

REM Push to GitHub
echo 🚀 رفع المشروع إلى GitHub...
echo.
echo ⚠️  ستحتاج إلى:
echo    - اسم المستخدم (Username)
echo    - Personal Access Token (ليس كلمة المرور!)
echo.
echo 📌 للحصول على Token:
echo    1. GitHub → Settings → Developer settings
echo    2. Personal access tokens → Tokens (classic)
echo    3. Generate new token (classic)
echo    4. اختر صلاحية: repo (كل الصلاحيات)
echo    5. انسخ الـ Token
echo.
pause

git push -u origin main
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   🎉 تم النشر بنجاح!
    echo   🎉 Successfully Deployed!
    echo ========================================
    echo.
    echo ✅ المشروع الآن على GitHub
    echo 🔗 Repository: %repourl%
    echo.
    echo 📝 الخطوات التالية:
    echo    1. أضف وصف للـ Repository
    echo    2. أضف Topics (arabic, legal, flask, react)
    echo    3. فعّل Issues و Discussions
    echo    4. أنشئ أول Release (v2.0.0)
    echo.
) else (
    echo.
    echo ❌ فشل الرفع!
    echo.
    echo 💡 الأسباب المحتملة:
    echo    - خطأ في اسم المستخدم أو Token
    echo    - عدم وجود صلاحيات كافية للـ Token
    echo    - مشكلة في الاتصال بالإنترنت
    echo.
    echo 🔄 حاول مرة أخرى أو استخدم:
    echo    git push -u origin main
    echo.
)

pause
