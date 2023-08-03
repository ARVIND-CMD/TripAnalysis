from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
import datetime


def haversine(lon1, lat1, lon2, lat2):
    try:
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 
        return c * r
    except Exception as e:
        print(f"Exeption in haversine : {e}")
        return -1
    

# Vehicle Trails Helper Functions
def data_cleaning_vehicle_trails(df):
    try:
        # Deleting duplicate rows
        df.drop_duplicates(subset=["lat","lon"], keep='last', inplace=True)
        df.sort_values(by=['tis'], inplace=True)
        # Removing empty values to NaN and deleting them from the table
        df.replace(r'^\s*$', np.nan, regex=True, inplace = True)
        new_df = df.dropna(subset=['lon','lat','osf','spd','tis'], inplace=False)
        return new_df
    except Exception as e:
        print(f"Exeption in data_cleaning_vehicle_trails : {e}")
        return pd.DataFrame() #check for empty dataframe

def filter_data_on_epoch_time(start_time,end_time,df):
    try:
        return df.loc[(df['tis'] >= start_time) & (df['tis'] < end_time)]
    except Exception as e:
        print(f"Exeption in filter_data_on_epoch_time : {e}")
        return -1

def calculate_distance(df):
    try:
        st_long = df['lon'].iloc[0]
        st_lat = df['lat'].iloc[0]
        end_long = df['lon'].iloc[-1]
        end_lat = df['lat'].iloc[-1]
        distance_travelled = haversine(st_long,st_lat,end_long,end_lat)
        return distance_travelled
    except Exception as e:
        print(f"Exeption fetching calculate_distance : {e}")
        return -1

def no_of_speed_violations(df):
    try:
        return len(df[(df['osf'] == True)])
    except Exception as e:
        print(f"Exeption fetching no_of_speed_violations : {e}")
        return -1

def license_plate_no(df):
    try:
        return df['lic_plate_no'].iloc[0]
    except Exception as e:
        print(f"Exeption fetching llicense_plate_no : {e}")
        return -1


#Trip info helper functions

def data_cleaning_trips_info(df):
    try:
        # Deleting duplicate rows
        df.drop_duplicates(subset=["trip_id","transporter_name","vehicle_number","date_time"], keep='last', inplace=True)
        # Removing empty values to NaN and deleting them from the table
        df.replace(r'^\s*$', np.nan, regex=True, inplace = True)
        new_df = df.dropna(subset=['transporter_name','vehicle_number','date_time'], inplace=False)
        # Freeing up the space for df garbage collector will be called here
        lst = [df]
        del lst
        return new_df
    except Exception as e:
        print(f"Exeption in data_cleaning_trips_info : {e}")
        return pd.DataFrame() 

def unix_time_millis(t):
    t = str(int(t))
    d=datetime.datetime.strptime(t, "%Y%m%d%H%M%S")
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((d - epoch).total_seconds())

def transporter_name(df,license_plate):
    try:
        return df[df['vehicle_number']==license_plate]['transporter_name'].iloc[0]
    except Exception as e:
        print(f"Exeption fetching transporter_name : {e}")
        return ""

def no_of_trips_completed(df,license_plate,start_time,end_time):
    try:
        df.loc[(df['epoch_time'] >= start_time) & (df['epoch_time'] < end_time)]
        freq_vehicle_number = df['vehicle_number'].value_counts().to_dict()
        return freq_vehicle_number[license_plate]
    except Exception as e:
        print(f"Exeption fetching no_of_trips_completed : {e}")
        return -1



