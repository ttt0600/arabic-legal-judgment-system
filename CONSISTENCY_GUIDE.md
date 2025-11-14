# 🔄 دليل الحفاظ على اتساق المشروع
# Project Consistency Maintenance Guide

## 📋 نظرة عامة / Overview

هذا الدليل يشرح كيفية الحفاظ على اتساق المشروع عبر جميع الملفات والتكوينات.

This guide explains how to maintain project consistency across all files and configurations.

---

## 🎯 ملفات الإعدادات المركزية / Central Configuration Files

### 1. project_config.json

هذا الملف يحتوي على جميع إعدادات المشروع في مكان واحد:

```json
{
  "github": {
    "username": "ttt0600",
    "repository": "arabic-legal-judgment-system",
    "url": "https://github.com/ttt0600/arabic-legal-judgment-system"
  },
  "project": {
    "name": "Arabic Legal Judgment System",
    "version": "2.0.0"
  },
  "urls": {
    "frontend": "http://localhost:3000",
    "backend": "http://localhost:5000",
    "api": "http://localhost:5000/api"
  }
}
```

---

## 🛠️ أدوات الاتساق / Consistency Tools

### 1. update_project.py

**الغرض**: تحديث جميع URLs والمراجع تلقائياً

**الاستخدام**:
```bash
python update_project.py
```

**ماذا يفعل**:
- ✅ يحدث ملفات README
- ✅ يحدث package.json
- ✅ يحدث وثائق النشر
- ✅ يحدث GitHub badges
- ✅ يتحقق من .env.example

### 2. consistency_checker.py

**الغرض**: فحص اتساق المشروع والإبلاغ عن المشاكل

**الاستخدام**:
```bash
python consistency_checker.py
```

**ماذا يفعل**:
- 🔍 يفحص جميع ملفات README
- 🔍 يفحص إعدادات Frontend و Backend
- 🔍 يفحص Docker files
- 🔍 يفحص GitHub workflows
- 📊 يعطي تقرير مفصل

### 3. run_update.bat (Windows)

**الغرض**: تشغيل التحديث بنقرة واحدة

**الاستخدام**:
```bash
run_update.bat
```

---

## 📁 الملفات التي يجب تحديثها معاً

عند تغيير أي إعداد، تأكد من تحديث هذه الملفات:

### إعدادات GitHub

| الملف | السطر/القسم | التحديث المطلوب |
|-------|-------------|-----------------|
| `README.md` | Badges, Links | GitHub username & repo |
| `README_COMPLETE.md` | All GitHub URLs | Full URLs |
| `package.json` | repository, bugs, homepage | GitHub URLs |
| `GITHUB_DEPLOYMENT.md` | Examples | GitHub username |
| `project_config.json` | github section | All GitHub info |

### إعدادات URLs

| الملف | المتغير | القيمة |
|-------|---------|--------|
| `frontend/src/services/api.js` | baseURL | `http://localhost:5000/api` |
| `frontend/vite.config.js` | proxy target | `http://localhost:5000` |
| `docker-compose.yml` | ports | `5000:5000`, `3000:80` |
| `.env.example` | URLs | All service URLs |

### إعدادات الإصدار

| الملف | الموقع | التنسيق |
|-------|--------|---------|
| `package.json` | version | `2.0.0` |
| `README.md` | Badge | `version-2.0-blue` |
| `project_config.json` | project.version | `2.0.0` |

---

## 🔄 سير عمل التحديث / Update Workflow

### عند تغيير GitHub Username/Repository

```bash
# 1. تحديث project_config.json
# عدّل github.username و github.repository

# 2. تشغيل سكريبت التحديث
python update_project.py

# 3. مراجعة التغييرات
git diff

# 4. Commit و Push
git add .
git commit -m "Update GitHub references"
git push
```

### عند تغيير URLs أو Ports

```bash
# 1. تحديث project_config.json
# عدّل urls و ports sections

# 2. تحديث .env.example
# عدّل القيم المتأثرة

# 3. تحديث frontend/src/services/api.js
# عدّل baseURL

# 4. تحديث docker-compose.yml
# عدّل ports mapping

# 5. تحديث README files
# عدّل جداول URLs

# 6. اختبر التغييرات
npm run dev  # Frontend
python app.py  # Backend

# 7. Commit
git add .
git commit -m "Update URLs and ports configuration"
git push
```

### عند إصدار نسخة جديدة

```bash
# 1. تحديث project_config.json
{
  "project": {
    "version": "2.1.0"
  }
}

# 2. تحديث package.json
{
  "version": "2.1.0"
}

# 3. تحديث README badges
![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)

# 4. إنشاء CHANGELOG.md entry

# 5. إنشاء Git tag
git tag -a v2.1.0 -m "Release version 2.1.0"
git push origin v2.1.0

# 6. إنشاء GitHub Release
```

---

## ✅ قائمة التحقق اليومية / Daily Checklist

قبل كل Commit، تحقق من:

- [ ] جميع URLs صحيحة ومتسقة
- [ ] لا توجد "YOUR_USERNAME" أو "your-repo" في الكود
- [ ] ملف .env غير موجود في Git
- [ ] جميع الإعدادات في project_config.json محدّثة
- [ ] README files متطابقة مع الواقع
- [ ] package.json يحتوي على المعلومات الصحيحة

---

## 🔍 الفحص اليدوي / Manual Check

### فحص سريع للـ URLs

```bash
# ابحث عن placeholders
grep -r "YOUR_USERNAME" .
grep -r "your-repo" .
grep -r "username/repo" .

# فحص GitHub URLs
grep -r "github.com" README*.md

# فحص localhost URLs
grep -r "localhost:" frontend/src/
```

### فحص إعدادات API

```bash
# Frontend
cat frontend/src/services/api.js | grep baseURL

# Backend
cat config.py | grep -E "HOST|PORT"

# Docker
cat docker-compose.yml | grep "ports:"
```

---

## 🚨 مشاكل شائعة وحلولها / Common Issues

### مشكلة: URLs غير صحيحة بعد التحديث

**الحل**:
```bash
# تشغيل المدقق
python consistency_checker.py

# تشغيل المحدث
python update_project.py

# مراجعة يدوية
git diff
```

### مشكلة: Frontend لا يتصل بـ Backend

**الحل**:
```bash
# 1. تحقق من إعدادات API
cat frontend/src/services/api.js

# 2. تحقق من CORS في Backend
cat app.py | grep CORS

# 3. تحقق من Port
netstat -ano | findstr :5000
```

### مشكلة: Docker containers لا تتواصل

**الحل**:
```bash
# 1. تحقق من network configuration
cat docker-compose.yml | grep network

# 2. تحقق من ports mapping
cat docker-compose.yml | grep ports

# 3. إعادة بناء containers
docker-compose down
docker-compose build
docker-compose up
```

---

## 📊 مراقبة الاتساق / Monitoring Consistency

### مؤشرات الصحة / Health Indicators

| المؤشر | الحالة الجيدة | التحقق |
|--------|---------------|---------|
| URLs | لا توجد placeholders | `grep -r "YOUR_" .` |
| Versions | متطابقة في جميع الملفات | Manual check |
| Ports | متسقة | Check configs |
| GitHub info | صحيحة | Visit URLs |

### تقرير صحة المشروع / Project Health Report

قم بتشغيل هذا بشكل دوري:

```bash
# التقرير الشامل
python consistency_checker.py > health_report.txt

# مراجعة التقرير
cat health_report.txt
```

---

## 🎯 أفضل الممارسات / Best Practices

### 1. استخدم project_config.json

✅ **افعل**:
```javascript
import config from '../../../project_config.json';
const apiUrl = config.urls.api;
```

❌ **لا تفعل**:
```javascript
const apiUrl = 'http://localhost:5000/api'; // Hard-coded
```

### 2. تحديثات منتظمة

```bash
# كل أسبوع
python consistency_checker.py

# قبل كل release
python update_project.py
git diff  # Review changes
```

### 3. توثيق التغييرات

عند تغيير أي إعداد:
```bash
git commit -m "Update [setting]: [old value] → [new value]
  
  Affected files:
  - file1
  - file2
  
  Reason: [why the change was made]"
```

### 4. اختبار بعد التحديث

```bash
# اختبر Backend
python app.py
curl http://localhost:5000/api/health

# اختبر Frontend
cd frontend
npm run dev
# افتح http://localhost:3000

# اختبر التكامل
# اختبر login, API calls, etc.
```

---

## 📝 Checklist قبل Push

```bash
# 1. تشغيل المدقق
python consistency_checker.py

# 2. مراجعة التغييرات
git status
git diff

# 3. التحقق من .gitignore
cat .gitignore | grep ".env"

# 4. اختبار محلي
python app.py &
cd frontend && npm run dev

# 5. إذا كان كل شيء OK
git add .
git commit -m "Your message"
git push
```

---

## 🆘 الحصول على المساعدة / Getting Help

إذا واجهت مشاكل في الاتساق:

1. **راجع هذا الدليل**
2. **شغّل consistency_checker.py**
3. **افتح Issue على GitHub** مع:
   - وصف المشكلة
   - ناتج consistency_checker.py
   - الخطوات لإعادة المشكلة

---

<div align="center">

**✅ الاتساق = مشروع صحي**

**Consistency = Healthy Project**

</div>
