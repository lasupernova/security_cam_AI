import datetime

def pretty_print_timedelta(delta):
    """
    Converts datetime.timedelta - object to string and returns a pretty printed version in the following format:
    "hh:mm:ss" or "more than 24 hours" in case the tiemdelta is over 24 hours.

    Parameters:
        delta (datetime.timedelta) - timedelta to be converted

    Returns:
        duration (str)
    """
    days = delta.days
    hh, remainder = divmod(td.seconds, 3600)
    mm, ss = divmod(remainder, 60)

    if days == 0:
        return f"{hh}h:{mm}m:{ss}s"
    else:
        return "More than 24 hours!"