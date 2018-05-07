"""
How to detect cycles.

author: cyrus
date: 2018-4-20
"""
from detection import CycleDetection
import tools
import numpy as np
import os


class CycleDetectionAction:

    def __init__(self, file_path, sample_rate=33.0, smoothing_factor=0.6, subset_size=20, debug=False):
        self.file_path = file_path

        self.sample_rate = float(sample_rate)
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
        self.real_indices = []

        self.data_splitted = None
        self.data_magnitude_splitted = None

    def get_data(self, file_path):
        raw_data = np.loadtxt(file_path, delimiter=',').reshape(-1, 4)
        timestamps = raw_data[:, 0].tolist()
        data = [raw_data[:, i].tolist() for i in range(1, 4)]

        return timestamps, data

    def save_splitted_data(self, result_dir):
        target_dir = os.path.join(result_dir, self.get_username(), self.get_session_name())
        tools.check_result_dir(target_dir)

        for i, data in enumerate(self.data_splitted):
            with open(os.path.join(target_dir, str(i)), 'w') as f:
                for line in data:
                    f.write(','.join([str(d) for d in line]))
                    f.write('\n')
                    f.flush()
        print('>>> write done, count of cycles is {0}'.format(len(self.data_splitted)))

    # modified by tiantian, get the normalized cycle for each person (101 points)
    def save_splitted_magnitude_data(self, result_dir):
        target_dir = os.path.join(result_dir, self.get_username(), self.get_session_name())
        tools.check_result_dir(target_dir)
        for i, data in enumerate(self.data_magnitude_splitted):
            timestamps = np.arange(0, 1.1, 1.0 / (len(data) - 1))
            if len(timestamps) > len(data):
                timestamps = timestamps[:len(data)]
            if len(timestamps) == 0:
                continue
            timestamps_interpolated, data_interpolated = \
            tools.get_interpolation(timestamps, data, target_sample_rate=self.sample_rate)   #get 101 sample totally
            with open(os.path.join(target_dir, str(i)), 'w') as f:
                for line in data_interpolated[0]:
                    #print line
                    f.write(str(line))
                    f.write('\n')
                    f.flush()

        print('>>> write done, count of cycles is {0}'.format(len(self.data_magnitude_splitted)))

    def get_filename(self):
        return '_'.join(self.file_path.split('/')[-2:])

    def get_username(self):
        return self.file_path.split('/')[-2]

    def get_session_name(self):
        return self.file_path.split('/')[-1]

    def action(self, remove_odd=False):
        # 1. Get data and timestamps.
        self.timestamps, self.data = self.get_data(self.file_path)

        # 2. Interpolation
        self.timestamps_interpolated, self.data_interpolated = \
            tools.get_interpolation(self.timestamps, self.data, target_sample_rate=self.sample_rate)

        # [optional]
        # save data into a new file

        # 3 Weighted moving average.
        self.data_smoothed = tools.get_weighted_moving_average(self.data_interpolated, self.smoothing_factor)

        # 4 Get magnitude.
        self.data_magnitude = tools.get_magnitude(self.data_smoothed)

        # 5 Detect cycles.
        detection = CycleDetection(self.data_magnitude, subset_size=self.subset_size, debug=self.debug)
        self.indices = detection.get_cycle_boundary_indices()

        # [optional]
        # save indices into a new file

        # 6 Remove odd cycles.
        if remove_odd:
            self.indices = tools.remove_odd_cycles(self.data_magnitude, self.indices)  # time-consuming!!!

        # 7 Remove offset in indices.
        factor = float(len(self.timestamps)) / float(len(self.timestamps_interpolated))
        for i in range(0, len(self.indices)):
            start = int((self.indices[i][0] - 5) * factor)
            end = int((self.indices[i][1] - 5) * factor)
            self.real_indices.append((start, end))

        # 7 Get splitted data.
        self.data_splitted = tools.get_splitted_data(self.data, self.real_indices)

        # modified by tiantian, 1D interpolation on magnitude data, each cycle is normalized to a length of k observations, k = 100
        self.data_magnitude_splitted = tools.get_splitted_magnitude_data(self.data_magnitude, self.indices)  #smoothed data
        #self.data_magnitude_splitted = tools.get_splitted_magnitude_data(tools.get_magnitude(self.data), self.real_indices) #original data


if __name__ == '__main__':
    file_path = './test_data'
    print('>>> file name: {0}'.format(file_path))
    cycle_generation = CycleDetectionAction(
        file_path,
        sample_rate=100.0,
        subset_size=80,
        smoothing_factor=0.3
    )
    cycle_generation.action(remove_odd=True)
    # show and save
    tools.show_nd(
        cycle_generation.timestamps,
        cycle_generation.data
    )
    tools.show_cycles_by_time(
        cycle_generation.timestamps,
        cycle_generation.data,
        cycle_generation.real_indices,
        title='original',
        save=True,
        path=os.path.join('results', 'original')
    )
    tools.show_cycles_by_time(
        cycle_generation.timestamps_interpolated,
        cycle_generation.data_magnitude,
        cycle_generation.indices,
        title='magnitude',
        save=True,
        path=os.path.join('results', 'magnitude')
    )
    tools.show_cycles(
        cycle_generation.data, cycle_generation.real_indices,
        title='cycles',
        save=True,
        path=os.path.join('results', 'cycles')
    )
