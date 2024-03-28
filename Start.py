import subprocess
import sys
import time
scripts = [
    "ais_Argentina_usa.py",
    "ais_Chile_usa.py",
    "ais_uk_usa.py",
    "AIS_UK_USA_YUYUE.py"
]

# 遍历并执行每个脚本
for script in scripts:
    subprocess.run(["python", script])
