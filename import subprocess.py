import subprocess
import json
import os

params = {...}

subprocess.run(
    ["python", "std_score_visualize.py"],
    input=json.dumps(params),
    text=True
)