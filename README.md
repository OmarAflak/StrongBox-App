# StrongBox Desktop Application

A free, opensource, and safe passwords keeper. [Chrome extension available](https://github.com/OmarAflak/StrongBox-Extension).

# Run

```
git clone ... & cd ...
python -m venv .venv
source .venv/bin/activate
.venv/bin/python -m pip install -r requirements.txt
uvicorn strongbox.app.server:app --reload
```
