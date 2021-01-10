import sys
from pprint import pprint
from itertools import count
from typing import Tuple, Sequence
from multiprocessing import Pool, cpu_count, Process, Queue
from pprint import pprint

import time


def run_sim(
    bus_ids: Sequence[int],
    offsets: Sequence[int],
    start: int,
    stop: int,
    max_val: int,
    max_val_offset: int,
) -> int:

    for multiple in range(start, stop):
        # We only need to check multiples of our largest bus_id
        timestamp = max_val * multiple - max_val_offset
        temp = tuple(
            bus_id - timestamp % bus_id == offset
            for bus_id, offset in zip(bus_ids[1:], offsets[1:])
        )
        if all(temp) and timestamp % bus_ids[0] == 0:
            print("timestamp={}", timestamp)
            return timestamp

    return None


if __name__ == "__main__":
    start_time = time.time()

    filename = sys.argv[1]

    contents = open(filename).readlines()

    timestamp = int(contents[0])
    bus_ids = [int(bus_id) for bus_id in contents[1].split(",") if bus_id != "x"]

    offsets = [
        idx for idx, bus_id in enumerate(contents[1].split(",")) if bus_id != "x"
    ]

    offset_lookup = {
        int(bus_id): offset
        for offset, bus_id in enumerate(contents[1].split(","))
        if bus_id != "x"
    }

    largest_bus_id = max(bus_ids)
    largest_bus_id_offset = offset_lookup[largest_bus_id]
    offsets[0] = largest_bus_id

    # Make immutable just in case
    bus_ids = tuple(bus_ids)
    offsets = tuple(offsets)

    chunk_size = 100_000
    chunk_start = 1
    chunk_stop = chunk_size + 1

    pool_size = cpu_count()
    pool = Pool(pool_size)

    while True:

        result = run_sim(
            bus_ids,
            offsets,
            chunk_start,
            chunk_stop,
            largest_bus_id,
            largest_bus_id_offset,
        )

        args = []
        for _ in range(pool_size):
            args.append(
                (
                    bus_ids,
                    offsets,
                    chunk_start,
                    chunk_stop,
                    largest_bus_id,
                    largest_bus_id_offset,
                )
            )

            chunk_start += chunk_size
            chunk_stop += chunk_size

        result = pool.starmap_async(run_sim, args)
        results = result.get()

        if any(output != None for output in results):
            break

    print("results={}", results)
    stop_time = time.time()
    elapsed = stop_time - start_time

    print("took %s seconds" % elapsed)
