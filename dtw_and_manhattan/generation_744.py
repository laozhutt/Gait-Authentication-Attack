"""
Cycle generation from data set 774

author: cyrus
date: 2018-4-20
"""

import numpy as np
import os

import sys

ROOT = '/home/tiantian/onecycleattack/Gait-Authentication-Attack/dtw_and_manhattan'
sys.path.append(ROOT)

from cycle_detection import tools
from cycle_detection.actions import CycleDetectionAction


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


if __name__ == '__main__':
    RESULTS_DIR_PIC = os.path.join(ROOT, 'results/744_cycle_detection_pics')
    RESULTS_DIR_DAT = os.path.join(ROOT, 'results/744_data_splitted')
    RESULTS_DIR_MAG_DAT = os.path.join(ROOT, 'results/744_data_magnitude_splitted')
    DATA_SET_DIR = os.path.join(ROOT, 'dataset/744_dataset_catalog')

    # check
    tools.check_result_dir(RESULTS_DIR_PIC)
    tools.check_result_dir(RESULTS_DIR_DAT)
    tools.check_result_dir(RESULTS_DIR_MAG_DAT)


    if not os.path.exists(DATA_SET_DIR):
        raise Exception('there is no dataset'.format(DATA_SET_DIR))

    user_names = os.listdir(DATA_SET_DIR)
    for user_name in user_names:
        dir_path = os.path.join(DATA_SET_DIR, user_name)
        file_paths = [os.path.join(dir_path, file_path) for file_path in os.listdir(dir_path)]

        for file_path in file_paths:
            print('>>> file name: {0}'.format(file_path))
            cycle_generation = CycleGeneration(
                os.path.join(DATA_SET_DIR, file_path),
                sample_rate=100.0,
                subset_size=80,
                # debug=True,
                smoothing_factor=0.3
            )
            cycle_generation.action(remove_odd=True)
            # show and save
            path = os.path.join(RESULTS_DIR_PIC, cycle_generation.get_filename())
            # tools.show_cycles_by_time(
            #     cycle_generation.timestamps,
            #     cycle_generation.data,
            #     cycle_generation.real_indices,
            # )
            tools.show_cycles_by_time(
                cycle_generation.timestamps_interpolated,
                cycle_generation.data_magnitude,
                cycle_generation.indices,
                save=True,
                path=path
            )
            print('>>> save pic: {0}'.format(path))
            tools.show_cycles(cycle_generation.data, cycle_generation.real_indices)
            cycle_generation.save_splitted_data(RESULTS_DIR_DAT)
            cycle_generation.save_splitted_magnitude_data(RESULTS_DIR_MAG_DAT)
