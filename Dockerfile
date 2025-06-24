FROM python:3.13-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /application

RUN pip install --upgrade pip wheel

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH /application

RUN chmod +x entrypoint_api.sh

CMD ["bash", "entrypoint_api.sh"]