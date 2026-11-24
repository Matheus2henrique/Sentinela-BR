FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY sentinela_api.py exportar_estatico.py ./
COPY dados ./dados
EXPOSE 8000
CMD ["uvicorn", "sentinela_api:app", "--host", "0.0.0.0", "--port", "8000"]
