import unittest
from unittest.mock import patch
from io import StringIO
import os
from collections import defaultdict
# Import the functions from the program
from Fair_Billing import get_user_start_end, get_users_sessions, parse_log_file, calculate_session_duration


class TestFairBilling(unittest.TestCase):

    # Test get_user_start_end function
    def test_get_user_start_end(self):
        data = defaultdict(list, {'ALICE99': [{'Start': '14:02:03'}, {'End': '14:02:34'}, {'Start': '14:02:58'}, {'Start': '14:03:33'}, {'End': '14:03:35'}, {'End': '14:04:05'}, {'End': '14:04:23'}], 'CHARLIE': [{'Start': '14:02:03'}, {'End': '14:02:05'}, {'Start': '14:03:02'}, {'End': '14:03:37'}, {'Start': '14:04:41'}]})
        expected_result = {'ALICE99': {'start_times': ['14:02:03', '14:02:58', '14:03:33'], 'end_times': ['14:02:34', '14:03:35', '14:04:05', '14:04:23']}, 'CHARLIE': {'start_times': ['14:02:03', '14:03:02', '14:04:41'], 'end_times': ['14:02:05', '14:03:37']}}
        self.assertEqual(get_user_start_end(data), expected_result)

    # Test get_users_sessions function
    def test_get_users_sessions(self):
        user_dict = {'ALICE99': {'start_times': ['14:02:03', '14:02:58', '14:03:33'], 'end_times': ['14:02:34', '14:03:35', '14:04:05', '14:04:23']}, 'CHARLIE': {'start_times': ['14:02:03', '14:03:02', '14:04:41'], 'end_times': ['14:02:05', '14:03:37']}}      
        start_timestamp = '14:02:03'
        end_time_stamp = '14:04:41'
        expected_result = {'ALICE99': [{'start': '14:02:03', 'end': '14:02:34'}, {'start': '14:02:58', 'end': '14:03:35'}, {'start': '14:03:33', 'end': '14:04:05'}, {'start': '14:02:03', 'end': '14:04:23'}], 'CHARLIE': [{'start': '14:02:03', 'end': '14:02:05'}, {'start': '14:03:02', 'end': '14:03:37'}, {'start': '14:04:41', 'end': '14:04:41'}]}
        self.assertEqual(get_users_sessions(user_dict, start_timestamp, end_time_stamp), expected_result)

    # Test parse_log_file function
    @patch('sys.stdout', new_callable=StringIO)
    def test_parse_log_file(self, mock_stdout):
        file_path = 'test_log.txt'
        with open(file_path, 'w') as file:
            file.write("14:02:03 ALICE99 Start\n"
                       "14:02:05 CHARLIE End\n"
                       "14:02:34 ALICE99 End\n"
                       "14:02:58 ALICE99 Start\n"
                       "14:03:02 CHARLIE Start\n"
                       "14:03:33 ALICE99 Start\n"
                       "14:03:35 ALICE99 End\n"
                       "14:03:37 CHARLIE End\n"
                       "14:04:05 ALICE99 End\n"
                       "14:04:23 ALICE99 End\n"
                       "14:04:41 CHARLIE Start\n")
        expected_result =  {'ALICE99': [{'start': '14:02:03', 'end': '14:02:34'}, {'start': '14:02:58', 'end': '14:03:35'}, {'start': '14:03:33', 'end': '14:04:05'}, {'start': '14:02:03', 'end': '14:04:23'}], 'CHARLIE': [{'start': '14:02:03', 'end': '14:02:05'}, {'start': '14:03:02', 'end': '14:03:37'}, {'start': '14:04:41', 'end': '14:04:41'}]}
        self.assertEqual(parse_log_file(file_path), expected_result)

    # Test calculate_session_duration function
    def test_calculate_session_duration(self):
        sessions = {'ALICE99': [{'start': '14:02:03', 'end': '14:02:34'}, {'start': '14:02:58', 'end': '14:03:35'}, {'start': '14:03:33', 'end': '14:04:05'}, {'start': '14:02:03', 'end': '14:04:23'}], 'CHARLIE': [{'start': '14:02:03', 'end': '14:02:05'}, {'start': '14:03:02', 'end': '14:03:37'}, {'start': '14:04:41', 'end': '14:04:41'}]}
        expected_result = {
            'ALICE99': (4, 240),
            'CHARLIE': (3, 37)
        }
        self.assertEqual(calculate_session_duration(sessions), expected_result)


if __name__ == "__main__":
    unittest.main()
