FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install .

# Port
EXPOSE 8000

CMD ./entrypoint.sh
