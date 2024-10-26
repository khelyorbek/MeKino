FROM python:3.10
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
EXPOSE 3000
CMD ["gunicorn", "-b", "0.0.0.0:3000", "app:app"]l