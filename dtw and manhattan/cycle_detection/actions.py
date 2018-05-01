"""
How to detect cycles.

author: cyrus
date: 2018-4-19
"""
from detection import CycleDetection
import os
import tools as tool
import numpy as np
import matplotlib.pyplot as plt

ROOT = '.'
SAMPLE_RATE = 33.0  # float
SMOOTHING_FACTOR = 0.6  # [0, 1]
SUBSET_SIZE = 20  # less than sample_rate * 0.8, but can not be too small


def get_data(file_path):
    raw_data = np.loadtxt(file_path, delimiter=',').reshape(-1, 4)
    timestamps = raw_data[:, 0].tolist()
    data = [raw_data[:, i].tolist() for i in range(1, 4)]

    return timestamps, data


def show(timestamps, data, timestamps_interpolated=None, data_magnitude=None, indices=None):
    if not isinstance(data[0], (tuple, list)):
        data = [data]
    for d in data:
        plt.plot(timestamps, d)

    if timestamps_interpolated is not None and data_magnitude is not None:
        plt.plot(timestamps_interpolated, data_magnitude)
    else:
        timestamps_interpolated = timestamps
        data_magnitude = tool.get_magnitude(data)

    if indices is not None:
        for cycle in indices:
            print(cycle)
            x = [timestamps_interpolated[c] for c in cycle]
            y = [data_magnitude[c] for c in cycle]
            plt.plot(x, y)
    plt.show()


def main():
    # 1. Get data and timestamps.
    file_path = os.path.join(ROOT, 'test_data.csv')

    timestamps, data = get_data(file_path)
    # show(timestamps, data)

    # 2. Interpolation
    timestamps_interpolated, data_interpolated = \
        tool.get_interpolation(timestamps, data, target_sample_rate=SAMPLE_RATE)
    # show(timestamps_interpolated, data_interpolated)

    # [optional]
    # save data into a new file

    # 3 Weighted moving average.
    data_smoothed = tool.get_weighted_moving_average(data_interpolated, SMOOTHING_FACTOR)

    # 4 Get magnitude.
    data_magnitude = tool.get_magnitude(data_smoothed)

    # [optional]
    # save data into a new file

    # 5 Detect cycles.
    detection = CycleDetection(data_magnitude, subset_size=SUBSET_SIZE)
    indices = detection.get_cycle_boundary_indices()

    # [optional]
    # save indices into a new file

    # 6 Remove odd cycles
    # indices = tool.remove_odd_cycles(data_magnitude, indices)  # time-consuming!!!

    # Show original data and cycle detection results.
    show(timestamps_interpolated, data_magnitude, indices=indices)

    # 7 Get splitted data.
    data_splitted = tool.get_splitted_data(data, indices)

    # [optional]
    # save data into a new file


if __name__ == '__main__':
    main()
