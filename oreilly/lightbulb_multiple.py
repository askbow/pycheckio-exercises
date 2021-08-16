from datetime import datetime
from typing import List, Optional, Union, Tuple

class DynamicList(list):
    def __init__(self, gen):
        self._gen = gen

    def __getitem__(self, index):
        while index >= len(self):
            self.append(self._gen)
        return super(DynamicList, self).__getitem__(index)

def timediff(
        start: datetime, 
        end: datetime, 
        start_watching: Optional[datetime] = datetime(1970, 1, 1, 0, 0, 0),
        end_watching: Optional[datetime] = datetime(9999, 12, 31, 23, 59, 59)
    ) -> int:
    if start_watching > end:
        return 0
    if end_watching < start:
        return 0
    
    adjusted_start = start if start > start_watching else start_watching
    adjusted_end = end if end < end_watching else end_watching
    return (adjusted_end - adjusted_start).total_seconds()

def normalize_events(
        els: List[Union[datetime, Tuple[datetime, int]]]
    ) -> List[Tuple[datetime, int]]:
    normalized_els = list()
    lights = DynamicList(False)
    room_before = False
    for element in els:
        id = 1
        event = element
        if isinstance(element, tuple):
            event, id = element
        # toggle the light:
        lights[id] ^= True
        
        # if any of the lights are on, the event has no effect on the room
        if not any(lights) == room_before:
            normalized_els.append(event)
            room_before = any(lights)
        
    return normalized_els
    

def sum_light(
        els: List[Union[datetime, Tuple[datetime, int]]],
        start_watching: Optional[datetime] = datetime(1970, 1, 1, 0, 0, 0),
        end_watching: Optional[datetime] = datetime(9999, 12, 31, 23, 59, 59)
    ) -> int:
    """
        how long the light bulb has been turned on
    """
    events = normalize_events(els)
    if not len(events) % 2 == 0:
        events.append(end_watching)
    e = iter(events)
    periods = zip(e, e)
    r = sum([timediff(s, e, start_watching, end_watching) for s,e in periods])
    #print(f'sum: {r}')
    return r


if __name__ == '__main__':
    print("Basic:")
    print(sum_light([
        datetime(2015, 1, 12, 10, 0 , 0),
        datetime(2015, 1, 12, 10, 10 , 10),
        datetime(2015, 1, 12, 11, 0 , 0),
        datetime(2015, 1, 12, 11, 10 , 10),
    ]))
    
    # These "asserts" are used for self-checking and not for an auto-testing
    assert sum_light(els=[
        datetime(2015, 1, 12, 10, 0 , 0),
        datetime(2015, 1, 12, 10, 10 , 10),
    ]) == 610

    assert sum_light([
        datetime(2015, 1, 12, 10, 0 , 0),
        datetime(2015, 1, 12, 10, 10 , 10),
        datetime(2015, 1, 12, 11, 0 , 0),
        datetime(2015, 1, 12, 11, 10 , 10),
    ]) == 1220

    assert sum_light([
        datetime(2015, 1, 12, 10, 0 , 0),
        datetime(2015, 1, 12, 10, 10 , 10),
        datetime(2015, 1, 12, 11, 0 , 0),
        datetime(2015, 1, 12, 11, 10 , 10),
        datetime(2015, 1, 12, 11, 10 , 10),
        datetime(2015, 1, 12, 12, 10 , 10),
    ]) == 4820

    assert sum_light([
        datetime(2015, 1, 12, 10, 0 , 0),
        datetime(2015, 1, 12, 10, 0 , 1),
    ]) == 1

    assert sum_light([
        datetime(2015, 1, 12, 10, 0 , 0),
        datetime(2015, 1, 12, 10, 0 , 10),
        datetime(2015, 1, 12, 11, 0 , 0),
        datetime(2015, 1, 13, 11, 0 , 0),
    ]) == 86410

    print("tested compat with prev version!")


if __name__ == "__main__":
    print("With Start:")
    print(
        sum_light(
            [
                datetime(2015, 1, 12, 10, 0, 0),
                datetime(2015, 1, 12, 10, 0, 10),
            ],
            datetime(2015, 1, 12, 10, 0, 5),
        )
    )

    assert (
        sum_light(
            els=[
                datetime(2015, 1, 12, 10, 0, 0),
                datetime(2015, 1, 12, 10, 0, 10),
            ],
            start_watching=datetime(2015, 1, 12, 10, 0, 5),
        )
        == 5
    )

    assert (
        sum_light(
            [
                datetime(2015, 1, 12, 10, 0, 0),
                datetime(2015, 1, 12, 10, 0, 10),
            ],
            datetime(2015, 1, 12, 10, 0, 0),
        )
        == 10
    )

    assert (
        sum_light(
            [
                datetime(2015, 1, 12, 10, 0, 0),
                datetime(2015, 1, 12, 10, 10, 10),
                datetime(2015, 1, 12, 11, 0, 0),
                datetime(2015, 1, 12, 11, 10, 10),
            ],
            datetime(2015, 1, 12, 11, 0, 0),
        )
        == 610
    )

    assert (
        sum_light(
            [
                datetime(2015, 1, 12, 10, 0, 0),
                datetime(2015, 1, 12, 10, 10, 10),
                datetime(2015, 1, 12, 11, 0, 0),
                datetime(2015, 1, 12, 11, 10, 10),
            ],
            datetime(2015, 1, 12, 11, 0, 10),
        )
        == 600
    )

    assert (
        sum_light(
            [
                datetime(2015, 1, 12, 10, 0, 0),
                datetime(2015, 1, 12, 10, 10, 10),
                datetime(2015, 1, 12, 11, 0, 0),
                datetime(2015, 1, 12, 11, 10, 10),
            ],
            datetime(2015, 1, 12, 10, 10, 0),
        )
        == 620
    )

    assert (
        sum_light(
            [
                datetime(2015, 1, 12, 10, 0, 0),
                datetime(2015, 1, 12, 10, 10, 10),
                datetime(2015, 1, 12, 11, 0, 0),
                datetime(2015, 1, 12, 11, 10, 10),
                datetime(2015, 1, 12, 11, 10, 11),
                datetime(2015, 1, 12, 12, 10, 11),
            ],
            datetime(2015, 1, 12, 12, 10, 11),
        )
        == 0
    )

    assert (
        sum_light(
            [
                datetime(2015, 1, 12, 10, 0, 0),
                datetime(2015, 1, 12, 10, 10, 10),
                datetime(2015, 1, 12, 11, 0, 0),
                datetime(2015, 1, 12, 11, 10, 10),
                datetime(2015, 1, 12, 11, 10, 11),
                datetime(2015, 1, 12, 12, 10, 11),
            ],
            datetime(2015, 1, 12, 12, 9, 11),
        )
        == 60
    )

    print("Start check complete")


if __name__ == '__main__':
    print("Start and End:")
    print(sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 10),
    ],
    datetime(2015, 1, 12, 10, 0, 0),
    datetime(2015, 1, 12, 10, 0, 10)))
    
    assert sum_light(els=[
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 10),
    ],
    start_watching=datetime(2015, 1, 12, 10, 0, 0),
    end_watching=datetime(2015, 1, 12, 10, 0, 10)) == 10
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 10),
    ],
    datetime(2015, 1, 12, 10, 0, 0),
    datetime(2015, 1, 12, 10, 0, 7)) == 7
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 10),
    ],
    datetime(2015, 1, 12, 10, 0, 3),
    datetime(2015, 1, 12, 10, 0, 10)) == 7
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 10),
    ],
    datetime(2015, 1, 12, 10, 0, 10),
    datetime(2015, 1, 12, 10, 0, 20)) == 0
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
    ],
    datetime(2015, 1, 12, 10, 30, 0),
    datetime(2015, 1, 12, 11, 0, 0)) == 0
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
    ],
    datetime(2015, 1, 12, 10, 10, 0),
    datetime(2015, 1, 12, 11, 0, 0)) == 10
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
    ],
    datetime(2015, 1, 12, 10, 10, 0),
    datetime(2015, 1, 12, 11, 0, 10)) == 20
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
    ],
    datetime(2015, 1, 12, 9, 50, 0),
    datetime(2015, 1, 12, 10, 0, 10)) == 10
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
    ],
    datetime(2015, 1, 12, 9, 0, 0),
    datetime(2015, 1, 12, 10, 5, 0)) == 300
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
        datetime(2015, 1, 12, 11, 10, 10),
    ],
    datetime(2015, 1, 12, 11, 5, 0),
    datetime(2015, 1, 12, 12, 0, 0)) == 310
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
    ],
    datetime(2015, 1, 12, 11, 5, 0),
    datetime(2015, 1, 12, 11, 10, 0)) == 300
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
    ],
    datetime(2015, 1, 12, 10, 10, 0),
    datetime(2015, 1, 12, 11, 0, 10)) == 20
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 10, 10),
        datetime(2015, 1, 12, 11, 0, 0),
    ],
    datetime(2015, 1, 12, 9, 10, 0),
    datetime(2015, 1, 12, 10, 20, 20)) == 610
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
    ],
    datetime(2015, 1, 12, 9, 10, 0),
    datetime(2015, 1, 12, 10, 20, 20)) == 1220
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
    ],
    datetime(2015, 1, 12, 9, 9, 0),
    datetime(2015, 1, 12, 10, 0, 0)) == 0
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
    ],
    datetime(2015, 1, 12, 9, 9, 0),
    datetime(2015, 1, 12, 10, 0, 10)) == 10
    
    print("Start and End testing Complete")


if __name__ == '__main__':
    print("Multi-lighbulb test:")

    print(sum_light(els=[
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], start_watching=datetime(2015, 1, 12, 10, 0, 0), end_watching=datetime(2015, 1, 12, 10, 1, 0)))

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        (datetime(2015, 1, 12, 10, 0, 0), 2),
        datetime(2015, 1, 12, 10, 0, 10),
        (datetime(2015, 1, 12, 10, 1, 0), 2),
    ]) == 60

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        datetime(2015, 1, 12, 10, 0, 10),
        (datetime(2015, 1, 12, 11, 0, 0), 2),
        (datetime(2015, 1, 12, 11, 1, 0), 2),
    ]) == 70

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ]) == 30
    
    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ]) == 40

    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
        (datetime(2015, 1, 12, 10, 1, 0), 3),
        (datetime(2015, 1, 12, 10, 1, 20), 3),
    ]) == 60

    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        (datetime(2015, 1, 12, 10, 0, 0), 2),
        datetime(2015, 1, 12, 10, 0, 10),
        (datetime(2015, 1, 12, 10, 1, 0), 2),
    ], datetime(2015, 1, 12, 10, 0, 50)) == 10
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], datetime(2015, 1, 12, 10, 0, 30)) == 20
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], datetime(2015, 1, 12, 10, 0, 20)) == 30
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], datetime(2015, 1, 12, 10, 0, 10)) == 30
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], datetime(2015, 1, 12, 10, 0, 50)) == 0
    
    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], datetime(2015, 1, 12, 10, 0, 30)) == 20
    
    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], datetime(2015, 1, 12, 10, 0, 20)) == 30
    
    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
        (datetime(2015, 1, 12, 10, 1, 20), 2),
        (datetime(2015, 1, 12, 10, 1, 40), 2),
    ], datetime(2015, 1, 12, 10, 0, 20)) == 50
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        (datetime(2015, 1, 12, 10, 0, 0), 2),
        datetime(2015, 1, 12, 10, 0, 10),
        (datetime(2015, 1, 12, 10, 1, 0), 2),
    ], datetime(2015, 1, 12, 10, 0, 30), datetime(2015, 1, 12, 10, 1, 0)) == 30
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        (datetime(2015, 1, 12, 10, 0, 0), 2),
        datetime(2015, 1, 12, 10, 0, 10),
        (datetime(2015, 1, 12, 10, 1, 0), 2),
    ], datetime(2015, 1, 12, 10, 0, 20), datetime(2015, 1, 12, 10, 1, 0)) == 40
    
    assert sum_light([
        datetime(2015, 1, 12, 10, 0, 0),
        (datetime(2015, 1, 12, 10, 0, 0), 2),
        datetime(2015, 1, 12, 10, 0, 10),
    ], datetime(2015, 1, 12, 10, 0, 0), datetime(2015, 1, 12, 10, 0, 30)) == 30
    
    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], datetime(2015, 1, 12, 10, 0, 0), datetime(2015, 1, 12, 10, 1, 0)) == 40
    
    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], datetime(2015, 1, 12, 10, 0, 0), datetime(2015, 1, 12, 10, 0, 10)) == 0
    
    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
        datetime(2015, 1, 12, 10, 0, 40),
        (datetime(2015, 1, 12, 10, 0, 50), 2),
    ], datetime(2015, 1, 12, 10, 0, 10), datetime(2015, 1, 12, 10, 0, 20)) == 10
    

    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
    ], datetime(2015, 1, 12, 10, 0, 10), datetime(2015, 1, 12, 10, 0, 20)) == 10
    
    assert sum_light([
        (datetime(2015, 1, 12, 10, 0, 10), 3),
        datetime(2015, 1, 12, 10, 0, 20),
        (datetime(2015, 1, 12, 10, 0, 30), 3),
        (datetime(2015, 1, 12, 10, 0, 30), 2),
    ], datetime(2015, 1, 12, 10, 0, 10), datetime(2015, 1, 12, 10, 0, 30)) == 20    

    assert sum_light(els=[
        (datetime(2015, 1, 11, 0, 0, 0), 3),
        datetime(2015, 1, 12, 0, 0, 0),
        (datetime(2015, 1, 13, 0, 0, 0), 3),
        (datetime(2015, 1, 13, 0, 0, 0), 2),
        datetime(2015, 1, 14, 0, 0, 0),
        (datetime(2015, 1, 15, 0, 0, 0), 2),
    ], start_watching=datetime(2015, 1, 10, 0, 0, 0), end_watching=datetime(2015, 1, 16, 0, 0, 0)) == 345600

    print("Multi-lighbulb test is completed!")
