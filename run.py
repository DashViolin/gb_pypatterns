import platform
import sys
from subprocess import Popen
from time import sleep

command = "python manage.py run"
if platform.system().lower() == "windows":
    server_task = Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)  # type: ignore
else:
    server_task = Popen(command, executable="/bin/bash", shell=True)

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        server_task.kill()
        break
sys.exit(0)
