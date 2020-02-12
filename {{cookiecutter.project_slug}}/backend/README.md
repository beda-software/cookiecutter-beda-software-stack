# {{cookiecutter.project_name}} Backend

## Tests
To run tests locally, copy `.env.tpl` to `.env` and specify `AIDBOX_LICENSE_ID` and `AIDBOX_LICENSE_KEY`.  


Build images using `docker-compose build -f docker-compose.tests.yaml`.


After that, just start `./run_test.sh` or `./run_test.sh tests/test_base.py` (if you want to run the particular file/test).
The first run may take about a minute because it prepares the db and devbox.


If you have updated some requirements, you need to re-run `docker-compose build -f docker-compose.tests.yaml`
