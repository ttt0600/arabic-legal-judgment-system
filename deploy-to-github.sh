#!/bin/bash

echo ""
echo "========================================"
echo "  نشر المشروع على GitHub"
echo "  GitHub Deployment Script"
echo "========================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git غير مثبت! يرجى تثبيته أولاً"
    echo "❌ Git is not installed! Please install it first"
    echo ""
    echo "📥 Ubuntu/Debian: sudo apt install git"
    echo "📥 Mac: brew install git"
    exit 1
fi

echo "✅ Git مثبت"
echo ""

# Check if already initialized
if [ -d .git ]; then
    echo "ℹ️  Git مهيأ بالفعل"
    echo ""
else
    echo "📝 تهيئة Git..."
    git init
    echo "✅ تمت التهيئة"
    echo ""
fi

# Configure git (optional)
echo "🔧 إعداد Git (اختياري)..."
read -p "أدخل اسمك (Enter your name): " username
if [ ! -z "$username" ]; then
    git config user.name "$username"
fi

read -p "أدخل بريدك الإلكتروني (Enter your email): " email
if [ ! -z "$email" ]; then
    git config user.email "$email"
fi
echo ""

# Add all files
echo "📦 إضافة الملفات..."
git add .
echo "✅ تمت الإضافة"
echo ""

# Commit
echo "💾 إنشاء Commit..."
git commit -m "Initial commit: نظام إدارة الأحكام القانونية العربية v2.0"
echo ""

# Get GitHub repository URL
echo "🔗 ربط بـ GitHub Repository"
echo ""
echo "يرجى إنشاء Repository جديد على GitHub أولاً:"
echo "1. اذهب إلى https://github.com/new"
echo "2. اسم Repository: arabic-legal-judgment-system"
echo "3. لا تختر \"Initialize with README\""
echo "4. اضغط \"Create repository\""
echo ""

read -p "الصق رابط Repository (Paste repository URL): " repourl

if [ -z "$repourl" ]; then
    echo "❌ لم تدخل رابط Repository!"
    exit 1
fi

# Check if remote already exists
if git remote get-url origin &> /dev/null; then
    echo "ℹ️  Remote موجود بالفعل، سيتم تحديثه..."
    git remote set-url origin "$repourl"
else
    git remote add origin "$repourl"
fi

echo "✅ تم الربط بـ GitHub"
echo ""

# Set main branch
echo "🌿 إعداد Branch الرئيسي..."
git branch -M main
echo "✅ تم"
echo ""

# Push to GitHub
echo "🚀 رفع المشروع إلى GitHub..."
echo ""
echo "⚠️  ستحتاج إلى:"
echo "   - اسم المستخدم (Username)"
echo "   - Personal Access Token (ليس كلمة المرور!)"
echo ""
echo "📌 للحصول على Token:"
echo "   1. GitHub → Settings → Developer settings"
echo "   2. Personal access tokens → Tokens (classic)"
echo "   3. Generate new token (classic)"
echo "   4. اختر صلاحية: repo (كل الصلاحيات)"
echo "   5. انسخ الـ Token"
echo ""
read -p "اضغط Enter للمتابعة..."

if git push -u origin main; then
    echo ""
    echo "========================================"
    echo "  🎉 تم النشر بنجاح!"
    echo "  🎉 Successfully Deployed!"
    echo "========================================"
    echo ""
    echo "✅ المشروع الآن على GitHub"
    echo "🔗 Repository: $repourl"
    echo ""
    echo "📝 الخطوات التالية:"
    echo "   1. أضف وصف للـ Repository"
    echo "   2. أضف Topics (arabic, legal, flask, react)"
    echo "   3. فعّل Issues و Discussions"
    echo "   4. أنشئ أول Release (v2.0.0)"
    echo ""
else
    echo ""
    echo "❌ فشل الرفع!"
    echo ""
    echo "💡 الأسباب المحتملة:"
    echo "   - خطأ في اسم المستخدم أو Token"
    echo "   - عدم وجود صلاحيات كافية للـ Token"
    echo "   - مشكلة في الاتصال بالإنترنت"
    echo ""
    echo "🔄 حاول مرة أخرى أو استخدم:"
    echo "   git push -u origin main"
    echo ""
fi
