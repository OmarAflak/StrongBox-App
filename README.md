# StrongBox Desktop Application

A free, opensource, and safe passwords keeper. [Chrome extension available](https://github.com/OmarAflak/StrongBox-Extension).

# Mac - GUI Support

```shell
# git clone ... & cd ...
python -m venv .venv
source .venv/bin/activate
.venv/bin/python -m pip install -r requirements.txt
PYTHONPATH=$(pwd) .venv/bin/python strongbox/gui/main.py 
```

The app will run in the background, and can be stopped from the status bar.

# Linux & Windows

```shell
# git clone ... & cd ...
python -m venv .venv
source .venv/bin/activate
.venv/bin/python -m pip install -r requirements.txt
uvicorn strongbox.app.server:app --reload
```