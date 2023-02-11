import multiprocessing
import numpy as np
import itertools

def read_input(name):
    f = open(name)
    sensors = []
    beacons = []
    for line in f:
        tokens = line.split()
        nums = []
        for token in tokens:
            if "=" in token:
                token_split = token.split("=")
                num = int(token_split[1].replace(":", "").replace(",", ""))
                nums.append(num)
        sensors.append((nums[0], nums[1]))
        beacons.append((nums[2], nums[3]))

    return sensors, beacons

def manhattan_distance(sensor, beacon):
    return sum([abs(sensor[j] - beacon[j]) for j in range(2)])

def sensor_coverage_row(sensor, row, beacon):
    dist = manhattan_distance(sensor, beacon)
    center = sensor[0]
    width = dist - abs(sensor[1] - row)
    coverage = list(range(center - width, center + width + 1))

    return coverage

def beacon_col(beacon, row):
    if beacon[1] == row:
        return beacon[0]
    else:
        return None

def row_coverage(row, sensors, beacons):
    print(row)
    rows = [row]*len(sensors)
    coverage = list(map(sensor_coverage_row, sensors, rows, beacons))
    coverage_set = set(itertools.chain(*coverage))
    beacon_blockage_set = set(map(beacon_col, beacons, rows))
    coverage_set -= beacon_blockage_set
    return coverage_set

def aoc15a(name, row):
    sensors, beacons = read_input(name)
    coverage = row_coverage(row, sensors, beacons)
    print(len(coverage))

def manage_coverage_row(row, coverage_row):
    empty_row = []
    for col in range(len(coverage_row)):
        if col not in coverage_row:
            empty_row.append((col, row))

    return empty_row

def aoc15b(name, dim):
    global pool
    pool = multiprocessing.Pool()

    sensors, beacons = read_input(name)
    global MAX_DIM
    MAX_DIM = dim
    rows = np.arange(MAX_DIM)
    sensors_arr = np.tile(np.array(sensors), (MAX_DIM, 1, 1))
    beacons_arr = np.tile(np.array(beacons), (MAX_DIM, 1, 1))
    arg = zip(rows, sensors_arr, beacons_arr)
    coverage = list(pool.starmap(row_coverage, arg))

    arg = zip(rows, coverage)
    empty_pos_list = list(pool.starmap(manage_coverage_row, arg))
    empty_pos_set = set(itertools.chain(*empty_pos_list))
    beacon_set = set(beacons)
    empty_pos_set -= beacon_set
    print(empty_pos_set)

    #pool.close()
    #pool.join()

if __name__ ==  '__main__':

    #aoc15a("input15_test.txt", 11)
    #aoc15a("input15.txt", 2000000)
    #aoc15b("input15_test.txt", 20)
    aoc15b("input15.txt", 4000000)