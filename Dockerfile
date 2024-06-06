FROM python:3.11-slim-bookworm as builder

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN python -m venv /venv \
    && . /venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && find /venv -name '__pycache__' -exec rm -r {} + \
    && find /venv -name '*.pyc' -exec rm -r {} + \
    && find /venv -name '*.pyo' -exec rm -r {} +

FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /venv /venv
COPY . .

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser
USER appuser

EXPOSE 8501

ENTRYPOINT [ "/venv/bin/python", "-m", "streamlit", "run" ]
CMD [ "viewer.py" ]