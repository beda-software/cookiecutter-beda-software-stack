FROM python:3.8
RUN mkdir /app
WORKDIR /app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install
COPY . .

CMD ["pipenv", "run", "gunicorn", "main:create_app", "--worker-class", "aiohttp.worker.GunicornWebWorker", "-b", "0.0.0.0:8081"]
EXPOSE 8081
