# Fair Billing Program
# Introduction

This program is designed to analyze log files from a hosted application provider that charges users based on the duration of their sessions. It calculates the total duration of sessions for each user, accounting for any missing start or end markers in the log file.
# Requirements

    Python 3.x
    Required libraries: collections

# Usage

To use this program, follow these steps:

    1. Ensure you have Python installed on your system.

    2. Open a terminal or command prompt.

    3. Navigate to the directory containing the program files.

    4. Run the program with the following command:
            python fair_billing.py <input_file.txt> foo bar
      Replace <input_file.txt> with the path to your input log file and along with dditional arguments
    5. The program will then process the log file and output the results, showing each user's name, number of sessions, and total duration in seconds.
# Input File Format
    The input file should contain log data in the following format:
            <timestamp> <username> <action>
      * <timestamp>: The time at which the session starts or ends, in the format HH:MM:SS.
      * <username>: A single alphanumeric string representing the user's name.
      * <action>: Either "Start" or "End" indicating the start or end of a session.
Example :

    14:02:03 ALICE99 Start
    14:02:05 CHARLIE End
    14:02:34 ALICE99 End
    14:02:58 ALICE99 Start
    14:03:02 CHARLIE Start
    14:03:33 ALICE99 Start
    14:03:35 ALICE99 End
    14:03:37 CHARLIE End
    14:04:05 ALICE99 End
    14:04:23 ALICE99 End
    14:04:41 CHARLIE Start


# Output
    The program will output the results in the following format:
    <username> <session_count> <total_duration>
    * <username>: The user's name.
    * <session_count>: The number of sessions for the user.
    * <total_duration>: The total duration of sessions for the user in seconds.
Example:

      ALICE99 4 240
      CHARLIE 3 37
# Assumptions

    The log file contains valid timestamps, usernames, and action markers.
    Missing start or end markers are handled as described in the program description.

# Error Handling

    If the input file is not found, the program will display an error message and exit.
    Other exceptions will also be caught and reported with appropriate error messages.
# Testing
    The program includes unit tests to ensure its correctness. These tests can be run using the following command:
        python test_fail_billing.py
    The tests cover various aspects of the program, including:
            * Extracting start and end times for each user.
            * Generating session data for each user.
            * Parsing the log file.
            * Calculating session duration for each user.

You can replace `test_fail_billing.py` with the actual name of your test file. This updated README file provides comprehensive information about the program, its usage, input/output formats, assumptions, error handling, and testing procedures.
