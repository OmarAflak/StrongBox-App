from typing import Type, TypeVar
from dataclasses_json import DataClassJsonMixin
from strongbox.locker.utils import create_parent_folder


T = TypeVar("T", bound="IO")


class IO(DataClassJsonMixin):
    def to_file(self, filepath: str):
        create_parent_folder(filepath)
        with open(filepath, "w") as file:
            file.write(self.to_json())

    @classmethod
    def from_file(cls: Type[T], filepath: str) -> T:
        with open(filepath, "r") as file:
            return cls.from_json(file.read())

    @classmethod
    def copy(cls: Type[T], obj: T) -> T:
        return cls.from_json(obj.to_json())
