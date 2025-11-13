# دليل النشر / Deployment Guide

## نظرة عامة / Overview

هذا الدليل يوضح كيفية نشر نظام إدارة الأحكام القانونية العربية في بيئات مختلفة.

## أنواع النشر / Deployment Types

### 1. النشر التطويري / Development Deployment
للتطوير والاختبار المحلي

### 2. النشر الإنتاجي / Production Deployment
للاستخدام الفعلي في بيئة العمل

### 3. النشر السحابي / Cloud Deployment
على منصات سحابية مثل AWS, Azure, Google Cloud

## المتطلبات / Requirements

### الحد الأدنى للموارد / Minimum Resources
- **المعالج**: 2 CPU cores
- **الذاكرة**: 4GB RAM
- **التخزين**: 50GB SSD
- **النطاق الترددي**: 100Mbps

### الموارد الموصى بها / Recommended Resources
- **المعالج**: 4+ CPU cores
- **الذاكرة**: 8GB+ RAM
- **التخزين**: 200GB+ SSD
- **النطاق الترددي**: 1Gbps

## النشر باستخدام Docker / Docker Deployment

### 1. إعداد Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  # MySQL Database
  mysql:
    image: mysql:8.0
    container_name: legal_mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: arabic_legal_system
      MYSQL_USER: legal_user
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: legal_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  # Backend API
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: legal_backend
    environment:
      - MYSQL_HOST=mysql
      - MYSQL_USER=legal_user
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
      - MYSQL_DB=arabic_legal_system
      - REDIS_URL=redis://redis:6379/0
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - SECRET_KEY=${SECRET_KEY}
    ports:
      - "5000:5000"
    depends_on:
      - mysql
      - redis
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: legal_frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  mysql_data:
  redis_data:
```

### 2. ملف Docker للخلفية

```dockerfile
# Dockerfile.backend
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p uploads logs

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### 3. ملف Docker للواجهة الأمامية

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## النشر على الخوادم المحلية / On-Premise Deployment

### 1. إعداد الخادم / Server Setup

```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت المتطلبات
sudo apt install -y python3 python3-pip nodejs npm mysql-server nginx

# إعداد MySQL
sudo mysql_secure_installation

# إنشاء قاعدة البيانات
sudo mysql -u root -p << EOF
CREATE DATABASE arabic_legal_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'legal_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON arabic_legal_system.* TO 'legal_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
EOF
```

### 2. نشر التطبيق / Deploy Application

```bash
# إنشاء مستخدم للتطبيق
sudo useradd -m -s /bin/bash legalapp
sudo su - legalapp

# استنساخ المشروع
git clone <repository-url> arabic-legal-judgment-system
cd arabic-legal-judgment-system

# إعداد البيئة الافتراضية
python3 -m venv venv
source venv/bin/activate

# تثبيت المتطلبات
pip install -r requirements.txt
pip install gunicorn

# إعدادات الإنتاج
cp .env.example .env
# تحرير ملف .env بالإعدادات الصحيحة

# تهيئة قاعدة البيانات
python database/init_db.py

# بناء الواجهة الأمامية
cd frontend
npm install
npm run build
cd ..
```

## المراقبة والصيانة / Monitoring & Maintenance

### 1. إعداد المراقبة

```bash
# تثبيت Prometheus و Grafana
docker run -d --name prometheus -p 9090:9090 prom/prometheus
docker run -d --name grafana -p 3000:3000 grafana/grafana
```

### 2. النسخ الاحتياطي / Backup

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/legal-system"
DB_NAME="arabic_legal_system"

# إنشاء مجلد النسخة الاحتياطية
mkdir -p $BACKUP_DIR

# نسخة احتياطية من قاعدة البيانات
mysqldump -u legal_user -p$MYSQL_PASSWORD $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# نسخة احتياطية من الملفات
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz uploads/ logs/

# حذف النسخ القديمة (أقدم من 30 يوم)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

### 3. تحديث النظام / System Updates

```bash
#!/bin/bash
# update.sh

cd /home/legalapp/arabic-legal-judgment-system

# سحب التحديثات
git pull origin main

# تحديث البيئة الافتراضية
source venv/bin/activate
pip install -r requirements.txt

# تشغيل الترقيات
python database/migrations.py

# بناء الواجهة الأمامية الجديدة
cd frontend
npm install
npm run build
cd ..

# إعادة تشغيل الخدمات
sudo systemctl restart legal-backend
sudo systemctl reload nginx

echo "System updated successfully"
```

## إعدادات الأمان / Security Configuration

### 1. إعدادات Firewall

```bash
# إعداد UFW
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing

# فتح المنافذ المطلوبة
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS

# إعدادات خاصة للإنتاج
sudo ufw deny 3306/tcp  # MySQL (داخليا فقط)
sudo ufw deny 5000/tcp  # Backend (داخليا فقط)
```

### 2. تعزيز الأمان / Security Hardening

```bash
# تعطيل SSH root login
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# تمكين SSH key authentication only
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# إعادة تشغيل SSH
sudo systemctl restart ssh

# تثبيت Fail2Ban
sudo apt install fail2ban

# إعداد Fail2Ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## استكشاف الأخطاء / Troubleshooting

### المشاكل الشائعة / Common Issues

#### 1. خطأ في الاتصال بقاعدة البيانات
```bash
# فحص حالة MySQL
sudo systemctl status mysql

# فحص الاتصال
mysql -u legal_user -p -e "SHOW DATABASES;"

# فحص ملف الإعدادات
cat .env | grep MYSQL
```

#### 2. مشاكل في الترميز العربي
```bash
# فحص ترميز قاعدة البيانات
mysql -u legal_user -p -e "SHOW VARIABLES LIKE 'character_set%';"

# يجب أن تكون النتيجة utf8mb4
```

#### 3. خطأ 502 Bad Gateway
```bash
# فحص حالة الخدمة الخلفية
sudo systemctl status legal-backend

# فحص سجلات Nginx
sudo tail -f /var/log/nginx/error.log

# فحص الاتصال الداخلي
curl http://127.0.0.1:5000/api/health
```

### أدوات التشخيص / Diagnostic Tools

```bash
# ملف فحص النظام
#!/bin/bash
# system_check.sh

echo "=== Arabic Legal System Health Check ==="

# فحص الخدمات
echo "1. Services Status:"
systemctl is-active mysql legal-backend nginx

# فحص قاعدة البيانات
echo "2. Database Connection:"
mysql -u legal_user -p$MYSQL_PASSWORD -e "SELECT 'OK' as status;"

# فحص المساحة
echo "3. Disk Usage:"
df -h /

# فحص الذاكرة
echo "4. Memory Usage:"
free -h

# فحص الشبكة
echo "5. Network Status:"
netstat -tlnp | grep -E ':80|:443|:3306|:5000'

# فحص السجلات
echo "6. Recent Errors:"
tail -20 /var/log/nginx/error.log
tail -20 /home/legalapp/arabic-legal-judgment-system/logs/app.log

echo "=== Health Check Complete ==="
```

## الأداء والتحسين / Performance Optimization

### 1. تحسين قاعدة البيانات / Database Optimization

```sql
-- إضافة فهارس للبحث السريع
CREATE INDEX idx_cases_title ON cases(title);
CREATE INDEX idx_cases_status ON cases(status);
CREATE INDEX idx_judgments_date ON judgments(judgment_date);
CREATE INDEX idx_documents_type ON documents(document_type);

-- تحسين إعدادات MySQL
-- في ملف /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
innodb_buffer_pool_size = 2G
innodb_log_file_size = 256M
max_connections = 100
query_cache_type = 1
query_cache_size = 128M
```

### 2. تحسين Nginx / Nginx Optimization

```nginx
# إضافة للملف /etc/nginx/nginx.conf
worker_processes auto;
worker_connections 2048;

# تمكين ضغط البيانات
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types
    text/css
    text/javascript
    text/xml
    text/plain
    application/javascript
    application/xml+rss
    application/json;

# تحسين التخزين المؤقت
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control public;
}
```

### 3. مراقبة الأداء / Performance Monitoring

```bash
# تثبيت htop للمراقبة
sudo apt install htop

# تثبيت iotop لمراقبة الإدخال/الإخراج
sudo apt install iotop

# مراقبة الاستهلاك
htop
iotop
```

---

## الخلاصة / Conclusion

هذا الدليل يغطي جميع جوانب نشر نظام إدارة الأحكام القانونية العربية. تأكد من:

1. **اتباع إعدادات الأمان** المذكورة أعلاه
2. **إجراء النسخ الاحتياطية** بانتظام
3. **مراقبة النظام** باستمرار
4. **تحديث النظام** عند توفر تحديثات

لأي استفسارات أو مساعدة، يرجى الرجوع إلى الوثائق الرئيسية أو التواصل مع فريق الدعم.
