start:
    venv/bin/python3 main.py

prestart:
    python3 -m venv venv
    venv/bin/pip install -r requirments.txt