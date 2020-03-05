import datetime
import random

class BuildIdGenerator:
    """Build Id generator based on time stamps. The time stamps are simulated:
    For every new build id, the time is "virtually and randomly" advanced into
    the future
    """
    
    def __init__(self):
        # Set an arbitrary start time
        self._datetime = datetime.datetime(2020, 2, 5, 21, 10)

    def generate_id(self):
        """Increases time 'randomly' and returns a new (unique) build id derived from that time stamp"""
        self._datetime += datetime.timedelta(minutes = random.randint(12, 60*24*7))
        return self._datetime.strftime("%y%m%d%H%M%S")
