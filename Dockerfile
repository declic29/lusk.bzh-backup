FROM alpine:3.19

RUN apk add --no-cache python3 py3-pip git build-base libffi-dev py3-lxml py3-yaml

WORKDIR /app

COPY . /app

RUN pip install -e .

ENV SEARXNG_SETTINGS_PATH=/app/searx/settings.yml

CMD ["python3", "-m", "searx.webapp"]
