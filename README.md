# StrongBox

A free, opensource, and safe passwords keeper. Chrome extension available.

# Run

```
git clone ... & cd ...
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn strongbox.server.api:app --reload
```