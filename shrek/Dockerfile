FROM python:latest
WORKDIR /app
COPY shrek.py /app/shrek.py
COPY requirements.txt /app/requirements.txt
COPY  quotes.json /app/quotes.json
RUN pip install -r /app/requirements.txt && rm /app/requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "/app/shrek.py"]