import unittest
from unittest_data_provider import data_provider
from .amy import Amy


class AmyTest(unittest.TestCase):
    """
    # Task 2
    """
    def setUp(self):
        self.amy = Amy()

    @staticmethod
    def test_calculate_subject_priority_score_dp():
        return (
            ('prefix priority:low suffix', 1 / 3),  # priority low should return score of 1/3
            ('prefix priority:medium suffix', 2 / 3),  # priority medium should return score of 2/3
            ('prefix priority:high suffix', 1),  # priority high should return score of 1
            ('priority:high suffix', 1),  # subject can be without prefix
            ('prefix priority:high', 1),  # subject can be without suffix
            ('some subject', 1/3),  # if the priority:X not found -> should return score of 1/3 (same as low)
            ('prefix priority:extra_high suffix', 1 / 3),  # not supported priority level - priority low should return score of 1/3
        )

    @data_provider(test_calculate_subject_priority_score_dp)
    def test_calculate_subject_priority_score(self, subject, expected_priority):
        self.assertEqual(self.amy.calculate_subject_priority_score(subject), expected_priority)

    @staticmethod
    def test_calculate_attached_files_priority_score_dp():
        return (
            ((0, 5), 1/3),  # priority low should return score of 1/3
            ((5, 11), 2 / 3),  # priority medium should return score of 2/3
            ((11, 100, 10), 1),  # priority high should return score of 1
        )

    @data_provider(test_calculate_attached_files_priority_score_dp)
    def test_calculate_attached_files_priority_score(self, num_of_files_range, expected_priority):
        for num_of_files in range(*num_of_files_range):
            self.assertEqual(self.amy.calculate_attached_files_priority_score(num_of_files), expected_priority)

    @staticmethod
    def test_calculate_sender_priority_score_dp():
        return (
            ('somename@company.com', 1),  # priority high should return score of 1
            ('somename@vendor1.com', 2/3),  # priority medium should return score of 2/3
            ('somename@vendor2.org', 2/3),  # priority medium should return score of 2/3
            ('somename@vendor2.com', 1 / 3),  # priority low should return score of 1/3
            ('somename@somedomain.com', 1/3),  # priority low should return score of 1/3
            ('somedomain.com', 1 / 3),  # not a valid email - priority low should return score of 1/3
        )

    @data_provider(test_calculate_sender_priority_score_dp)
    def test_calculate_sender_priority_score(self, sender, expected_priority):
        self.assertEqual(self.amy.calculate_sender_priority_score(sender), expected_priority)

    @staticmethod
    def test_calculate_priority_score_dp():
        return (
            (dict(subject='prefix priority:high suffix', num_of_files=15, sender='somename@company.com'), 1),  # every property is high
            (dict(subject='prefix priority:medium suffix', num_of_files=6, sender='somename@vendor1.com'), 0.67), # every property is medium
            (dict(subject='prefix priority:low suffix', num_of_files=0, sender='somename@somedomain.com'), 0.33), # every property is low
            (dict(subject='prefix priority:high suffix', num_of_files=0, sender='somename@vendor1.com'), 0.77), # according to the formula
            (dict(subject='prefix priority:medium suffix', num_of_files=15, sender='somename@vendor1.com'), 0.73), # according to the formula
            (dict(subject='prefix priority:medium suffix', num_of_files=3, sender='somename@company.com'), 0.7), # according to the formula
        )

    @data_provider(test_calculate_priority_score_dp)
    def test_calculate_priority_score(self, email_properties, expected_priority):
        self.assertEqual(self.amy.calculate_priority_score(email_properties), expected_priority)
