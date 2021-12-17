import os
import subprocess

os.chdir('/src/test')
subprocess.run(["/usr/local/bin/pytest", "-m", "parsing"])
os.chdir('..')
bot = subprocess.Popen(["/usr/local/bin/python", "bot.py"])
os.chdir('/src/test')
subprocess.run(["/usr/local/bin/pytest", "-m", "bot"])
bot.wait()
