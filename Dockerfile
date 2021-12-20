FROM python:3.9-alpine
RUN mkdir -p /app/wedding/templates
RUN mkdir -p /app/static/fonts
RUN mkdir /app/static/css
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
ADD templates/*.html /app/wedding/templates/
ADD static/css/bootstrap.css /app/static/css
ADD static/fonts/* /app/static/fonts/
RUN pip3 install -r requirements.txt
CMD ["gunicorn", "-w 1", "-b", "0.0.0.0:8001", "main:app"]
