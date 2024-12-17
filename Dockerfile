FROM python:3.12-slim

WORKDIR /root/gogrok

COPY requirements.txt /root/gogrok/
RUN pip install -r requirements.txt

COPY . /root/gogrok/

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=config.settings

# Run Gunicorn as the entry point
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
