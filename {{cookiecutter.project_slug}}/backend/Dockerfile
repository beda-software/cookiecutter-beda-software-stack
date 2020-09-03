FROM python:3.7
RUN mkdir /app
WORKDIR /app

# COPY ./requirements ./requirements
COPY . .
RUN pip install pipenv
RUN pipenv install

CMD ["gunicorn", "main:create_app", "--worker-class", "aiohttp.worker.GunicornWebWorker", "-b", "0.0.0.0:8081"]
EXPOSE 8081
