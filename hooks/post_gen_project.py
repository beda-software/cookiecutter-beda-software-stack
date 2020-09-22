import os
import shutil
import sys
from subprocess import Popen, PIPE

REMOVE_PATHS = [
    {% if cookiecutter.add_push_notifications == "n" %}'backend/app/push_notification.py',{% endif %}
    {% if cookiecutter.add_gcs == "n" %}
    'backend/app/gcs.py',
    'backend/app/contrib/google_cloud.py',
    {% endif %}
    {% if cookiecutter.add_aws == "n" %}
    'backend/app/aws.py',
    'backend/app/contrib/amazon.py',
    {% endif %}
]

if __name__ == '__main__':
    create_frontend = '{{ cookiecutter.create_frontend }}'.lower() == 'y'
    create_mobile = '{{ cookiecutter.create_mobile }}'.lower() == 'y'
    if create_frontend:
        process = Popen(
            ['npx', 'create-react-app', 'frontend',
             # TODO: use our template
             '--template', 'cra-template-typescript'],
            stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode())

    if create_mobile:
        process = Popen(
            ['npx', 'react-native', 'init', 'mobile',
             # TODO: use our template
             '--template', 'react-native-template-typescript@6.2.0'],
            stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode())

    if not create_frontend or not create_mobile:
        shutil.rmtree('shared')

    for path in REMOVE_PATHS:
        path = path.strip()
        path = os.path.join(os.getcwd(), path)
        if path and os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    sys.exit(0)
