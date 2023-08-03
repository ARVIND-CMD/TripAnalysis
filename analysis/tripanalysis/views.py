from django.shortcuts import render
from django import forms 
import os
from math import radians, cos, sin, asin, sqrt
import pandas as pd
from tripanalysis.helper_functions import *

class InputForm(forms.Form): 
    start_time = forms.CharField(required=True,max_length=10,min_length=10,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9]+', 'title':'Enter start time(10 digit number) epoch time'}))
    end_time = forms.CharField(required=True,max_length=10,min_length=10,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9]+', 'title':'Enter end time (10 digit number) epoch time '}))

def home(request):
    if request.method=="POST":
        form = InputForm(request.POST)
        if form.is_valid():
            start_time = int(form.cleaned_data["start_time"])
            end_time = int(form.cleaned_data["end_time"])
            result_lst = []
            current_path = os.path.dirname(__file__)
            path = current_path+"\\EOL-dump"
            files = [file for file in os.listdir(path)]
            for file in files:
                if file[-4:] == ".csv":
                    filename = path+"\\"+file
                    df= pd.read_csv(filename)
                    new_df = data_cleaning_vehicle_trails(df)
                    filtered_data = filter_data_on_epoch_time(start_time,end_time,new_df)
                    total_distance_travelled = calculate_distance(filtered_data)
                    speed_violations_count = no_of_speed_violations(filtered_data)
                    license_plate = license_plate_no(filtered_data)
                    trip_info_file_path = path + "\\Trip-Info.xlsx"
                    trips_info_df = pd.read_excel(trip_info_file_path)
                    trips_info_df['epoch_time'] = trips_info_df.apply (lambda row: unix_time_millis(row['date_time']), axis=1)
                    no_of_trips = no_of_trips_completed(trips_info_df,license_plate,start_time,end_time)
                    trans_name = transporter_name(trips_info_df,license_plate)     
                    if not (license_plate == -1 or total_distance_travelled == -1 or no_of_trips == -1 or trans_name == "" or speed_violations_count == -1):    
                        new_lst = {'license_plate':license_plate,'total_distance_travelled':total_distance_travelled,'no_of_trips':no_of_trips,'avg_speed':'NA','trans_name':trans_name,'speed_violations_count':speed_violations_count}
                        result_lst.append(new_lst)                                   
            context = {"data": result_lst}
            return render(request,'tripanalysis/home.html', context)
        else:
            form = InputForm()
            context = {"form": form}
            return render(request,'tripanalysis/home.html', context)
    else:
        form = InputForm()
        context = {"form": form}
        return render(request,'tripanalysis/home.html', context)

