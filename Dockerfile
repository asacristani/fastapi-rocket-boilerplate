FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false && poetry install

# Port
EXPOSE 8000

CMD ./entrypoint.sh
