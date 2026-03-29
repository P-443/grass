# استخدام صورة جاهزة مخصصة لـ Grass Node
FROM mrwan0/grass-node:latest

# تحديد مسار العمل
WORKDIR /app

# المتغيرات البيئية (سيتم سحبها من إعدادات ريلواي)
ENV USER_EMAIL="tahanmare0062"
ENV USER_PASSWORD="FirstNameAhmed1*"

# أمر التشغيل الافتراضي الموجود في الصورة
CMD ["python3", "main.py"]
