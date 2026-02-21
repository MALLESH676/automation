FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENV PYTHONPATH="."
EXPOSE 5000
CMD ["python", "src/app/server.py"]
