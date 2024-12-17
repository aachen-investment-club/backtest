import pandas as pd
from typing import Union
from datastream.Source import Source


class EODSource(Source):
    def __init__(self: "EODSource", ric: str, data: pd.DataFrame) -> None:
        self.ric: str = ric
        self.data: pd.DataFrame = data
        self.start: pd.Timestamp = pd.Timestamp(self.data.index[0])
        self.end: pd.Timestamp = self.data.index[-1]
        assert self.start < self.end, "Start date must be before end date."
        self.length: int = self.data.shape[0]
        assert self.length > 0, "Data must have at least one entry."
        self.counter: int = 0

    def pop_next_value(self: "EODSource") -> (
        Union[dict, None]
    ):
        next_data_object = {
            'id': self.ric,
            'timestamp': self.data.index[self.counter], 
            'data': self.data.iloc[self.counter],
        }
        self.counter += 1
        return next_data_object

    def get_next_timestamp(self: "EODSource") -> pd.Timestamp:
        return pd.Timestamp(self.data.index[self.counter])

    def empty(self: "EODSource") -> bool:
        if self.counter == self.length:
            return True
        else:
            return False
