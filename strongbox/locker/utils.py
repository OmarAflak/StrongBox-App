import os


def create_parent_folder(filepath: str):
    base = os.path.dirname(filepath)
    if base != "":
        os.makedirs(base, exist_ok=True)
