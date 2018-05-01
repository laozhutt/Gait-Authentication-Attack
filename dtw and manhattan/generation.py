"""
Cycle generation from data set 774

author: cyrus and tiantian
date: 2018-4-20
"""

import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
import os

import sys

ROOT = '/home/tiantian/onecycleattack/mimicry-master/experiment/cycle_generation_from_dataset_774'
RESULTS_DIR = 'results'  # relative
DATA_SET_DIR = 'AutomaticExtractionData_IMUZCenter'  # relative
sys.path.append(ROOT)

from cycle_detection import tools as tool
from cycle_detection.actions2 import CycleDetectionAction


class CycleGeneration(CycleDetectionAction):
    def get_data(self, file_path):
        """
        Cannot show the details of data set because of the agreement signed.
        """
        raw_data = np.loadtxt(file_path, delimiter=',', skiprows=2).reshape(-1, 6)
        timestamps = np.arange(0, raw_data.shape[0] / self.sample_rate, 1 / self.sample_rate)
        data = [raw_data[:, i].tolist() for i in range(3, 6)]
        if len(timestamps) > len(data):
            timestamps = timestamps[:len(data[0])]

        return timestamps, data

    def show(self, timestamps, data, timestamps_interpolated=None, data_magnitude=None, indices=None):
        plt.figure()

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

        target_dir = os.path.join(ROOT, RESULTS_DIR, 'cycle_detection_pics')
        if not os.path.exists(target_dir):
            os.system('mkdir -p {0}'.format(target_dir))
        plt.savefig(os.path.join(target_dir,  self.get_filename()))
        # plt.show()
        plt.close()

    def save_splitted_data(self, data_splitted):
        target_dir = os.path.join(ROOT, RESULTS_DIR, 'data_splitted', self.get_filename())
        if not os.path.exists(target_dir):
            os.system('mkdir -p {0}'.format(target_dir))
        for i, data in enumerate(data_splitted):
            with open(os.path.join(target_dir, str(i)), 'w') as f:
                for line in data:
                    f.write(','.join([str(d) for d in line]))
                    f.write('\n')
                    f.flush()
        print('>>> write done, count of cycles is {0}'.format(len(data_splitted)))

    # modified by tiantian, get the normalized cycle for each person (101 points)
    def save_splitted_magnitude_data(self, data_magnitude_splitted):
        # plt.figure()
        target_dir = os.path.join(ROOT, RESULTS_DIR, 'data_magnitude_splitted', self.get_filename())
        if not os.path.exists(target_dir):
            os.system('mkdir -p {0}'.format(target_dir))
        for i, data in enumerate(data_magnitude_splitted):
            timestamps = np.arange(0, 1.1, 1.0 / (len(data) - 1))
            if len(timestamps) > len(data):
                timestamps = timestamps[:len(data)]
            timestamps_interpolated, data_interpolated = \
            tool.get_interpolation(timestamps, data, target_sample_rate=self.sample_rate)   #get 101 sample totally
            with open(os.path.join(target_dir, str(i)), 'w') as f:
                for line in data_interpolated[0]:
                    #print line
                    f.write(str(line))
                    f.write('\n')
                    f.flush()
            # plt.plot(timestamps_interpolated, data_interpolated[0])
            # target_magnitude_dir = os.path.join(ROOT, RESULTS_DIR, 'cycle_magnitude_detection_pics',str(i))
            # if not os.path.exists(target_magnitude_dir):
            #     os.system('mkdir -p {0}'.format(target_magnitude_dir))
            # plt.savefig(os.path.join(target_magnitude_dir, self.get_filename()))
            # plt.close()
        print('>>> write done, count of cycles is {0}'.format(len(data_magnitude_splitted)))





if __name__ == '__main__':
    file_paths = os.listdir(os.path.join(ROOT, DATA_SET_DIR))

    for file_path in file_paths:
        print('>>> file name: {0}'.format(file_path))
        cycle_generation = CycleGeneration(
            os.path.join(ROOT, DATA_SET_DIR, file_path),
            sample_rate=100.0,
            subset_size=80,
            # debug=True,
        )

        cycle_generation.action()
