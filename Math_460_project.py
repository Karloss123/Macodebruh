##Our Final Code/Master Document for Python
import numpy as np
import matplotlib.pyplot as plt
import quandl

from scipy import stats
import matplotlib.dates as mdates
import datetime, time
import pandas as pd
import quandl
from event_reader import read_events
#quandle key is needed to be able to grab more data from quandl API
quandl.ApiConfig.api_key = 'WoytVVADas1zdPH8dBTh'

def nan_helper(y):
    return np.isnan(y), lambda z: z.nonzero()[0]


def index_of(date, list_of_dates):
  #takes a date in string format and a list and either returns the index or returns a flag depending on whether the date exists in the list
    if date in list_of_dates:
        return list_of_dates.index(date)
    else:
        return -1

def FormatDate(objectDate,strFormat="%Y-%m-%d"):
  #allows you to go between different date formats, and transforms a pandas date-time to a readable string to parse through a text file
    return objectDate.strftime(strFormat)  

def dates_list(list_of_dates):
  #takes a list of improperly formatted dates and transforms the into format that dates are mostly represented as in text
    new_list = list()
    for i in list_of_dates:
        new_list.append(FormatDate(i))
    return(new_list)

def compare(dataset,event,window, figflag):
  #takes a dataframe, an event date, and fits/compares the line of best fit for the the event interval and the entire dataset
    dates = dates_list(dataset.index)
    event_loc = dataset.index.get_loc(event)
    start = event_loc -window
    end = event_loc + window
    event_data = dataset[event_loc:end]
    prior_data = dataset[start: event_loc]
    clean_data= dataset.dropna()
    clean_event_data = event_data.dropna()
    ref = np.array(clean_data.index)
    ref_nums = mdates.date2num(ref)
    days_ref = ref_nums - ref_nums[0]
    slope_ref, intercept_ref, r_value_ref,p_value_ref, std_err_ref = stats.linregress(days_ref, clean_data["Open"])
    event = np.array(clean_event_data.index)
    event_nums = mdates.date2num(event)
    days_event = event_nums - ref_nums[0]
    slope_event, intercept_event, r_value_event, p_value_event, std_err_event = stats.linregress(days_event, clean_event_data["Open"])
    diff_slope = slope_event - slope_ref
    start_interval = dates[start]
    end_interval = dates[end]
    if figflag == 1:
        plt.plot(days_ref, clean_data["Open"], '.', label = 'original data')
        plt.plot(days_ref, intercept_ref + slope_ref* days_ref, "r", label = "reference slope ≈ "+ str(round(slope_ref,2)))
        plt.plot(days_event, intercept_event + slope_event * days_event, "c", label = "event slope ≈ " + str(round(slope_event,2)))
        plt.legend()
        plt.show()
    return([diff_slope, start_interval,event, end_interval])



    
def compare_multiple(dataset, events,window, figflag):
    dates = dates_list(dataset.index)
    differences = list()
    clean_data= dataset.interpolate()
    ref = np.array(clean_data.index)
    ref_nums = mdates.date2num(ref)
    days_ref = ref_nums - ref_nums[0]
    slope_ref, intercept_ref, r_value_ref,p_value_ref, std_err_ref = stats.linregress(days_ref, clean_data["Open"])
    if figflag ==1:
        plt.plot(days_ref, clean_data["Open"], '.', label = 'original data')
        plt.plot(days_ref, intercept_ref + slope_ref* days_ref, "r", label = "reference slope ≈ "+ str(round(slope_ref,2)))
        plt.legend()
    for event_day in events:
        indx = index_of(event_day, dates)
        if indx == -1:
            day_val = int(event_day[8:10])
            day_val +=1
            if day_val >= 10:
                event_day = event_day[0:8]+str(day_val)
            else:
                event_day = event_day[0:8]+'0'+str(day_val)
            
            indx = index_of(event_day, dates)
            if indx == -1:
                day_val = int(event_day[8:10])
                day_val -= 2
                if day_val >= 10:
                    event_day = event_day[0:8]+str(day_val)
                else:
                    event_day = event_day[0:8]+'0'+str(day_val)
            
                indx = index_of(event_day, dates)
                if indx == -1:
                    continue
        event_data = dataset[indx:indx+window]
        clean_event_data = event_data.interpolate()
        event = np.array(clean_event_data.index)
        event_nums = mdates.date2num(event)
        days_event = event_nums - ref_nums[0]
        slope_event, intercept_event, r_value_event, p_value_event, std_err_event = stats.linregress(days_event, clean_event_data["Open"])
        diff_slope = slope_event - slope_ref
        differences.append(diff_slope)
        if figflag ==1:
            plt.plot(days_event, intercept_event + slope_event * days_event, linewidth = 3.0)
    return(differences)





def compare_multiple_better(dataset, events,window_forward,window_backward, figflag):
  #takes multiple events and does the same thing that compare does, but also allows a forward and backwards window, and also adjusts for events in the list that are not in the dataset
    dates = dates_list(dataset.index)
    differences = list()
    clean_data= dataset.interpolate()
    ref = np.array(clean_data.index)
    ref_nums = mdates.date2num(ref)
    days_ref = ref_nums - ref_nums[0]
    slope_ref, intercept_ref, r_value_ref,p_value_ref, std_err_ref = stats.linregress(days_ref, clean_data["Open"])
    if figflag ==1:
        plt.plot(days_ref, clean_data["Open"], '.', label = 'original data')
        plt.plot(days_ref, intercept_ref + slope_ref* days_ref, "r", label = "reference slope ≈ "+ str(round(slope_ref,2)))
        plt.legend()
        plt.xlabel("number of days")
        plt.ylabel("Opening Price SP500 in USD")
    for event_day in events:
        indx = index_of(event_day, dates)
        if indx == -1:
            day_val = int(event_day[8:10])
            day_val +=1
            if day_val >= 10:
                event_day = event_day[0:8]+str(day_val)
            else:
                event_day = event_day[0:8]+'0'+str(day_val)
            
            indx = index_of(event_day, dates)
            if indx == -1:
                day_val = int(event_day[8:10])
                day_val -= 2
                if day_val >= 10:
                    event_day = event_day[0:8]+str(day_val)
                else:
                    event_day = event_day[0:8]+'0'+str(day_val)
            
                indx = index_of(event_day, dates)
                if indx == -1:
                    continue
        ref_interval = clean_data[indx-window_backward: indx+window_forward]
        reference = np.array(ref_interval.index)
        reference_nums = mdates.date2num(reference)
        days_reference = reference_nums - reference_nums[0]
        slope_reference, intercept_reference, r_value_reference, p_value_reference, std_err_reference = stats.linregress(days_reference, ref_interval["Open"])
        event_data = clean_data[indx:indx+window_forward]
        event = np.array(event_data.index)
        event_nums = mdates.date2num(event)
        days_event = event_nums - ref_nums[0]
        slope_event, intercept_event, r_value_event, p_value_event, std_err_event = stats.linregress(days_event, event_data["Open"])
        diff_slope = slope_event - slope_reference
        differences.append(diff_slope)
        if figflag ==1:
            plt.plot(days_event, intercept_event + slope_event * days_event, linewidth = 3.0)
    return(differences)


mydata = quandl.get("CHRIS/CME_SP2", qopts = {'columns': ['open','high','low','last','volume']}, start_date= "2013-01-01", end_date="2018-10-01")
#basic way of using quandl to get data

events, descriptions = read_events()
#we have a txt file with the event dates and descriptions that we are reading from
diffs = compare_multiple_better(mydata,events, 10,10,0)
diffs_array = np.array(diffs)
nans, x = nan_helper(diffs_array)
diffs_array[nans]= np.interp(x(nans), x(~nans), diffs_array[~nans])
#the two lines above are magic for dealing with nan's in an array
diffs_list = diffs_array.tolist()



def get_bins(list_of_nums, very_good, good ,bad, very_bad):
  #takes an array of numbers and separates them based on their value, named in terms of good and bad for me to remember what it does
    indices_very_good = [list_of_nums.index(i) for i in list_of_nums if i >= very_good]
    indices_good = [list_of_nums.index(i) for i in list_of_nums if i >= good]
    indices_neutral = [list_of_nums.index(i) for i in list_of_nums if bad < i < good ]
    indices_bad = [list_of_nums.index(i) for i in list_of_nums if i <= bad]
    indices_very_bad = [list_of_nums.index(i) for i in list_of_nums if i <= very_bad]
    return([indices_very_good, indices_good, indices_neutral, indices_bad, indices_very_bad])

list_of_bins = get_bins(diffs_list, 4,2,2,4)   

major_positive = list_of_bins[0]
minor_positive = list_of_bins[1]
neutral = list_of_bins[2]
minor_negative = list_of_bins[3]
major_negative = list_of_bins[4]



    

#To plot the different slopes on top of the reference slope
#plt.hist(diffs_array, 50, facecolor='green', alpha=0.75, edgecolor = "black",linewidth = 1.2)
#plt.ylabel("Frequency")
#plt.xlabel("Event Slope - Reference Slope: Reference 15 days, Event 10 days")
#plt.show()



#earlier code that I do not want to throw out yet
#Example (uncomment if you wanna try it out)
##event = "2016-02-01"
#compare(dataset, event, 14,figflag = 1)


#plt.plot(days_ref, clean_ref_data["Open"], 'o', label = 'original data')
#plt.plot(days_ref, intercept_ref + slope_ref* days_ref, label = "reference slope ≈ "+ str(round(slope_ref,2)))
#plt.plot(days_event, intercept_event + slope_event * days_event, label = "event slope ≈ " + str(round(slope_event,2)))

##plt.show()




#f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
#f.suptitle('Sharing Y axis')
#ax1.plot(days_ref, clean_ref_data["Open"], 'o', label = 'original data')
##ax1.plot(days_event, intercept_event + slope_event*days_event, "c", label = "event slope ≈ " + str(round(slope_event,2)))

#ax2.plot(days_ref, clean_ref_data["Open"], 'o', label = 'original data')
#ax2.plot(days_ref, intercept_ref + slope_ref * days_ref, "r", label = "reference slope ≈ " + str(round(slope_ref,2)))
#ax2.plot(days_event, intercept_event + slope_event*days_event, "c", label = "event slope ≈ " + str(round(slope_event,2)))
#plt.show()



    
    
