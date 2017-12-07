from datetime import datetime, timedelta
import numpy


class TimeStatistic():
    def average(self):
        timedelta_list = self.timedeltas()
        time_list = self.filter_outliers([timedelta.seconds for timedelta in timedelta_list])

        if (len(time_list) > 0):
            return (len(time_list), sum(time_list) / len(time_list) / 60)
        else:
            return 'n/a'

    # Should be overwritten
    def timedeltas(self):
        return

    def filter_outliers(self, time_list):
        times = [time for time in time_list]

        sd = numpy.std(times)
        mean = numpy.mean(times)

        return [time for time in times if time >= mean - 3 * sd and time <= mean + 3 * sd]


class Route(TimeStatistic):
    valid_headsigns = [
        'Bl CMS',
        'Bl Hopkins Bayview',
        'Br White Marsh',
        'Br UM Medical',
        'Gd Canton Crossing',
        'Gd Walbrook Junction',
        'Gr Towson Town Center',
        'Gr W Baltimore MARC',
        'Lm Harbor East',
        'Lm Northwest Hospital',
        'Nv WaterSedge',
        'Nv Mondawmin',
        'Or Essex',
        'Or W Baltimore MARC',
        'Pk Cedonia',
        'Pk W Baltimore MARC',
        'Pr Catonsville',
        'Pr Johns Hopkins Hospital',
        'Rd Lutherville',
        'Rd UM Transit Center',
        'Sv Morgan State',
        'Sv Curtis Bay',
        'Yw Patapsco',
        'Yw UMBC',
        'Yw Mondawmin'
        ]

    def __init__(self, num_id):
        self.num_id = num_id
        self.headsigns = {}

    def timedeltas(self):
        return [time for headsign in self.headsigns.items() for time in headsign[1].timedeltas()]

    # hand a row from the csv
    def insert_trip(self, stop_list):
        if (stop_list[0]['headsign'] not in self.headsigns):
            self.headsigns[stop_list[0]['headsign']] = Headsign(stop_list[0]['headsign'])
        self.headsigns[stop_list[0]['headsign']].insert_trip(stop_list)


class Headsign(TimeStatistic):
    valid_start = [
        13783,
        6995,
        11123,
        14101,
        14144,
        12613,
        14108,
        14136,
        14147,
        9486,
        13528,
        1992,
        14109,
        4541,
        14110,
        919,
        14143,
        180,
        14086,
        14083,
        6859,
        14149,
        13529,
        13529,
        2737,
        10964
        ]

    def __init__(self, name):
        self.name = name
        self.start_stops = {}

    def timedeltas(self):
        return [time for start_stops in self.start_stops.items() for time in start_stops[1].timedeltas()]

    def insert_trip(self, stop_list):
        # sort by actual time
        # first is earliest
        stop_list = sorted(stop_list, key=lambda stop: datetime.strptime(stop['actual_time'], '%H:%M:%S'))

        # validate start and stop ids
        if (int(stop_list[0]['stop_id']) not in self.valid_start):
            # print('Invalid start id:')
            # print(stop_list[0]['stop_id'])
            return

        if (stop_list[0]['stop_id'] not in self.start_stops):
            self.start_stops[stop_list[0]['stop_id']] = HeadsignStart(stop_list[0]['stop_id'])
        self.start_stops[stop_list[0]['stop_id']].insert_trip(stop_list)


class HeadsignStart(TimeStatistic):
    def __init__(self, stop_id):
        self.stop_id = stop_id
        self.trips = {}

    def timedeltas(self):
        return [time for trip in self.trips.items() for time in trip[1].timedeltas()]

    def insert_trip(self, stop_list):
        if (stop_list[0]['trip_id'] not in self.trips):
            self.trips[stop_list[0]['trip_id']] = Trip(stop_list[0]['trip_id'], stop_list[0]['vehicle_id'])
        self.trips[stop_list[0]['trip_id']].insert_stops(stop_list)


# may be worth adding in all the fields later so you can just put everything into this
# and then insert all of these into the structure
class Trip(TimeStatistic):
    def __init__(self, num_id, bus_id):
        self.num_id = num_id
        self.bus_id = bus_id
        self.stops = []

    # returns only the difference between the first and last stops
    def timedeltas(self):
        time_list = [stop.time for stop in self.stops]
        time_list.sort()
#         return [time_list[i - 1] - time_list[i] for i in range(1, len(time_list))]
        return [time_list[-1] - time_list[0]]

    def insert_stops(self, stop_list):
        for stop in stop_list:
            self.stops.append(Stop(stop['stop_id'], datetime.strptime(stop['actual_time'], '%H:%M:%S')))


class Stop():
    def __init__(self, stop_id, time):
        self.stop_id = stop_id
        self.time = time
