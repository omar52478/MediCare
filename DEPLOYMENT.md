# 🚀 Deployment Guide - MediCare on Render

## ✅ الملفات الجاهزة للـ Deployment

تم إنشاء الملفات التالية:
- ✅ `.gitignore` - لتجاهل الملفات غير المطلوبة
- ✅ `requirements.txt` - جميع المكتبات المطلوبة
- ✅ `Procfile` - لتشغيل Gunicorn
- ✅ `build.sh` - سكريبت البناء
- ✅ `render.yaml` - إعدادات Render
- ✅ `runtime.txt` - إصدار Python
- ✅ `settings.py` - محدث للإنتاج

---

## 📦 الخطوة 1: تثبيت المكتبات الجديدة (اختياري - للتجربة محلياً)

```powershell
pip install gunicorn whitenoise psycopg2-binary dj-database-url python-dotenv
```

---

## 📁 الخطوة 2: جمع الملفات الثابتة

```powershell
python manage.py collectstatic --no-input
```

---

## 🔧 الخطوة 3: أوامر Git

### إذا لم يكن Git مُهيأ:
```powershell
# تهيئة Git
git init

# إضافة الـ Remote
git remote add origin https://github.com/omar52478/MediCare.git
```

### إضافة الملفات والـ Commit:
```powershell
# إضافة جميع الملفات
git add .

# عمل Commit
git commit -m "Prepare for Render deployment"

# رفع الملفات (إذا كان هناك محتوى سابق)
git pull origin main --rebase

# رفع للـ GitHub
git push -u origin main
```

### إذا واجهت مشكلة في الـ Push:
```powershell
git push -u origin main --force
```

---

## 🌐 الخطوة 4: إعداد Render

### 1. اذهب إلى [render.com](https://render.com) وسجل الدخول

### 2. إنشاء Web Service جديد:
   - اضغط على **"New +"** → **"Web Service"**
   - اختر **"Build and deploy from a Git repository"**
   - اضغط **"Connect"** وحدد الـ repo: `omar52478/MediCare`

### 3. إعدادات الـ Service:
   | الإعداد | القيمة |
   |---------|--------|
   | **Name** | `medicare` |
   | **Region** | `Frankfurt (EU Central)` أو أقرب منطقة |
   | **Branch** | `main` |
   | **Runtime** | `Python 3` |
   | **Build Command** | `./build.sh` |
   | **Start Command** | `gunicorn project.wsgi:application` |
   | **Plan** | `Free` |

### 4. إضافة Environment Variables:
   اضغط على **"Advanced"** وأضف:
   
   | Key | Value |
   |-----|-------|
   | `SECRET_KEY` | (اضغط Generate) |
   | `DEBUG` | `False` |
   | `PYTHON_VERSION` | `3.11.0` |

### 5. إنشاء قاعدة بيانات PostgreSQL (اختياري):
   - اذهب إلى **"New +"** → **"PostgreSQL"**
   - Name: `medicare-db`
   - Plan: `Free`
   - بعد الإنشاء، انسخ **Internal Database URL**
   - ارجع للـ Web Service وأضف:
     - `DATABASE_URL` = (الـ URL اللي نسخته)

### 6. اضغط **"Create Web Service"**

---

## ⏳ الخطوة 5: انتظر الـ Build

- Render هيشغل `build.sh` تلقائياً
- هياخد حوالي 2-5 دقائق
- لما يخلص، هتلاقي رابط زي: `https://medicare-xxxx.onrender.com`

---

## 🔐 الخطوة 6: إنشاء حساب Admin

بعد ما الموقع يشتغل، محتاج تعمل superuser:

### الطريقة 1: من Render Shell
1. اذهب للـ Web Service في Render
2. اضغط على **"Shell"** tab
3. اكتب:
```bash
python manage.py createsuperuser
```

### الطريقة 2: إضافة أمر في build.sh
أضف في نهاية `build.sh`:
```bash
# Create superuser (only first time)
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell
```

---

## 🎉 تم!

الموقع جاهز على:
```
https://medicare-xxxx.onrender.com
```

### الروابط المهمة:
- **الصفحة الرئيسية:** `/`
- **تسجيل الدخول:** `/accounts/login/`
- **لوحة التحكم:** `/accounts/dashboard/`
- **Django Admin:** `/admin/`

---

## 🔧 حل المشاكل الشائعة

### المشكلة: Static files not found
```bash
# في Render Shell
python manage.py collectstatic --no-input
```

### المشكلة: Database errors
- تأكد من إضافة `DATABASE_URL` في Environment Variables
- أو أنشئ PostgreSQL database من Render

### المشكلة: Build failed
- اتأكد إن `build.sh` له صلاحيات التنفيذ:
```bash
chmod +x build.sh
```
- أو أضف الأمر ده في Build Command:
```
chmod +x build.sh && ./build.sh
```

---

## 📝 ملاحظات مهمة

1. **الـ Free Plan** في Render بيعمل sleep بعد 15 دقيقة من عدم النشاط
2. **أول request** بعد الـ sleep بياخد وقت (30 ثانية تقريباً)
3. **PostgreSQL Free** ليه حدود (90 يوم)
4. **للإنتاج الحقيقي:** استخدم Paid Plan

---

**🏥 MediCare - Hospital Management System**
