# python version 3.8.0
# Author: Lane Birmingham

import pytz
from datetime import datetime as dt
from datetime import timedelta


def main():
    print('Shouldnt print this statement. File for import only')


class TimeClass():
    def __init__(self):
        super().__init__()
        self.fmt = '%d-%m-%Y %H:%M:%S %Z%z'
        self.tz = pytz.timezone('Australia/Brisbane')
        self.local_time = ""
        self.local_time_string = ""
        self.time_until = ""
        #print('Timezone init to ', self.tz)
    
    def __repr__(self) -> str:
        # what is printed when class is printed
        return self.local_time_string

    def gen_AEST(self, time_age = 0.0):
        """ Generate Aus eastern standard time to a time of time_age ago """

        self.local_time = dt.now(self.tz) 
        self.local_time = self.local_time - timedelta(minutes = time_age)
        self.local_time_string = self.local_time.strftime(self.fmt)
        time_now = dt.now(self.tz)
        self.time_until = self.local_time - time_now
        # print('test')


if __name__ == '__main__':
    main()
