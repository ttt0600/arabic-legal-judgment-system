# دليل النشر على GitHub
# GitHub Deployment Guide

## 📋 المحتويات / Contents

1. [الإعداد الأولي](#1-الإعداد-الأولي)
2. [إنشاء Repository](#2-إنشاء-repository)
3. [رفع المشروع](#3-رفع-المشروع)
4. [إعداد GitHub Pages](#4-إعداد-github-pages)
5. [إعداد GitHub Actions](#5-إعداد-github-actions)
6. [الأمان والحماية](#6-الأمان-والحماية)

---

## 1. الإعداد الأولي

### تثبيت Git

```bash
# تحقق من تثبيت Git
git --version

# إذا لم يكن مثبتاً:
# Windows: قم بتحميل من https://git-scm.com/
# Linux:
sudo apt install git

# Mac:
brew install git
```

### إعداد Git

```bash
# إعداد الاسم والبريد الإلكتروني
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# التحقق من الإعدادات
git config --list
```

---

## 2. إنشاء Repository على GitHub

### الطريقة 1: من واجهة GitHub

1. اذهب إلى https://github.com
2. اضغط على **"+"** → **"New repository"**
3. املأ البيانات:
   - **Repository name**: `arabic-legal-judgment-system`
   - **Description**: `نظام إدارة الأحكام القانونية العربية - Arabic Legal Judgment Management System`
   - **Public** or **Private**: اختر حسب الحاجة
   - ✅ **لا تختر** "Initialize with README" (لأن لدينا README بالفعل)
4. اضغط **"Create repository"**

### الطريقة 2: من GitHub CLI

```bash
# تثبيت GitHub CLI (اختياري)
# Windows: scoop install gh
# Mac: brew install gh
# Linux: sudo apt install gh

# تسجيل الدخول
gh auth login

# إنشاء repository
gh repo create arabic-legal-judgment-system --public --description "نظام إدارة الأحكام القانونية العربية"
```

---

## 3. رفع المشروع

### الخطوة 1: تهيئة Git في المشروع

```bash
# انتقل لمجلد المشروع
cd C:\Users\talfandi\arabic-legal-judgment-system

# تهيئة Git
git init

# إضافة الملفات
git add .

# أول Commit
git commit -m "Initial commit: نظام إدارة الأحكام القانونية العربية v2.0"
```

### الخطوة 2: ربط بـ GitHub

```bash
# استبدل YOUR_USERNAME باسم المستخدم الخاص بك
git remote add origin https://github.com/YOUR_USERNAME/arabic-legal-judgment-system.git

# التحقق من الربط
git remote -v
```

### الخطوة 3: رفع الكود

```bash
# رفع إلى branch main
git branch -M main
git push -u origin main
```

### إذا واجهت مشكلة المصادقة

```bash
# استخدم Personal Access Token بدلاً من كلمة المرور

# 1. اذهب إلى GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
# 2. اضغط "Generate new token (classic)"
# 3. اختر الصلاحيات: repo (كل الصلاحيات)
# 4. انسخ الـ Token

# 5. استخدمه في Push
git push -u origin main
# Username: your_username
# Password: paste_your_token_here
```

---

## 4. إعداد GitHub Pages (اختياري)

إذا أردت استضافة الواجهة الأمامية على GitHub Pages:

### الخطوة 1: إعداد Frontend للنشر

```bash
cd frontend

# تحديث vite.config.js
# أضف base: '/arabic-legal-judgment-system/'
```

```javascript
// vite.config.js
export default {
  base: '/arabic-legal-judgment-system/',
  // ... بقية الإعدادات
}
```

### الخطوة 2: بناء المشروع

```bash
npm run build
```

### الخطوة 3: رفع على GitHub Pages

```bash
# تثبيت gh-pages
npm install --save-dev gh-pages

# إضافة scripts في package.json
"scripts": {
  "predeploy": "npm run build",
  "deploy": "gh-pages -d dist"
}

# النشر
npm run deploy
```

### الخطوة 4: تفعيل GitHub Pages

1. اذهب إلى Repository → Settings → Pages
2. Source: اختر `gh-pages` branch
3. اضغط Save
4. سيكون الموقع متاح على: `https://YOUR_USERNAME.github.io/arabic-legal-judgment-system/`

---

## 5. إعداد GitHub Actions (CI/CD)

سيتم إنشاء workflow تلقائي للاختبار والنشر.

### الملفات موجودة بالفعل:
- `.github/workflows/ci.yml`
- `.github/workflows/deploy.yml`

لتفعيلها:

1. اذهب إلى Repository → Settings → Actions → General
2. تأكد من تفعيل Actions
3. عند كل Push، ستعمل الـ Actions تلقائياً

---

## 6. الأمان والحماية

### ⚠️ ملفات مهمة يجب عدم رفعها

تأكد من وجود هذه الملفات في `.gitignore`:

```bash
# تحقق من محتوى .gitignore
cat .gitignore

# يجب أن يحتوي على:
# .env
# venv/
# __pycache__/
# *.pyc
# node_modules/
# *.log
# *.db
# uploads/
```

### إذا رفعت .env بالخطأ

```bash
# احذفه من Git history
git rm --cached .env
git commit -m "Remove .env from git"
git push

# غيّر جميع كلمات المرور والمفاتيح فوراً!
```

### حماية الـ Secrets

1. اذهب إلى Repository → Settings → Secrets and variables → Actions
2. أضف Secrets:
   - `MYSQL_PASSWORD`
   - `JWT_SECRET_KEY`
   - `SECRET_KEY`

### تفعيل Branch Protection

1. Settings → Branches → Add rule
2. Branch name pattern: `main`
3. فعّل:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date

---

## 📝 الأوامر السريعة

### رفع تحديثات جديدة

```bash
# إضافة التغييرات
git add .

# Commit
git commit -m "وصف التحديث"

# رفع
git push
```

### إنشاء Branch جديد

```bash
# إنشاء branch للميزة الجديدة
git checkout -b feature/new-feature

# العمل على الميزة...

# رفع Branch
git push -u origin feature/new-feature

# إنشاء Pull Request من GitHub
```

### التحديث من GitHub

```bash
# جلب آخر التحديثات
git pull origin main
```

---

## 🎯 الخطوات التالية بعد النشر

1. ✅ أضف **README** badges:
   - Build status
   - Code coverage
   - License
   - Version

2. ✅ أنشئ **Releases**:
   - Repository → Releases → Create new release
   - Tag: v2.0.0
   - أضف notes عن التحديثات

3. ✅ فعّل **Issues** و **Discussions**

4. ✅ أضف **Topics**:
   - Settings → Topics
   - أضف: `arabic`, `legal`, `management-system`, `flask`, `react`

5. ✅ أنشئ **Wiki** للوثائق

6. ✅ أضف **LICENSE**

---

## 🔗 روابط مفيدة

- [GitHub Docs](https://docs.github.com)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## ✅ قائمة التحقق النهائية

قبل النشر، تأكد من:

- [ ] ملف `.gitignore` محدّث
- [ ] لا توجد ملفات حساسة (`.env`, passwords)
- [ ] README.md محدّث وواضح
- [ ] LICENSE موجود
- [ ] الكود يعمل بدون أخطاء
- [ ] الاختبارات تمر بنجاح
- [ ] التوثيق كامل
- [ ] Links في README تعمل
- [ ] Screenshots مضافة (اختياري)

---

<div align="center">

**🎉 مبروك! مشروعك الآن على GitHub 🎉**

</div>
