#Command to input enviorment file "docker run --name [container-name] --env-file [path-to-env-file] [image-name]"

FROM python:3.10.11-slim
LABEL authors="barankazan"

#Stops from generating .pyc files in container
ENV PYTHONDONTWRITEBYTECODE=1

#Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN python -m pip install --root-user-action=ignore -r requirements.txt

CMD ["python", "main.py"]