# استخدام نسخة خفيفة من بايثون
FROM python:3.9-slim

# تثبيت المكتبات اللازمة للاتصال
RUN pip install --no-cache-dir requests loguru websockets_proxy self_parsing

# تحميل سكربت التشغيل (نسخة مجتمعية موثوقة للـ Docker)
ADD https://raw.githubusercontent.com/ym95/grass-node/main/main.py /app/main.py

WORKDIR /app

# إعداد المتغيرات البيئية التي سيستخدمها السكربت
ENV GRASS_USER="tahanmare0062"
ENV GRASS_PASS="FirstNameAhmed1*"

# أمر التشغيل
CMD ["python", "main.py"]
