FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y docker.io

ENTRYPOINT ["python", "src/algorithmRun.py", "-f"]
CMD ["config.yaml"]
