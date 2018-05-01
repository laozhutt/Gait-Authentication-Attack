"""
Unittest to tools.

author: cyrus
date: 2018-4-19
"""
from unittest import TestCase
import tools


class TestTools(TestCase):
    def test_get_interpolation(self):
        # Arrange.
        timestamps = [-1, 0, 1, 2]  # 1HZ
        data = [
            [1, 2, 3, 4],
            [1, 2, 3, 4],
            [1, 2, 3, 4],
        ]
        target_sample_rates = [0.5, 1, 2]  # <1HZ, =1HZ, >1HZ

        # Action.
        result = []  # target_timestamps=t_t, target_data=t_d
        for target_sample_rate in target_sample_rates:
            t_t, t_d = tools.get_interpolation(
                timestamps, data, target_sample_rate=target_sample_rate)
            result.append([t_t, t_d])

        # Assert.
        self.assertEqual(result[0][0], [.0, 2.0])  # expected, actual, reversed
        self.assertEqual(result[1][0], [.0, 1.0, 2.0, 3.0])
        self.assertEqual(result[2][0], [.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
        self.assertEqual(result[0][1][0], [1.0, 3.0])
        self.assertEqual(result[1][1][0], [1.0, 2.0, 3.0, 4.0])
        self.assertEqual(result[2][1][0], [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])

    def test_get_magnitude(self):
        # Arrange.
        data = [
            [3, 6, 5],
            [4, 8, 12],
        ]

        # Action.
        result = tools.get_magnitude(data)

        # Assert.
        self.assertEqual(result, [5.0, 10.0, 13.0])

    def test_remove_odd_cycles(self):
        # Arrange.
        data = [
            1, 2, 3, 5, 4, 3, 2,
            1, 2, 2, 5, 4, 3, 2,
            1, 2, 3, 5, 4, 3, 2,
        ]
        indices = [
            [2, 8],
            [9, 15],
            [16, 20],
        ]
        # Action.
        results = tools.remove_odd_cycles(data, indices)

        # Assert.
        self.assertItemsEqual([[2, 8], [9, 15], [16, 20]], results)

    def test_get_splitted_data(self):
        # Arrange.
        data = [
            1, 2, 3, 5, 4, 3, 2,
            1, 2, 2, 5, 4, 3, 2,
            1, 2, 3, 5, 4, 3, 2,
        ]
        indices = [
            [2, 8],
            [9, 15],
            [16, 20],
        ]
        # Action.
        results = tools.get_splitted_data(data, indices)

        # Assert.
        self.assertItemsEqual([[3, 5, 4, 3, 2, 1], [2, 5, 4, 3, 2, 1], [3, 5, 4, 3]], results)
