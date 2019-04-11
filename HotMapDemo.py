import csv
import os
# to install fitparse, run
# sudo pip3 install -e git+https://github.com/dtcooper/python-fitparse#egg=python-fitparse
import fitparse
import pytz

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

# allowed_fields = ['timestamp', 'position_lat', 'position_long', 'distance',
#                   'enhanced_altitude', 'altitude', 'enhanced_speed',
#                   'speed', 'heart_rate', 'cadence', 'fractional_cadence']


# For fast Speed
allowed_fields = ['timestamp', 'position_lat', 'position_long', 'altitude']
required_fields = ['timestamp', 'position_lat', 'position_long', 'altitude']

UTC = pytz.UTC
CST = pytz.timezone('US/Central')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 100)


def main():
    files = os.listdir("./")
    fit_files = [file for file in files if file[-4:].lower() == '.fit']
    for file in fit_files:
        fitfile = fitparse.FitFile(file, data_processor=fitparse.StandardUnitsDataProcessor())

        print('converting %s' % file)

        messages = fitfile.messages
        data = []
        for m in messages:
            skip = False
            if not hasattr(m, 'fields'):
                continue
            fields = m.fields
            # check for important data types
            mdata = {}
            for field in fields:
                if field.name in allowed_fields:
                    if field.name == 'timestamp':
                        mdata[field.name] = UTC.localize(field.value).astimezone(CST)
                    else:
                        mdata[field.name] = field.value
            for rf in required_fields:
                if rf not in mdata:
                    skip = True
            if not skip:
                data.append(mdata)

        try:
            lat_data = pd.DataFrame(data)["position_lat"].astype(str).replace("None", np.nan).astype(float)
            long_data = pd.DataFrame(data)["position_long"].astype(str).replace("None", np.nan).astype(float)
            plt.plot(long_data, lat_data, 'b', alpha=0.2)
        except KeyError:
            print "error"

    plt.show()
    print('finished conversions')


def write_fitfile_to_csv(fitfile, output_file='test_output.csv'):
    messages = fitfile.messages
    data = []
    for m in messages:
        skip = False
        if not hasattr(m, 'fields'):
            continue
        fields = m.fields
        # check for important data types
        mdata = {}
        for field in fields:
            if field.name in allowed_fields:
                if field.name == 'timestamp':
                    mdata[field.name] = UTC.localize(field.value).astimezone(CST)
                else:
                    mdata[field.name] = field.value
        for rf in required_fields:
            if rf not in mdata:
                skip = True
        if not skip:
            data.append(mdata)

    try:
        lat_data = pd.DataFrame(data)["position_lat"].astype(str).replace("None", np.nan).astype(float)
        long_data = pd.DataFrame(data)["position_long"].astype(str).replace("None", np.nan).astype(float)
        plt.plot(long_data, lat_data, 'b', alpha=0.2)
    except KeyError:
        print "error"

    # print pd.DataFrame(data).head()
    # write to csv
    # with open(output_file, 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(allowed_fields)
    #     for entry in data:
    #         writer.writerow([str(entry.get(k, '')) for k in allowed_fields])
    # print('wrote %s' % output_file)


def plot_gps():
    data = pd.read_csv("./36766433.csv")
    lat_data = data["position_lat"].astype(str).replace("None", np.nan).astype(float)
    long_data = data["position_long"].astype(str).replace("None", np.nan).astype(float)
    plt.plot(lat_data, long_data)
    plt.show()


if __name__ == '__main__':
    main()
