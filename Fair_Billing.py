from collections import defaultdict
import sys


def get_user_start_end(data):
    """
    Extracts start and end times for each user from the given data.

    Args:
        data (dict): A dictionary containing user data.

    Returns:
        dict: A dictionary containing user start and end times.
    """
    matched_data = {}
    for user, timings in data.items():
        start_time = []
        end_time = []
        for timing in timings:
            if 'Start' in timing:
                start_time.append(timing['Start'])
            elif 'End' in timing:
                end_time.append(timing['End'])
        matched_data[user] = {'start_times': start_time, 'end_times': end_time}
    return matched_data


def get_users_sessions(user_dict, start_timestamp, end_time_stamp):
    """
    Generates session data for each user based on start and end times.

    Args:
        user_dict (dict): A dictionary containing user start and end times.
        start_timestamp (str): The earliest timestamp in the log file.
        end_time_stamp (str): The latest timestamp in the log file.

    Returns:
        dict: A dictionary containing session data for each user.
    """
    sessions_data = {}
    for user, timings in user_dict.items():
        start_list = timings['start_times']
        end_list = timings['end_times']
        session = []
        max_length = max(len(start_list), len(end_list))
        for i in range(max_length):
            start_time = start_list[i] if i < len(start_list) else start_timestamp
            end_time = end_list[i] if i < len(end_list) else end_time_stamp
            session.append({'start': start_time, 'end': end_time})
        sessions_data[user] = session
    return sessions_data


def parse_log_file(file_path):
    """
    Parses the log file and extracts user session data.

    Args:
        file_path (str): The path to the log file.

    Returns:
        dict: A dictionary containing session data for each user.
    """
    try:
        data = defaultdict(list)
        start_times = {}
        first_timestamp = None
        last_timestamp = None

        with open(file_path, 'r') as file:
            for line in file:
                parts = line.split()
                timestamp = parts[0]
                if first_timestamp is None:
                    first_timestamp = timestamp
                last_timestamp = timestamp
                first_time = first_timestamp.split()[0]
                last_time = last_timestamp.split()[0]
                if len(parts) >= 3:
                    time_str = parts[0]
                    user = parts[1]
                    action = parts[2]

                    if action == 'Start':
                        start_times[user] = time_str
                    elif action == 'End':
                        if user not in start_times:
                            start_times[user] = time_str
                            data[user].append({"Start": first_timestamp})
                    if user in start_times:
                        data[user].append({action: time_str})
        user_dict = get_user_start_end(data)
        session_data = get_users_sessions(user_dict, first_time, last_time)
        return session_data
    except FileNotFoundError:
        print("Error: File not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def calculate_session_duration(sessions):
    """
    Calculates session duration for each user.

    Args:
        sessions (dict): A dictionary containing session data for each user.

    Returns:
        dict: A dictionary containing session count and total duration for each user.
    """
    user_sessions = {}
    for username, logs in sessions.items():
        session_count = 0
        total_duration = 0
        for log in logs:
            if log['start'] is not None and log['end'] is not None:
                start_time = log['start']
                end_time = log['end']
                start_hour, start_minute, start_second = map(int, start_time.split(':'))
                end_hour, end_minute, end_second = map(int, end_time.split(':'))
                duration = (end_hour - start_hour) * 3600 + (end_minute - start_minute) * 60 + (
                        end_second - start_second)
                total_duration += max(0, duration)
                session_count += 1
        user_sessions[username] = (session_count, total_duration)
    return user_sessions


def main():
    """
    Main function to run the program.
    """
    if len(sys.argv) < 3:
        print("Usage: python program_name.py input_file.txt argument1 argument2")
        return

    input_file = sys.argv[1]
    additional_args = sys.argv[2:]  # Collect additional arguments

    sessions = parse_log_file(input_file)
    if not sessions:
        print("No valid session data found.")
        return

    user_sessions = calculate_session_duration(sessions)
    for username, (session_count, total_duration) in user_sessions.items():
        print(f"{username} {session_count} {total_duration}")

    # Use additional arguments here
    print("Additional arguments:", additional_args)


if __name__ == "__main__":
    main()
