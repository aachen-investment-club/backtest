from typing import List, Optional, Union
from datastream.Source import Source
from datastream.ClockSource import ClockSource
import pandas as pd


class Datastream:
    def __init__(
        self: "Datastream",
        data_sources: List[Source],
        clock_cycle: Optional[pd.Timedelta] = None,
    ) -> None:
        self.data_sources = data_sources
        self.timestamp: pd.Timestamp = pd.Timestamp(0)  # init with 0

        # set values obtained from data_sources
        assert len(data_sources) > 0, "data_sources must be a non-empty list"
        self.total_data_obj = sum([source.length for source in data_sources])
        self.data_obj_counter = 0
        self.start = min([source.start for source in data_sources])
        self.end = max([source.end for source in data_sources])

        # init clock and append to data_sources
        # must be after all other data_sources because it uses the 
        # min start and max end of the other data_sources
        if clock_cycle is not None:
            self.clock = ClockSource(
                start=self.start, end=self.end, cycle=clock_cycle
            )
            self.total_data_obj += self.clock.length
            self.data_sources.append(self.clock)

    def pop_next(
        self: "Datastream",
    ) -> Union[dict, None]:
        # assuming that we have at least one data source
        # set default next_source to None
        next_source: Optional[Source] = None

        # find the next source
        for source in self.data_sources:
            if not source.empty():
                if next_source is None:
                    next_source = source  # init with first source in list
                    continue
                else:
                    # if we find a source with a timestamp that is earlier
                    # than the current next_source,
                    # set next_source to that source
                    if next_source.get_next_timestamp() \
                          > source.get_next_timestamp():
                        next_source = source

        if next_source is None:
            return None
        else:
            next_data_obj = next_source.pop_next_value()
            self.timestamp = next_data_obj['timestamp']  # update global timestamp
            self.data_obj_counter += 1
            return next_data_obj
