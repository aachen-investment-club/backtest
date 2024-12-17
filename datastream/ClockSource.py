from datastream.Source import Source
import pandas as pd


class ClockSource(Source):
    def __init__(
        self: "ClockSource",
        start: pd.Timestamp,
        end: pd.Timestamp,
        cycle: pd.Timedelta,
    ) -> None:
        """_summary_
        Args:
            cycle (pd.Timedelta): clock cycle time
        """
        self.cycle = cycle
        self.counter = 0
        self.start = start
        self.end = end
        self.next_timestamp = start
        self.length = int((self.end - self.start) / self.cycle)
        self.type = "Clock"

    def pop_next_value(self: "ClockSource") -> dict:
        next_data_object =  {
            'id': 'Clock',
            'timestamp': self.next_timestamp,
        }
        self.next_timestamp += self.cycle
        self.counter += 1
        return next_data_object

    def get_next_timestamp(self: "ClockSource") -> pd.Timestamp:
        return self.next_timestamp

    def empty(self: "ClockSource") -> bool:
        if self.next_timestamp == self.end + self.cycle:
            return True
        else:
            return False
