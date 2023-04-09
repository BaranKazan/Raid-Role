#Command to input enviorment file "docker run --name [container-name] --env-file [path-to-env-file] [image-name]"

FROM python:3.10.11-slim
LABEL authors="barankazan"

#Stops from generating .pyc files in container
ENV PYTHONDONTWRITEBYTECODE=1

#Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["python", "main.py"]