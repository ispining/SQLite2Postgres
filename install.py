import subprocess, sys

subprocess.call('pip install virtualenv', shell=True)
if sys.platform == 'win32':
    subprocess.call('/venv/Scripts/activate', shell=True)
else:
    subprocess.call('source /venv/bin/activate', shell=True)

subprocess.call('pip install -r ./r.txt')
