import csv
import os
import sys
from classes import Headsign, Trip, Route, Stop


def main():
    process_file(sys.argv[1])


def process_file(file_name):
    route_dict = {}
    trip_bins = {}
    average_str_read = '{} {:30} {} {} {}\n'.format(
        'route_info', 'headsign_info', 'headsign_start', 'count', 'average time')
    average_str_csv = '{},{},{},{},{}\n'.format(
        'route_info', 'headsign_info', 'headsign_start', 'count', 'average time')

    # read in the csv
    with open(file_name, 'r') as csvfile:
        read_values = csv.DictReader(csvfile)

        # put into objects
        # probably want to use a dict object to sort
        # block_id, trip_id, route_id, route_short_name, direction_id, stop_id, headsign, vehicle_id, driver_id, sched_adherence_secs, scheduled_date, scheduled_time, actual_date, actual_time, is_arrival
        # build empty things?
        for row in read_values:
            if row['trip_id'] not in trip_bins:
                trip_bins[row['trip_id']] = []
            trip_bins[row['trip_id']].append(row)

        for stop_list in trip_bins.items():
            if(stop_list[1][0]['route_id'] not in route_dict):
                route_dict[stop_list[1][0]['route_id']] = Route(int(stop_list[1][0]['route_id']))
            route_dict[stop_list[1][0]['route_id']].insert_trip(stop_list[1])

    # get the averages
    for route in route_dict.items():
        route_info = '{}'.format(route[1].num_id)

        for headsign in route[1].headsigns.items():
            headsign_info = '{}'.format(headsign[1].name)

            for headsign_start in headsign[1].start_stops.items():
                avg_time = headsign_start[1].average()

                if avg_time[1] is not 'n/a':
                    average_str_read += '{:7}:{:35}:{:7}: trip count:{:3}: {}'.format(
                        route_info, headsign_info, headsign_start[1].stop_id, avg_time[0], avg_time[1])

                    average_str_csv += '{},{},{},{},{}'.format(
                        route_info, headsign_info, headsign_start[1].stop_id, avg_time[0], avg_time[1])

                    average_str_read += '\n'
                    average_str_csv += '\n'

    print(average_str_read)

    # output to file
    path_info = os.path.split(os.path.abspath(sys.argv[1]))
    with open(os.path.join(path_info[0], "average_trip_times_" + path_info[1]), 'w') as csvfile:
        csvfile.write(average_str_csv)

def main2():
    average_str_read = '{} {:30} {} {} {}\n'.format(
        'route_info', 'headsign_info', 'headsign_start', 'count', 'average time')
    average_str_csv = '{},{},{},{},{}\n'.format(
        'route_info', 'headsign_info', 'headsign_start', 'count', 'average time')

    # loop through files
    directory = sys.argv[1]
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            route_dict = {}
            trip_bins = {}
            print(filename)

            # read in the csv
            with open(os.path.join(directory, filename), 'r') as csvfile:
                read_values = csv.DictReader(csvfile)

                # put into objects
                # probably want to use a dict object to sort
                # block_id, trip_id, route_id, route_short_name, direction_id, stop_id, headsign, vehicle_id, driver_id, sched_adherence_secs, scheduled_date, scheduled_time, actual_date, actual_time, is_arrival
                # build empty things?
                for row in read_values:
                    if row['trip_id'] not in trip_bins:
                        trip_bins[row['trip_id']] = []
                    trip_bins[row['trip_id']].append(row)

                for stop_list in trip_bins.items():
                    if(stop_list[1][0]['route_id'] not in route_dict):
                        route_dict[stop_list[1][0]['route_id']] = Route(int(stop_list[1][0]['route_id']))
                    route_dict[stop_list[1][0]['route_id']].insert_trip(stop_list[1])

            # get the averages
            for route in route_dict.items():
                route_info = '{}'.format(route[1].num_id)

                for headsign in route[1].headsigns.items():
                    headsign_info = '{}'.format(headsign[1].name)

                    for headsign_start in headsign[1].start_stops.items():
                        avg_time = headsign_start[1].average()

                        if avg_time[1] is not 'n/a':
                            average_str_read += '{:7}:{:35}:{:7}: trip count:{:3}: {}'.format(
                                route_info, headsign_info, headsign_start[1].stop_id, avg_time[0], avg_time[1])

                            average_str_csv += '{},{},{},{},{}'.format(
                                route_info, headsign_info, headsign_start[1].stop_id, avg_time[0], avg_time[1])

                            average_str_read += '\n'
                            average_str_csv += '\n'

            print(average_str_read)

            # output to file
            with open(os.path.join(directory, "average_trip_times_" + filename), 'w') as csv_outfile:
                csv_outfile.write(average_str_csv)

if __name__ == '__main__':
    main()
