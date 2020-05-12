import os
import glob
from MesaHandler import MesaAccess


def get_latest_log():
    """ Gets the most recent profile filename from the
    LOGS directory.

        Returns:
            latest_log (str): filename of most recent profile
    """
    ma = MesaAccess()
    try:
        log_prefix = ma["profile_data_prefix"]
    except KeyError:
        log_prefix = "profile"
    try:
        log_dir = ma["log_directory"]
    except KeyError:
        log_dir = "LOGS"

    log_fnames = log_prefix + "*.data"
    src = os.path.join(log_dir, log_fnames)
    list_of_logs = glob.glob(src)
    
    if list_of_logs:
        latest_log = max(list_of_logs, key=os.path.getctime)
    else:
        print("failed in get_latest_log")
        latest_log = ""

    return latest_log
