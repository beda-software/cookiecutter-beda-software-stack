#!/bin/bash

PGUSER=postgres

AIO_HOST=0.0.0.0
AIO_PORT=8081
APP_ID=app-{{cookiecutter.project_slug_dashed}}
AIDBOX_PORT=8080
AIDBOX_CLIENT_ID=root

case $TIER in
    master)
        AIDBOX_BASE_URL=https://master-backend.{{cookiecutter.project_domain}}
        FRONTEND_URL=https://master.{{cookiecutter.project_domain}}
        ;;
    staging)
        AIDBOX_BASE_URL=https://staging-backend.{{cookiecutter.project_domain}}
        FRONTEND_URL=https://staging.{{cookiecutter.project_domain}}
        ;;
    develop)
        AIDBOX_BASE_URL=https://develop-backend.{{cookiecutter.project_domain}}
        FRONTEND_URL=https://develop.{{cookiecutter.project_domain}}
        ;;
esac
