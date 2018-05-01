"""
Tools for cycle detection

author: cyrus and tiantian
date: 2018-4-19
"""
import numpy as np
from scipy import interpolate
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw


def get_interpolation(timestamps, data, target_sample_rate=50, method='linear'):
    """Get interpolation or down-sampling according to timestamps and data.

    :param timestamps: [0 or 0.0, 0.02, 0.03, ...]
    :param data: N-D array or an array.
    :param target_sample_rate: default=50HZ
    :param method: default=linear
    :return: Interpolation or down-sampling result.
    """
    # Remove offset.
    offset = timestamps[0]
    if offset != 0 or offset != 0.0:
        timestamps = [timestamp - offset for timestamp in timestamps]

    # Evaluate interpolations with target timestamps.
    interval = 1.0 / target_sample_rate

    target_timestamps = np.arange(0, timestamps[-1] + interval / 2, interval).tolist()  # construct target timestamps
    target_timestamps[-1] = min(target_timestamps[-1], timestamps[-1]) # avoid overflow caused by interval/2

    if not isinstance(data[0], (tuple, list)):
        data = [data]
    assert len(data) != 0, 'data can not be empty'

    evaluate_interpolations = [interpolate.interp1d(timestamps, d) for d in data]  # get evaluation functions
    target_data = [e_i(target_timestamps).tolist() for e_i in evaluate_interpolations]  # evaluate


    return target_timestamps, target_data


def get_exponential_moving_average_order_1(data, factor):
    """Perform order-1 exponential moving average on data.

    :param data: An array.
    :param factor: Smoothing factor.
    :return: An array after smoothing.
    """
    data_smoothed = [data[0]] # there are several other strategies for setting up value of the first
    for i in range(1, len(data)):
        t = data[i] * factor + data_smoothed[i - 1] * (1 - factor)  # as formula
        data_smoothed.append(t)

    return data_smoothed


def get_exponential_moving_average_order_3(data, factor):
    """Perform order-3 exponential moving average on data.

    :param data: An array.
    :param factor: Smoothing factor.
    :return: An array.
    """
    data_order_1 = get_exponential_moving_average_order_1(data, factor)
    data_order_2 = get_exponential_moving_average_order_1(data_order_1, factor)
    return get_exponential_moving_average_order_1(data_order_2, factor)


def get_weighted_moving_average(data, factor):
    """Perform weighted moving average.

    :param data: N-D array or an array.
    :param factor: Smoothing factor.
    :return: N-D data smoothed.
    """
    if not isinstance(data[0], (tuple, list)):
        data = [data]
    assert len(data) != 0, 'data can not be empty'

    # exponential moving average order 3
    return [get_exponential_moving_average_order_3(d, factor) for d in data]


def get_magnitude(data):
    """Get magnitude by time axis.

    :param data: N-D array or an array.
    :return: An array which is magnitude(data).
    """
    if not isinstance(data[0], (tuple, list)):
        data = [data]
    assert len(data) != 0, 'data can not be empty'

    return np.sqrt(np.sum(np.square(data), axis=0)).tolist()


def remove_odd_cycles(data, indices):
    """Remove odd cycles as paper says.

    :param data: An array.
    :param indices: Indices found by cycle detection.
    :return: Indices removing odd ones.
    """
    # TODO this function is time-consuming
    # Calculate DWT matrix.
    distances = []
    for (start_x, end_x) in indices:
        for (start_y, end_y) in indices:
            distance, _ = fastdtw(data[start_x: end_x], data[start_y: end_y], dist=euclidean)
            distances.append(distance)

    distances_matrix = np.array(distances).reshape(-1, len(indices)).tolist()

    # Calculate DWT matrix's mean and std which are defined in paper.
    distances = []
    for distances_row in distances_matrix:
        distances.append(np.sum(distances_row) / (len(indices) - 1))
    mean = np.mean(distances)
    std = np.std(distances)

    # Get indices to be removed which are not in [mean-2*std, mean+2*std].
    to_be_removed = []
    for i, distance in enumerate(distances):
        if distance < mean - 2 * std or distance > mean + 2 * std:
            to_be_removed.append(i)

    # Remove these abnormal indices.
    indices_result = []
    for index in indices:
        if index in to_be_removed:
            continue
        else:
            indices_result.append(index)

    return indices_result


def get_splitted_data(data, indices):
    """Return splitted data according to indices.

    :param data: N-D array.
    :param indices: Indices denote start and end of cycles.
    :return: Return splitted data according to indices.
    """
    data = np.array(data).T
    return [data[start:end, :].tolist() for (start, end) in indices]

def get_splitted_magnitude_data(data, indices):
    """Return splitted magnitude data according to indices.

    :param data: 1-D array.
    :param indices: Indices denote start and end of cycles.
    :return: Return splitted magnitude data according to indices.
    """
    data = np.array(data).T
    return [data[start:end].tolist() for (start, end) in indices]

def cal_fastdtw(cycle1, cycle2):
    """Return fast dtw distance of the two cycles.

    :param cycle1: the first cycle stored the normalized maginitude data.
    :param cycle2: the second cycle stored the normalized maginitude data.
    :return: Return the dtw distance. NOte: when the lengths of the data in two cycle is the same, dtw and manhattan are the same.
    """

    min_distance, path = fastdtw(cycle1, cycle2, dist=euclidean)
    
    # for i in range(len(cycle1)):
    #     distance, path = fastdtw(np.roll(cycle1,i), cycle2, dist=euclidean)
    #     if distance < min_distance:
    #         min_distance = distance
    return min_distance


