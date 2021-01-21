# Cookiecutter for beda.software stack

## Setup

Install cookiecutter and other dependencies
```bash
pip install -r requirements.txt 
```

Run

```
cookiecutter https://github.com/beda-software/cookiecutter-beda-software-stack.git
```

## Restore the database from the dump
```bash
docker-compose down
docker-compose up -d devbox-db
# wait for db to start
cat backup.dump |  docker exec -i environment_devbox-db_1 pg_restore  -d devbox
```
