from abc import ABC, abstractmethod
from typing import Union
import pandas as pd


class Source(ABC):
    def __init__(self: "Source") -> None:
        self.start: pd.Timestamp = pd.Timestamp(0)
        self.end: pd.Timestamp = pd.Timestamp(0)
        self.length: int = 0

    @abstractmethod
    def pop_next_value(self: "Source") -> (
        Union[dict, None]
    ):
        raise NotImplementedError("Derived class should implement pop_next_data()")

    @abstractmethod
    def get_next_timestamp(self: "Source") -> pd.Timestamp:
        raise NotImplementedError("Derived class should implement get_next_timestamp()")

    @abstractmethod
    def empty(self: "Source") -> bool:
        raise NotImplementedError("Derived class should implement empty()")
