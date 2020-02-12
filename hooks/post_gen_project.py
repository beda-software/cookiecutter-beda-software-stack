import shutil
import sys
from subprocess import Popen, PIPE

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

    sys.exit(0)
