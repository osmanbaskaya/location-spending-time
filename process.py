import json
import sys
import datetime
from bs4 import BeautifulSoup
import json
from geopy import distance
from itertools import cycle
import pandas as pd
import seaborn as sns
import os


def get_coord(location):
    longitude = str(location['longitudeE7'])
    latitude = str(location['latitudeE7'])
    longitude = "{}.{}".format(longitude[:-7], longitude[-7:])
    latitude = "{}.{}".format(latitude[:-7], latitude[-7:])
    try:
        latitute = float(latitude)
        longitude = float(longitude)
        return latitude, longitude
    except ValueError as e:
        print("ValueError:\n{}".format(location), file=sys.stderr, flush=True)
        return None


def get_date(location):
    return datetime.datetime.fromtimestamp(int(location['timestampMs']) / 1000)


class Locator:
    def __init__(self, places, threshold=0.05):
        self.places = places
        self.threshold = threshold
        self.been_there = {}
        self.start_time = {}
        self.initiate()

    def initiate(self):
        self.been_there = dict(zip(self.places.keys(), cycle([False])))
        self.start_time = dict(zip(self.places.keys(), cycle([None])))

    def exit_from_place(self, place, t, d):
        if self.been_there[place]:
            self.been_there[place] = False
            hour_diff = (self.start_time[place] - t).seconds / 3600
            d[place][-1] += hour_diff
            self.start_time[place] = None
        else:
            d[place][-1] += 0

    def enter_to_place(self, place, t):
        self.been_there[place] = True
        self.start_time[place] = t


    @staticmethod
    def read_location_data_file(data_fn):
        print("Reading the input: {}".format(data_fn))
        return json.load(open(data_fn))['locations']


    def process_data(self, data_fn, stop_after_num_day=None):

        locations = Locator.read_location_data_file(data_fn)

        d = {"date": [], 'weekday': [], 'month': []}
        d.update(dict([(place, []) for place in self.places]))

        date_to_process = None
        num_of_day_processed = -1

        for i, location in enumerate(locations, 0):
            t = get_date(location)
            curr_date = t.strftime('%Y-%m-%d')

            # new day
            if curr_date != date_to_process:
                num_of_day_processed += 1
                if num_of_day_processed % 30 == 0:
                    print("{} of day processed. {} location has been read.".format(num_of_day_processed, i), flush=True)

                if date_to_process is not None:
                    for place in self.places.keys():
                        self.exit_from_place(place, t, d)  # day.

                date_to_process = curr_date
                d['date'].append(date_to_process)
                d['month'].append("{}-{}".format(*date_to_process.split('-')[:2]))

                d['weekday'].append(t.weekday() + 1)
                for place in self.places:
                    d[place].append(0)

                if stop_after_num_day is not None:
                    if num_of_day_processed > stop_after_num_day:
                        break

            curr_loc = get_coord(location)
            if curr_loc is not None:
                for place, loc in self.places.items():
                    dist = distance.distance(loc, curr_loc).miles

                    # Entering
                    if dist < self.threshold and not self.been_there[place]:
                        self.enter_to_place(place, t)

                    # Exiting
                    if dist > self.threshold and self.been_there[place]:
                        self.exit_from_place(place, t, d)

        print("Done. Total {} of day processed. {} location has been read.".format(num_of_day_processed, i), flush=True)
        df = pd.DataFrame(d)
        Locator.write_processed_data(df, data_fn)
        return df

    @staticmethod
    def write_processed_data(df, input_filename):
        output_fn = "processed-{}.tsv".format(os.path.splitext(input_filename)[0])
        print("Writing the output file: {}".format(output_fn))
        df.to_csv(output_fn, sep='\t', index=False)  # save

