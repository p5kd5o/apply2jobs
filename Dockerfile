FROM python:3.13

ARG LOG_LEVEL=INFO
ENV LOG_LEVEL=${LOG_LEVEL}

EXPOSE 8000

WORKDIR /app

COPY src /app

RUN pip --no-cache-dir install --requirement requirements.txt

CMD ["fastapi", "run", "api.py"]
