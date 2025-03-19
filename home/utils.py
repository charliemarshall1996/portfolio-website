def generate_time_choices():
    start_time = 9 * 60  # 09:00 in minutes
    end_time = 17 * 60  # 17:00 in minutes
    increment = 15  # 15-minute increments
    time_choices = []

    current_time = start_time
    while current_time <= end_time:
        hours = current_time // 60
        minutes = current_time % 60
        time_str = f"{hours:02d}:{minutes:02d}"  # Format as HH:MM
        time_choices.append((time_str, time_str))
        current_time += increment

    return time_choices
