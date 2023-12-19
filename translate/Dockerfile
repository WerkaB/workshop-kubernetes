FROM python:latest
WORKDIR /app
COPY translate.py /app/translate.py
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt && rm /app/requirements.txt
EXPOSE 8080
ENTRYPOINT ["python", "/app/translate.py"]