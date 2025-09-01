FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

COPY main.py .
COPY xgbModel.pkl .
COPY scaler.pkl .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
