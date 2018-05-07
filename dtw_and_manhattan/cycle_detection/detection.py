"""
Core of cycle detection.

author: cyrus
date: 2018-4-19
"""
import scipy.spatial.distance as distance
import numpy as np

from cycle_detection import tools


class CycleDetection:
    def __init__(self, data, subset_size=70, debug=False):
        """
        :param data: A 1-D list.
        :param subset_size: Size of subset used to find the cycle length. This
        size should be smaller than the regular cycle length. The size and the
        length both depends on sample rate. Default size is 70 samples at a
        sample rate of 100HZ.
        """
        if len(data) == 0:
            raise ValueError('current data is empty')

        self.serial = data
        self.serial_length = len(data)

        self.subset_size = subset_size
        if self.subset_size >= self.serial_length:
            raise ValueError('current subset_size {0} is larger than length of data'.format(subset_size))

        # Only for test.
        self.baseline = None
        self.euclidean = []
        self.minimums = []
        self.cycle_boundary_indices = []
        self.debug = debug

        # relation of params
        # |-----------------------------------------------------------------------|---> x
        # |<---------cycle_length --------------------------->|<------offset----->|
        # |<-----cycle_length - offset---->|<-----offset----->|<------offset----->|
        # |<-----cycle_length - offset---->|<-interval->|<-interval->|<-interval->|
        # |<------------------------------>|<-invalid-->|<--valid--->|<-invalid-->|

        # Get estimation of walking cycle length(samples) with distance scores.
        self.cycle_length = int(self.get_cycle_length_estimation())  # get cycle_length as paper says
        if self.cycle_length <= 20:
            raise RuntimeWarning('current length of data is {0}, more than 10 is better'.format(self.cycle_length))
        self.offset = int(np.ceil(self.cycle_length * 0.1))
        self.interval = 2 * self.offset / 3
        print('>>> serial length: {0}'.format(self.serial_length))
        print('>>> cycle_length: {0}'.format(self.cycle_length))
        print('>>> offset: {0}'.format(self.offset))
        print('>>> interval: {0}'.format(self.interval))

        self.count = 0  # count of cycles we find

    def get_cycle_length_estimation(self):
        """Get estimation of walking cycle length(samples) with distance scores.

        :return: Return the estimation of walking cycle length(samples).
        """

        # Find a baseline area around the center of this serial.
        start = self.serial_length / 2 - self.subset_size / 2
        end = start + self.subset_size
        baseline = self.serial[start: end]
        self.baseline = baseline  # only for test

        # Calculate the distance scores bidirectionally.
        # Algorithm 1
        right_minimums = self.get_local_minimum_indices(end, self.serial_length, baseline)  # [start, end) [end, ...
        left_minimums = self.get_local_minimum_indices(0, start, baseline)  # [0, start), [start, ...
        cycle_length1 = np.mean([start - left_minimums[-1], right_minimums[0] - start])

        # Algorithm 2
        dist = self.get_distance_to_subset(baseline)
        dist = tools.get_exponential_moving_average_order_3(dist, 0.3)
        dist = tools.get_exponential_moving_average_order_3(dist, 0.3)
        minimums = self.get_local_minimum_indices_new(dist, 0, len(dist))
        for i in range(0, len(minimums)):
            minimums[i] -= 5
        cycle_length = int(np.mean(np.diff(minimums)))

        print '>>>', 'cycle length', 'old way', cycle_length1, 'new', cycle_length

        return cycle_length

    def get_distance_to_subset(self, baseline):
        distance_ = []
        for i in range(0, self.serial_length - len(baseline)):
            distance_.append(distance.euclidean(baseline, self.serial[i: i + len(baseline)]))
        return distance_

    @staticmethod
    def get_local_minimum_indices_new(data, start, end):
        local_minimum_indices = []
        for i in range(start, end - 1):
            if data[i - 1] > data[i] and data[i + 1] > data[i]:
                local_minimum_indices.append(i)
        if len(local_minimum_indices) == 0:  # monotony
            local_minimum_indices.append(data.index(min(data[start], data[end - 1])))

        return local_minimum_indices

    def get_local_minimum_indices(self, start, end, baseline=None):
        """Get indices to local minimums of euclidean distance

        :param start: Start of a serial.
        :param end: End of a serial.
        :param baseline: Baseline used compare with [start: end] of target data. If None, return the indices
        :return: A list contains global indices to local minimums.
        """
        if baseline is None:
            distance_ = self.serial[start: end]
        else:
            distance_ = []
            for i in range(start, end - self.subset_size):
                distance_.append(distance.euclidean(baseline, self.serial[i: i + self.subset_size]))
            self.euclidean.append(distance_)  # only for test

        local_minimum_indices = []
        # TODO if there are two consecutive same points?
        for i in range(1, len(distance_) - 1):
            if distance_[i - 1] > distance_[i] and distance_[i + 1] > distance_[i]:
                local_minimum_indices.append(i + start)
        if len(local_minimum_indices) == 0:  # monotony
            local_minimum_indices.append(distance_.index(min(distance_[0], distance_[-1])) + start)

        self.minimums.append(local_minimum_indices)  # only for test

        return local_minimum_indices

    def is_valid_minimum_index(self, start, end_to_be_checked):
        """Check whether the index is valid or not as rules below

        |<---------cycle_length --------------------------->|<------offset----->|
        |<-----cycle_length - offset---->|<-----offset----->|<------offset----->|
        |<------------------------------>|<-invalid-->|<--valid--->|<-invalid-->|
                                         ^
                                       start
                                               -1           0            1

        :param start: Start index of current cycle.
        :param end_to_be_checked: End index to be checked.
        :return: If in valid, return 0, in left invalid, return -1, in right invalid return 1, in others, return False.
        """
        if end_to_be_checked in range(start - 1 + self.interval,
                                      start - 1 + 2 * self.offset - self.interval):

            return 0
        elif end_to_be_checked in range(start - 1,
                                        start - 1 + self.interval):
            return -1
        elif end_to_be_checked in range(start - 1 + 2 * self.interval,
                                        start - 1 + 2 * self.offset):
            return 1
        else:
            return False

    def is_end(self, end_to_be_checked, offset=0):
        """Check whether the index is end of the serial or nor.

        :param end_to_be_checked: End index to be checked of a cycle.
        :return: If end, return True, if not, return False.
        """
        if end_to_be_checked + offset > self.serial_length:
            return True
        else:
            return False

    def get_next_ending_index(self, start, search_length):
        """Get next ending index.

        :param start: Start index of search range.
        :param search_length: Length of search range.
        :return: Ending index or there is no ending: None.
        """
        # Find a ending index.
        if self.debug:
            print('>>> get next in [{0}, {1})'.format(start, start + search_length))
        if self.is_end(start + search_length / 2):
            if self.debug:
                print('>>> reaching end')
            return None
        end = self.get_local_minimum_indices(start, start + search_length)
        if self.debug:
            print('>>> get {0}'.format(','.join([str(e) for e in end])))

        end_map = [self.serial[e] for e in end]
        end = end[end_map.index(min(end_map))]
        if self.debug:
            print('>>> get minimum {0}'.format(end))

        # Check it.
        if self.is_end(end, offset=2 * self.interval):
            return end
        is_valid = self.is_valid_minimum_index(start, end - 1)

        if self.debug:
            print('>>> range score {0}'.format(is_valid))
        if is_valid is False:
            return None
        elif is_valid == 0:
            return end
        elif is_valid == -1:
            return self.get_next_ending_index(start - self.interval, 2 * self.offset)
        elif is_valid == 1:
            return self.get_next_ending_index(start + self.interval, 2 * self.offset)
        else:
            return None

    def get_cycle_boundary_indices(self):
        """Get cycle boundary indices from 1-D list.

        :return: A list contains (start, end)s of all cycles.
        """
        # Find a minimum point around the center of this serial.
        p_start = self.find_minimum_index_around_center()

        # Find the other minimum points we want can be starts of new walking cycles bidirectionally.
        cycle_boundary_indices = self.search(p_start)  # to right
        self.serial = list(reversed(self.serial))  # reverse
        cycle_boundary_indices += self.search(self.serial_length - 1 - p_start, reversed_=True)  # to left
        self.cycle_boundary_indices = cycle_boundary_indices  # only for test

        return cycle_boundary_indices

    def find_minimum_index_around_center(self):
        # Algorithm 1
        minimum_indices = np.array(
            self.get_local_minimum_indices(0, self.serial_length))  # not all minimums are what we want
        middle = minimum_indices[len(minimum_indices) / 2]  # index in the middle
        minimum_indices = minimum_indices[np.where(
            middle - self.cycle_length / 2 < minimum_indices
        )]
        p_start = minimum_indices[np.where(
            middle + self.cycle_length / 2 > minimum_indices
        )]
        p_start_map = [self.serial[e] for e in p_start]
        p_start1 = p_start[p_start_map.index(min(p_start_map))]  # start = start from a minimum point around the center

        # Algorithm 2
        middle_index = self.serial_length / 2
        left_index = int(middle_index - 1.5 * self.cycle_length)
        right_index = int(middle_index + 1.5 * self.cycle_length)
        minimum_indices = self.get_local_minimum_indices_new(self.serial, left_index, right_index)
        p_start_map = [self.serial[e] for e in minimum_indices]
        p_start = minimum_indices[
            p_start_map.index(min(p_start_map))]  # start = start from a minimum point around the center

        print('>>> search start from {0}(old), {1}(new)'.format(p_start1, p_start))
        return p_start

    def search(self, start, reversed_=False):
        """Do search.

        :param start: Start index of this search.
        :param reversed_: If true, reverse the ending index returned.
        :return: A list contains ending indices.
        """
        results = []
        while True:
            end = self.get_next_ending_index(
                start + self.cycle_length - self.offset, 2 * self.offset)

            # TODO how terrible
            if end == start:
                break

            if end is None:
                print('>>> search summary: done, last start from {0}'.format(start))
                break
            else:
                print('>>> search summary: start {0} end {1}'.format(
                    start if not reversed_ else self.serial_length - 1 - start,
                    end if not reversed_ else self.serial_length - 1 - end)
                )

            if reversed_:
                results.append([self.serial_length - 1 - end, self.serial_length - 1 - start])
            else:
                results.append([start, end])

            start = end
            self.count += 1

        return results
