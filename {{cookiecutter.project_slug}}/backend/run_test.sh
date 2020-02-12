#!/bin/sh

if [ -f ".env" ]; then
    export `cat .env`
fi

if [ -z "${AIDBOX_LICENSE_KEY}" ]; then
    echo "AIDBOX_LICENSE_KEY is required to run tests"
    exit 1
fi

if [ -z "${AIDBOX_LICENSE_ID}" ]; then
    echo "AIDBOX_LICENSE_ID is required to run tests"
    exit 1
fi

export TEST_COMMAND=" wait-for-it.sh devbox:8080 --strict --timeout=0 -- pytest --cov-report html --cov-report term:skip-covered --cov=main $@"

docker-compose -f docker-compose.tests.yaml up --exit-code-from backend backend
exit $?
