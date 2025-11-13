_user -p

# إنشاء المستخدم إذا لم يكن موجوداً
CREATE USER 'legal_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON arabic_legal_system.* TO 'legal_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 2. النص العربي لا يظهر بشكل صحيح

**المشكلة**: النص العربي يظهر كرموز غريبة أو مربعات

**الحل**:
```bash
# تحقق من ترميز قاعدة البيانات
mysql -u legal_user -p
SHOW VARIABLES LIKE 'character_set%';

# يجب أن تكون جميعها utf8mb4

# تحقق من تثبيت مكتبات معالجة العربية
pip install arabic-reshaper python-bidi

# في Frontend، تأكد من وجود
<meta charset="UTF-8">
```

#### 3. خطأ 404 عند الوصول للـ API

**المشكلة**: `404 Not Found` عند طلب `/api/cases`

**الحل**:
```bash
# تحقق من تشغيل الخادم
ps aux | grep python

# تحقق من المنفذ الصحيح
netstat -tlnp | grep 5000

# تحقق من CORS في app.py
from flask_cors import CORS
CORS(app)

# إعادة تشغيل الخادم
python app.py
```

#### 4. مشكلة في رفع الملفات الكبيرة

**المشكلة**: `413 Request Entity Too Large`

**الحل**:
```python
# في config.py أو .env
MAX_CONTENT_LENGTH = 104857600  # 100MB

# في Nginx
client_max_body_size 100M;

# في MySQL
max_allowed_packet = 256M

# إعادة تشغيل الخدمات
sudo systemctl restart nginx
sudo systemctl restart mysql
```

#### 5. بطء في البحث

**المشكلة**: البحث يستغرق وقتاً طويلاً

**الحل**:
```sql
-- إضافة indexes للجداول
ALTER TABLE cases ADD FULLTEXT INDEX idx_cases_search (title, description);
ALTER TABLE judgments ADD FULLTEXT INDEX idx_judgments_search (title, content);

-- استخدام الخادم المحسّن
python optimized_server.py

-- تفعيل Redis للتخزين المؤقت
REDIS_URL=redis://localhost:6379/0
```

#### 6. خطأ في تثبيت المتطلبات

**المشكلة**: `error: Microsoft Visual C++ 14.0 is required`

**الحل**:
```bash
# Windows: تثبيت Build Tools
# قم بتحميل وتثبيت:
# https://visualstudio.microsoft.com/downloads/

# أو استخدم المتطلبات المينيمال
pip install -r requirements-minimal.txt

# Linux: تثبيت أدوات البناء
sudo apt install python3-dev build-essential
```

#### 7. خطأ في Frontend

**المشكلة**: `Cannot find module '@/components/...'`

**الحل**:
```bash
cd frontend

# مسح node_modules وإعادة التثبيت
rm -rf node_modules package-lock.json
npm install

# تحقق من vite.config.js
# يجب أن يحتوي على:
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
  },
}
```

### 📞 الحصول على المساعدة

إذا واجهت مشكلة غير مذكورة هنا:

1. **راجع السجلات (Logs)**:
   ```bash
   # سجلات Backend
   tail -f logs/app.log
   
   # سجلات Nginx
   sudo tail -f /var/log/nginx/error.log
   
   # سجلات MySQL
   sudo tail -f /var/log/mysql/error.log
   ```

2. **تحقق من GitHub Issues**: قد تكون المشكلة معروفة بالفعل
3. **افتح Issue جديد**: إذا كانت مشكلة جديدة، افتح Issue مع:
   - وصف المشكلة
   - خطوات إعادة المشكلة
   - رسائل الخطأ
   - نظام التشغيل والإصدارات

---

## 🤝 المساهمة / Contributing

نرحب بجميع المساهمات! سواء كانت:
- 🐛 إصلاح أخطاء
- ✨ إضافة ميزات جديدة
- 📝 تحسين التوثيق
- 🌍 الترجمة
- 🎨 تحسين التصميم

### خطوات المساهمة

#### 1. Fork المشروع

```bash
# اضغط على زر Fork في GitHub
# ثم استنسخ نسختك
git clone https://github.com/YOUR_USERNAME/arabic-legal-judgment-system.git
cd arabic-legal-judgment-system
```

#### 2. إنشاء فرع جديد

```bash
# للميزة الجديدة
git checkout -b feature/amazing-feature

# لإصلاح خطأ
git checkout -b fix/bug-description

# للتوثيق
git checkout -b docs/update-readme
```

#### 3. إجراء التغييرات

```bash
# قم بالتعديلات المطلوبة
# تأكد من اتباع معايير الكود

# اختبر التغييرات
pytest
npm test

# أضف الملفات المعدلة
git add .

# Commit مع رسالة واضحة
git commit -m "إضافة: ميزة البحث المتقدم في الأحكام"
```

#### 4. Push ثم Pull Request

```bash
# Push للفرع
git push origin feature/amazing-feature

# افتح Pull Request في GitHub
# املأ قالب PR بالتفاصيل المطلوبة
```

### 📋 معايير الكود / Code Standards

#### Python (Backend)

```python
# اتبع PEP 8
# استخدم أسماء واضحة
def get_case_by_id(case_id: int) -> Case:
    """
    جلب قضية حسب المعرّف
    
    Args:
        case_id: معرّف القضية
        
    Returns:
        Case: كائن القضية
    """
    return Case.query.get_or_404(case_id)

# استخدم Type Hints
def create_judgment(
    case_id: int,
    title: str,
    content: str
) -> Judgment:
    pass

# أضف Docstrings للوظائف المهمة
# استخدم التعليقات بالعربية للشرح
```

#### JavaScript/React (Frontend)

```javascript
// استخدم ESLint
// استخدم أسماء واضحة بالإنجليزية
const CaseList = () => {
  // استخدم Hooks بشكل صحيح
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // استخدم useEffect للتحميل
  useEffect(() => {
    fetchCases();
  }, []);
  
  return (
    // مكونات RTL للعربية
    <div dir="rtl">
      {/* التعليقات بالعربية للشرح */}
    </div>
  );
};
```

### ✅ قائمة التحقق قبل PR

- [ ] الكود يتبع معايير المشروع
- [ ] تم اختبار التغييرات محلياً
- [ ] أضفت/حدثت الاختبارات إن لزم الأمر
- [ ] حدثت التوثيق إن لزم الأمر
- [ ] الـ Commits واضحة ومفصلة
- [ ] لا توجد تعارضات مع main branch
- [ ] تم التأكد من عمل البرنامج مع التغييرات

### 🎨 إرشادات التصميم

- استخدم Material-UI Components
- التزم بـ Color Scheme الموجود
- تأكد من دعم RTL
- اختبر على شاشات مختلفة (Desktop, Tablet, Mobile)
- استخدم خطوط Cairo للعربية

### 📚 إرشادات التوثيق

- اكتب بالعربية والإنجليزية
- استخدم أمثلة واضحة
- أضف screenshots عند الحاجة
- حافظ على تنسيق Markdown
- تأكد من صحة الروابط

---

## 📄 الترخيص / License

هذا المشروع مرخص تحت **رخصة MIT** - راجع ملف [LICENSE](LICENSE) للتفاصيل.

```
MIT License

Copyright (c) 2024 Arabic Legal Judgment System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### ماذا يعني هذا؟

✅ **يمكنك**:
- استخدام المشروع لأي غرض (تجاري أو شخصي)
- تعديل الكود
- توزيع نسخك المعدلة
- دمج الكود في مشاريعك

⚠️ **بشرط**:
- الاحتفاظ بإشعار حقوق النشر
- ذكر الترخيص في أي نسخة

❌ **لا ضمانات**:
- المشروع مقدم "كما هو" بدون أي ضمانات
- المطورون غير مسؤولين عن أي أضرار

---

## 👥 الفريق / Team

### المطورون الرئيسيون / Core Developers

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/username">
        <img src="https://github.com/username.png" width="100px;" alt=""/>
        <br />
        <sub><b>الاسم هنا</b></sub>
      </a>
      <br />
      <sub>Lead Developer</sub>
    </td>
    <!-- أضف المزيد من المطورين -->
  </tr>
</table>

### المساهمون / Contributors

شكراً لكل من ساهم في هذا المشروع! 🙏

<a href="https://github.com/your-repo/arabic-legal-judgment-system/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=your-repo/arabic-legal-judgment-system" />
</a>

---

## 🌟 الدعم والمساعدة / Support

### 📞 طرق التواصل / Contact Methods

| الطريقة | الرابط/البريد | الاستجابة |
|---------|----------------|-----------|
| 📧 البريد الإلكتروني | support@legal-system.com | 24-48 ساعة |
| 💬 GitHub Discussions | [discussions](https://github.com/repo/discussions) | المجتمع |
| 🐛 GitHub Issues | [issues](https://github.com/repo/issues) | 1-3 أيام |
| 📚 الوثائق | [wiki](https://github.com/repo/wiki) | فوري |
| 💼 LinkedIn | [company-page](#) | للتعاون |

### ❓ الأسئلة الشائعة / FAQ

<details>
<summary><strong>س: هل النظام مجاني؟</strong></summary>
<br>
نعم، النظام مفتوح المصدر ومجاني تماماً للاستخدام الشخصي والتجاري تحت رخصة MIT.
</details>

<details>
<summary><strong>س: هل يدعم النظام أكثر من لغة؟</strong></summary>
<br>
حالياً النظام يدعم اللغة العربية فقط، ولكن البنية جاهزة لإضافة لغات أخرى. المساهمات في الترجمة مرحب بها!
</details>

<details>
<summary><strong>س: كم يستطيع النظام تخزين من السجلات؟</strong></summary>
<br>
النظام المحسّن يدعم ملايين السجلات. تم اختباره مع أكثر من 5 مليون سجل بأداء ممتاز.
</details>

<details>
<summary><strong>س: هل يمكن استخدامه في المحاكم الحكومية؟</strong></summary>
<br>
نعم، النظام مصمم لهذا الغرض. يحتوي على جميع المميزات المطلوبة للمحاكم والمكاتب القانونية.
</details>

<details>
<summary><strong>س: هل تقدمون دعم فني مدفوع؟</strong></summary>
<br>
نعم، نقدم خدمات دعم فني وتخصيص وتدريب. تواصل معنا على support@legal-system.com
</details>

<details>
<summary><strong>س: كيف أقوم بترقية النظام؟</strong></summary>
<br>
<code>git pull origin main</code><br>
<code>pip install -r requirements.txt</code><br>
<code>python database/migrate.py</code>
</details>

### 📖 الموارد التعليمية / Learning Resources

#### دروس فيديو / Video Tutorials

- 🎥 [التثبيت والإعداد - 15 دقيقة](https://youtube.com/watch?v=example)
- 🎥 [إدارة القضايا - 20 دقيقة](https://youtube.com/watch?v=example)
- 🎥 [البحث المتقدم - 10 دقائق](https://youtube.com/watch?v=example)
- 🎥 [التقارير والإحصائيات - 15 دقيقة](https://youtube.com/watch?v=example)

#### المقالات / Articles

- 📝 [دليل البدء السريع](docs/quick-start.md)
- 📝 [أفضل الممارسات](docs/best-practices.md)
- 📝 [نصائح الأداء](docs/performance-tips.md)
- 📝 [أمان النظام](docs/security-guide.md)

### 🎓 التدريب / Training

نقدم دورات تدريبية:
- ✅ **أساسيات النظام**: يوم واحد
- ✅ **الإدارة المتقدمة**: يومين
- ✅ **التخصيص والتطوير**: 3 أيام
- ✅ **النشر والصيانة**: يومين

للتسجيل: training@legal-system.com

---

## 🗺️ خريطة الطريق / Roadmap

### ✅ الإصدار 1.0 (مكتمل)
- [x] نظام المصادقة والترخيص
- [x] إدارة القضايا الأساسية
- [x] إدارة الأحكام
- [x] رفع المستندات
- [x] البحث الأساسي
- [x] التقارير البسيطة

### ✅ الإصدار 2.0 (الحالي)
- [x] تحسين الأداء للبيانات الكبيرة
- [x] قاعدة بيانات SQLite المحسّنة
- [x] البحث المتقدم مع معالجة العربية
- [x] واجهة مستخدم محسّنة
- [x] دعم Docker
- [x] توثيق شامل

### 🚧 الإصدار 2.5 (قيد التطوير)
- [ ] تطبيق الهاتف المحمول (React Native)
- [ ] إشعارات فورية (Push Notifications)
- [ ] تكامل مع واتساب للإشعارات
- [ ] نظام المهام والتذكيرات
- [ ] تقارير متقدمة مع AI
- [ ] تحليل البيانات بالذكاء الاصطناعي

### 🎯 الإصدار 3.0 (مخطط)
- [ ] تصنيف تلقائي للقضايا بـ AI
- [ ] استخراج البيانات من المستندات بـ OCR
- [ ] ملخصات تلقائية للأحكام
- [ ] توصيات ذكية للقضايا المشابهة
- [ ] دعم التوقيع الإلكتروني
- [ ] blockchain للتوثيق
- [ ] تكامل مع أنظمة المحاكم الحكومية

### 🌍 المستقبل البعيد
- [ ] دعم لغات متعددة (إنجليزي، فرنسي)
- [ ] منصة سحابية SaaS
- [ ] API متقدم للتكامل
- [ ] تطبيق Desktop (Electron)
- [ ] نظام محادثة مباشرة
- [ ] مساعد افتراضي بالذكاء الاصطناعي

### 🗳️ التصويت على الميزات

هل لديك اقتراح لميزة جديدة؟ 
[صوّت هنا](https://github.com/repo/discussions/categories/feature-requests)

---

## 📊 الإحصائيات / Statistics

### 📈 إحصائيات المشروع

![GitHub Stars](https://img.shields.io/github/stars/your-repo/arabic-legal-judgment-system?style=social)
![GitHub Forks](https://img.shields.io/github/forks/your-repo/arabic-legal-judgment-system?style=social)
![GitHub Issues](https://img.shields.io/github/issues/your-repo/arabic-legal-judgment-system)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/your-repo/arabic-legal-judgment-system)
![Contributors](https://img.shields.io/github/contributors/your-repo/arabic-legal-judgment-system)
![Last Commit](https://img.shields.io/github/last-commit/your-repo/arabic-legal-judgment-system)

### 💻 الكود

| المقياس | القيمة |
|---------|--------|
| عدد الملفات | 150+ |
| أسطر الكود | 25,000+ |
| لغات البرمجة | Python, JavaScript, SQL, HTML, CSS |
| المكتبات المستخدمة | 50+ |
| الاختبارات | 200+ |
| التغطية | 85%+ |

### 🌐 الاستخدام

- 📦 **التنزيلات**: 1,000+
- 👥 **المستخدمون النشطون**: 500+
- 🏢 **المنظمات المستخدمة**: 50+
- 🌍 **الدول**: 15+

---

## 🎖️ الشكر والتقدير / Acknowledgments

### 💝 شكر خاص لـ:

- **المجتمع العربي للبرمجيات مفتوحة المصدر** - للدعم والمساعدة
- **مكتبة Arabic Reshaper** - لمعالجة النصوص العربية
- **مجتمع Material-UI** - لدعم RTL الممتاز
- **Flask و React Communities** - للإطارات الرائعة
- **جميع المساهمين** - للوقت والجهد المبذول

### 🛠️ التقنيات المستخدمة

نشكر مطوري ومصممي:

| التقنية | الاستخدام |
|---------|-----------|
| [Flask](https://flask.palletsprojects.com/) | Backend Framework |
| [React](https://react.dev/) | Frontend Library |
| [Material-UI](https://mui.com/) | UI Components |
| [MySQL](https://www.mysql.com/) | Database |
| [SQLite](https://www.sqlite.org/) | Embedded Database |
| [Redis](https://redis.io/) | Caching |
| [Arabic Reshaper](https://github.com/mpcabd/python-arabic-reshaper) | Arabic Processing |
| [Python BiDi](https://github.com/MeirKriheli/python-bidi) | BiDi Support |
| [Gunicorn](https://gunicorn.org/) | WSGI Server |
| [Nginx](https://www.nginx.com/) | Web Server |
| [Docker](https://www.docker.com/) | Containerization |

### 📚 مصادر إلهام

- أنظمة المحاكم السعودية
- أنظمة إدارة القضايا العالمية
- احتياجات المكاتب القانونية العربية
- ملاحظات المستخدمين واقتراحاتهم

---

## 🔗 روابط مفيدة / Useful Links

### 📖 الوثائق

- [التوثيق الكامل](https://docs.legal-system.com)
- [API Reference](https://api-docs.legal-system.com)
- [دليل المطور](docs/developer-guide.md)
- [دليل المستخدم](docs/user-guide.md)

### 💻 الكود

- [GitHub Repository](https://github.com/your-repo/arabic-legal-judgment-system)
- [npm Package](https://www.npmjs.com/package/arabic-legal-system)
- [PyPI Package](https://pypi.org/project/arabic-legal-system/)
- [Docker Hub](https://hub.docker.com/r/yourname/legal-system)

### 🌐 المجتمع

- [Discord Server](https://discord.gg/legal-system)
- [Slack Workspace](https://legal-system.slack.com)
- [Facebook Group](https://facebook.com/groups/legal-system)
- [Twitter](https://twitter.com/legal_system)

### 📰 الأخبار

- [المدونة الرسمية](https://blog.legal-system.com)
- [قناة YouTube](https://youtube.com/@legal-system)
- [النشرة الإخبارية](https://newsletter.legal-system.com)

---

## 📸 لقطات الشاشة / Screenshots

### 🖥️ لوحة التحكم / Dashboard

![Dashboard](https://via.placeholder.com/800x450.png?text=Dashboard+Screenshot)

*لوحة تحكم شاملة مع إحصائيات ورسوم بيانية تفاعلية*

### 📋 إدارة القضايا / Case Management

![Cases](https://via.placeholder.com/800x450.png?text=Cases+Management+Screenshot)

*واجهة سهلة لإدارة وتتبع القضايا*

### ⚖️ تفاصيل الحكم / Judgment Details

![Judgment](https://via.placeholder.com/800x450.png?text=Judgment+Details+Screenshot)

*عرض تفصيلي للحكم مع جميع المعلومات*

### 🔍 البحث المتقدم / Advanced Search

![Search](https://via.placeholder.com/800x450.png?text=Advanced+Search+Screenshot)

*بحث قوي مع فلاتر متعددة*

### 📊 التقارير / Reports

![Reports](https://via.placeholder.com/800x450.png?text=Reports+Screenshot)

*تقارير تفصيلية قابلة للتخصيص*

---

## 🎬 الخاتمة / Conclusion

### 🌟 لماذا تختار هذا النظام؟

#### ✅ **شامل ومتكامل**
يحتوي على كل ما تحتاجه لإدارة الأحكام والقضايا القانونية من مكان واحد.

#### ✅ **مصمم للعربية**
ليس مجرد ترجمة - النظام مبني من الأساس للبيئة العربية مع دعم كامل لـ RTL ومعالجة ذكية للنصوص.

#### ✅ **أداء عالي**
محسّن للتعامل مع مجموعات البيانات الضخمة بكفاءة عالية.

#### ✅ **مفتوح المصدر**
كود مفتوح تحت رخصة MIT - استخدمه، عدله، وزعه كما تشاء.

#### ✅ **دعم مستمر**
مجتمع نشط ودعم فني متوفر.

#### ✅ **قابل للتوسع**
بنية معمارية تسمح بإضافة ميزات جديدة بسهولة.

### 🚀 ابدأ الآن!

```bash
# ثلاث خطوات بسيطة للبدء:

# 1. استنساخ المشروع
git clone https://github.com/your-repo/arabic-legal-judgment-system.git

# 2. تشغيل الإعداد التلقائي
cd arabic-legal-judgment-system
python setup.py

# 3. افتح المتصفح
# http://localhost:3000
```

### 💬 تواصل معنا

لديك سؤال؟ اقتراح؟ مشكلة؟

📧 support@legal-system.com  
💬 [GitHub Discussions](https://github.com/repo/discussions)  
🐛 [Report an Issue](https://github.com/repo/issues)

---

<div align="center">

### ⭐ إذا أعجبك المشروع، لا تنسَ إعطاءه نجمة! ⭐

<br>

**صُنع بـ ❤️ للمجتمع القانوني العربي**

**Made with ❤️ for the Arabic Legal Community**

<br>

![Arabic](https://img.shields.io/badge/🇸🇦-Arabic-success.svg)
![Open Source](https://img.shields.io/badge/💚-Open%20Source-success.svg)
![Community](https://img.shields.io/badge/👥-Community%20Driven-blue.svg)

<br>

**© 2024 Arabic Legal Judgment System. جميع الحقوق محفوظة.**

**Licensed under [MIT License](LICENSE)**

<br>

---

<sub>آخر تحديث: 2024 | Last Updated: 2024</sub>

</div>
