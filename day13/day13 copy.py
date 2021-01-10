import sys
from pprint import pprint
from itertools import count
import time

if __name__ == "__main__":
    filename = sys.argv[1]

    contents = open(filename).readlines()

    timestamp = int(contents[0])
    bus_ids = [int(bus_id) for bus_id in contents[1].split(",") if bus_id != "x"]

    offsets = [
        idx for idx, bus_id in enumerate(contents[1].split(",")) if bus_id != "x"
    ]

    first = bus_ids[0]
    step = count(1)
    offsets[0] = first

    while True:
        # We only need to check multiples of our first bus_id
        i = first * next(step)
        if all(
            bus_id - i % bus_id == offset for bus_id, offset in zip(bus_ids, offsets)
        ):
            print("timestamp={}", i)
            break

        # Part 1
        # departs = [id for id in ids if round % id == 0]
        # if round >= timestamp and len(departs) > 0:
        #     waits = round - timestamp
        #     print(f"{departs=} {round=} waits={waits} {departs[0]*waits}")
        #     break
