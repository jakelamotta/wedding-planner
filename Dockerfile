FROM python:3.9-alpine
RUN mkdir -p /app/wedding/templates
RUN mkdir -p /app/static/css/fonts
RUN mkdir /app/static/js
RUN mkdir /app/static/img
RUN mkdir -p /app/translations/se/LC_MESSAGES
RUN apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev
RUN apk add --no-cache libxslt
WORKDIR /app
ADD requirements.txt /app
ADD auth.py /app
ADD main.py /app
ADD wedding/util.py /app/wedding
ADD wedding/__init__.py /app/wedding
ADD models.py /app
ADD translations/se/LC_MESSAGES/messages.* translations/se/LC_MESSAGES/
ADD wedding/templates/*.html /app/wedding/templates/
ADD wedding/static/css/*.map /app/wedding/static/css/
ADD wedding/static/css/*.css /app/wedding/static/css/
ADD wedding/static/css/fonts/* /app/wedding/static/css/fonts/
ADD wedding/static/js/* /app/wedding/static/js/
ADD wedding/static/img/wedding1.jpg /app/wedding/static/img/
ADD wedding/static/img/gallery1.jpg /app/wedding/static/img/
ADD wedding/static/img/gallery2.jpg /app/wedding/static/img/
ADD wedding/static/img/gallery3.jpg /app/wedding/static/img/
ADD wedding/static/img/gallery4.jpg /app/wedding/static/img/
ADD wedding/static/img/gallery7.jpg /app/wedding/static/img/
ADD wedding/static/img/gallery6.jpg /app/wedding/static/img/
RUN pip3 install -r requirements.txt
CMD ["gunicorn", "-w 1", "-b", "0.0.0.0:8001", "main:app"]
