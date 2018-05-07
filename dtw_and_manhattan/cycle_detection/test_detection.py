"""
Unittest to class CycleDetection.

author: cyrus
date: 2018-4-19
"""
from detection import CycleDetection
from unittest import TestCase


class TestCycleDetection(TestCase):
    def test_get_cycle_length_estimation(self):
        # Arrange.
        data = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0,
        ]
        # Act.
        cycle_detection = CycleDetection(data, subset_size=6)
        cycle_length = cycle_detection.get_cycle_length_estimation()

        # Assert.
        self.assertEqual(21.0, cycle_length)

    def test_get_cycle_boundary_indices(self):
        # Arrange.
        data = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0,
        ]
        # Act.
        cycle_detection = CycleDetection(data, subset_size=3)
        cycle_length = cycle_detection.get_cycle_length_estimation()
        cycles = cycle_detection.get_cycle_boundary_indices()
        print cycles

        # Assert.
        self.assertEqual(21.0, cycle_length)
        self.assertItemsEqual([
            [83, 104], [104, 125], [125, 146], [146, 167],
            [62, 83], [41, 62], [20, 41], [0, 20]
        ], cycles)

    def test_get_local_minimum_indices_new(self):
        # Arrange.
        serial = [
            5, 3, 1, 3, 4,
            5, 3, 1, 3, 4,
            5, 3, 1, 3, 4,
            5, 3, 1, 3, 4,
        ]

        # Action.
        minimums = CycleDetection.get_local_minimum_indices_new(serial, 0, len(serial))

        # Assert.
        print minimums

