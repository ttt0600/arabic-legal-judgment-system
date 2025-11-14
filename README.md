# نظام إدارة الأحكام القانونية العربية
# Arabic Legal Judgment Management System

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![RTL Support](https://img.shields.io/badge/RTL-Supported-orange.svg)
![Arabic](https://img.shields.io/badge/Language-Arabic-success.svg)

**نظام متكامل ومحسّن لإدارة الأحكام والقضايا القانونية مع دعم كامل للغة العربية**

[الميزات](#-الميزات) • [التثبيت](#-التثبيت-السريع) • [الوثائق الكاملة](README_COMPLETE.md) • [المساهمة](#-المساهمة)

</div>

---

## 🌟 نظرة عامة

نظام شامل لإدارة الأحكام القانونية والقضايا مصمم خصيصاً للبيئة العربية. يوفر أدوات حديثة لإدارة القضايا، الأحكام، المستندات، البحث المتقدم، والتقارير مع دعم كامل للغة العربية واتجاه النص RTL.

## ✨ الميزات الرئيسية

- 🏛️ **إدارة القضايا**: إنشاء وتتبع القضايا مع تصنيف متقدم
- ⚖️ **إدارة الأحكام**: توثيق الأحكام القانونية مع ربطها بالقضايا
- 📄 **إدارة المستندات**: رفع وتخزين المستندات بأمان
- 🔍 **بحث ذكي**: بحث متقدم مع معالجة ذكية للنصوص العربية
- 📊 **تقارير شاملة**: إحصائيات ورسوم بيانية تفاعلية
- 👥 **إدارة المستخدمين**: نظام أدوار وصلاحيات متكامل
- 🌐 **دعم عربي كامل**: واجهة RTL ومعالجة نصوص عربية محسّنة
- 🚀 **أداء عالي**: يدعم ملايين السجلات بكفاءة

## 💻 التقنيات المستخدمة

**Backend**: Flask, SQLAlchemy, MySQL/SQLite, JWT, Arabic-Reshaper  
**Frontend**: React 18, Material-UI, React Router, Axios  
**Database**: MySQL 8.0+, SQLite 3.x, Redis (اختياري)

## ⚡ التثبيت السريع

### الطريقة 1: التلقائية (موصى بها)

```bash
git clone https://github.com/ttt0600/arabic-legal-judgment-system.git
cd arabic-legal-judgment-system
python setup.py
```

### الطريقة 2: اليدوية

```bash
# Backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env
python database/init_db.py
python app.py

# Frontend (نافذة جديدة)
cd frontend
npm install
npm run dev
```

### الطريقة 3: Docker

```bash
docker-compose up -d
```

## 🔗 الوصول للنظام

| الخدمة | الرابط | الوصف |
|--------|---------|-------|
| 🌐 الواجهة الأمامية | http://localhost:3000 | واجهة المستخدم |
| 🔌 API | http://localhost:5000/api | Backend API |
| 📊 قارئ CSV | http://localhost:5000/csv-reader-full | رفع البيانات |

**بيانات الدخول الافتراضية**:
- اسم المستخدم: `admin`
- كلمة المرور: `admin123`

⚠️ **مهم**: غيّر كلمة المرور فوراً في الإنتاج!

## 📚 الوثائق

- 📖 [الوثائق الكاملة](README_COMPLETE.md) - دليل شامل مفصل
- 🚀 [دليل النشر](docs/deployment.md) - تعليمات النشر
- 🔌 [توثيق API](docs/api.md) - مرجع API الكامل
- 🤝 [دليل المساهمة](docs/contributing.md) - كيفية المساهمة
- 🔧 [استكشاف الأخطاء](docs/troubleshooting.md) - حل المشاكل

## 🎯 الاستخدام السريع

### تشغيل الخادم المحسّن (للبيانات الكبيرة)

```bash
python optimized_server.py
```

### تحميل بيانات من CSV

```bash
# 1. شغّل الخادم
python optimized_server.py

# 2. افتح قارئ البيانات
# http://localhost:5000/csv-reader-full

# 3. اسحب ملف CSV وحمّل البيانات
```

## 📁 البنية الهيكلية

```
arabic-legal-judgment-system/
├── app.py                    # التطبيق الرئيسي
├── optimized_server.py       # خادم محسّن
├── models.py                 # نماذج البيانات
├── config.py                 # الإعدادات
├── database/                 # قاعدة البيانات
├── frontend/                 # الواجهة الأمامية
├── utils/                    # أدوات مساعدة
├── docs/                     # الوثائق
└── tests/                    # الاختبارات
```

## 🔌 API أمثلة

### تسجيل الدخول

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### جلب القضايا

```bash
curl -X GET "http://localhost:5000/api/cases?page=1&per_page=20" \
  -H "Authorization: Bearer <token>"
```

## 🚀 النشر

### على خادم Linux

```bash
# تثبيت المتطلبات
sudo apt update
sudo apt install python3 python3-venv mysql-server nginx

# إعداد المشروع
git clone <repo>
cd arabic-legal-judgment-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# إعداد قاعدة البيانات
python database/init_db.py

# تشغيل مع Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### مع Docker

```bash
docker-compose build
docker-compose up -d
```

## 🔒 الأمان

- ✅ JWT للمصادقة
- ✅ تشفير كلمات المرور (Bcrypt)
- ✅ RBAC (نظام الأدوار)
- ✅ حماية من SQL Injection
- ✅ CORS Protection
- ✅ سجل مراجعة شامل

## 🧪 الاختبار

```bash
# Backend
pytest
pytest --cov

# Frontend
cd frontend
npm test
```

## 🤝 المساهمة

نرحب بجميع المساهمات! 

1. Fork المشروع
2. أنشئ فرع للميزة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'إضافة ميزة رائعة'`)
4. Push للفرع (`git push origin feature/AmazingFeature`)
5. افتح Pull Request

راجع [دليل المساهمة](docs/contributing.md) للتفاصيل.

## 🐛 الإبلاغ عن الأخطاء

وجدت خطأ؟ [افتح Issue](https://github.com/ttt0600/arabic-legal-judgment-system/issues)

## 📞 الدعم

- 📧 البريد: support@legal-system.com
- 💬 المناقشات: [GitHub Discussions](https://github.com/ttt0600/arabic-legal-judgment-system/discussions)
- 📚 الوثائق: [Wiki](https://github.com/ttt0600/arabic-legal-judgment-system/wiki)

## 🗺️ خريطة الطريق

- [x] v1.0 - النظام الأساسي
- [x] v2.0 - التحسينات والأداء
- [ ] v2.5 - تطبيق الموبايل
- [ ] v3.0 - الذكاء الاصطناعي

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع [LICENSE](LICENSE)

## 🙏 الشكر والتقدير

- المجتمع العربي للبرمجيات مفتوحة المصدر
- مكتبة Arabic Reshaper
- مجتمع Material-UI
- جميع المساهمين

---

<div align="center">

**صُنع بـ ❤️ للمجتمع القانوني العربي**

**Made with ❤️ for the Arabic Legal Community**

<br>

⭐ إذا أعجبك المشروع، أعطه نجمة! ⭐

<br>

![Arabic](https://img.shields.io/badge/🇸🇦-Arabic-success.svg)
![Open Source](https://img.shields.io/badge/💚-Open%20Source-success.svg)
![Community](https://img.shields.io/badge/👥-Community-blue.svg)

</div>
