from asyncio.subprocess import PIPE
import subprocess
from time import sleep
res= subprocess.check_output("whoami", shell=True)
print(res)