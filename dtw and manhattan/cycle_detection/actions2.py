"""
How to detect cycles.

author: cyrus and tiantian
date: 2018-4-20
"""
from detection import CycleDetection
import tools as tool
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_RATE = 33.0  # float
SMOOTHING_FACTOR = 0.6  # [0, 1]
SUBSET_SIZE = 20  # less than sample_rate * 0.8, but can not be too small


class CycleDetectionAction:

    def __init__(self, file_path, sample_rate=33.0, smoothing_factor=0.6, subset_size=20, debug=False):
        self.file_path = file_path

        self.sample_rate = sample_rate
        self.smoothing_factor = smoothing_factor
        self.subset_size = subset_size
        self.debug = debug

        self.timestamps = None
        self.timestamps_interpolated = None

        self.data = None
        self.data_magnitude = None
        self.data_interpolated = None
        self.data_smoothed = None

        self.indices = None

    def get_data(self, file_path):
        raw_data = np.loadtxt(file_path, delimiter=',').reshape(-1, 4)
        timestamps = raw_data[:, 0].tolist()
        data = [raw_data[:, i].tolist() for i in range(1, 4)]

        return timestamps, data

    def show(self, timestamps, data, timestamps_interpolated=None, data_magnitude=None, indices=None):
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
                x = [timestamps_interpolated[c] for c in cycle]
                y = [data_magnitude[c] for c in cycle]
                plt.plot(x, y)
        plt.show()

    def save_splitted_data(self, data_splitted):
        pass

    def save_splitted_magnitude_data(self, data_magnitude_splitted):
        pass

    def get_filename(self):
        return self.file_path.split('/')[-1].split('.')[0]

    def action(self):
        # 1. Get data and timestamps.
        self.timestamps, self.data = self.get_data(self.file_path)

        # 2. Interpolation
        self.timestamps_interpolated, self.data_interpolated = \
            tool.get_interpolation(self.timestamps, self.data, target_sample_rate=self.sample_rate)
        # self.show(self.timestamps_interpolated, self.data_interpolated)

        # [optional]
        # save data into a new file

        # 3 Weighted moving average.
        self.data_smoothed = tool.get_weighted_moving_average(self.data_interpolated, self.smoothing_factor)

        # 4 Get magnitude.
        self.data_magnitude = tool.get_magnitude(self.data_smoothed)

        # [optional]
        # save data into a new file

        # 5 Detect cycles.
        detection = CycleDetection(self.data_magnitude, subset_size=SUBSET_SIZE, debug=self.debug)
        self.indices = detection.get_cycle_boundary_indices()

        # [optional]
        # save indices into a new file

        # 6 Remove odd cycles
        self.indices = tool.remove_odd_cycles(self.data_magnitude, self.indices)  # time-consuming!!!




        # Show original data and cycle detection results.
        self.show(self.timestamps_interpolated, self.data_magnitude, indices=self.indices)

        # 7 Get splitted data.
        #data_splitted = tool.get_splitted_data(self.data, self.indices)

        # modified by tiantian, 1D interpolation on magnitude data, each cycle is normalized to a length of k observations, k = 100
        data_magnitude_splitted = tool.get_splitted_magnitude_data(self.data_magnitude, self.indices)

        # [optional]
        # save data into a new file
        #self.save_splitted_data(data_splitted)
        self.save_splitted_magnitude_data(data_magnitude_splitted)


if __name__ == '__main__':
    action = CycleDetectionAction(
        '/home/cyrus/Public/mimicry/cycle_detection/test_data.csv'
    )
    action.action()
