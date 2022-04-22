#!/usr/bin/env python
# coding: utf-8

# 
# 
# ```
# # This is formatted as code
# ```
# 
# # Home Work - Data Preparation <font color='blue'></font>

# ## Instructions <font color='blue'> </font>

# NYC bikes September 2021 data from this link: https://s3.amazonaws.com/tripdata/202109-citibike-tripdata.csv.zip

# ## Import Library

# In[1]:


from __future__ import division

import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('pylab', 'inline')
import datetime as dt
import calendar
from haversine import haversine


# ## Questions <font color='blue'> </font>

# ### <font color='black'>1) How many rows in the NYC bikes September 2021 data?</font>

# In[4]:


df = pd.read_csv('202109-citibike-tripdata.csv')
df.head()


# In[3]:


print("Terdapat sejumlah " + str(len(df)) + " rows dalam dataset NYC bikes bulan September 2021")


# ### <font color='black'>2) How many rows with 'electric_bike' in the NYC bikes September 2021 data?</font>

# In[4]:


electric_bike = df[df.rideable_type=='electric_bike']
electric_bike.head()


# In[5]:


electric_bike['rideable_type'].unique() #Validasi hanya ada tipe electric bike


# In[6]:


print("Terdapat sejumlah " + str(len(electric_bike)) + " rows electric bike")


# ### <font color='black'>3) How many rows with 'member' and 'classic_bike' in the NYC bikes September 2021 data?</font>

# In[7]:


elec_member = df[(df.rideable_type=='electric_bike') & (df.member_casual=='member')]
elec_member.head()


# In[8]:


print("Terdapat sejumlah " + str(len(elec_member)) + " rows member dengan classic bike")


# ### <font color='black'>4) What is the overall average trip duration (in seconds)?</font>

# In[9]:


df['started_at'] =  pd.to_datetime(df['started_at'], format="%Y/%m/%d %H:%M")
df['ended_at'] =  pd.to_datetime(df['ended_at'], format="%Y/%m/%d %H:%M")


# In[10]:


df.dtypes


# In[11]:


df['duration'] = df['ended_at'] - df['started_at']
df['duration'] = df['duration'].dt.total_seconds()

df.head()


# In[12]:


print("Average trip duration: " + str(round(df.duration.mean(), 3)) + " seconds")


# ### <font color='black'>5) What is the average trip duration (in seconds) in the weekend?</font>

# In[13]:


index_day = range(0,7)
for i in index_day:
    print (i, calendar.day_name[i])


# In[14]:


df['start_day'] = df.started_at.apply(lambda x: calendar.day_name[x.weekday()])
df.head()


# In[15]:


df['is_weekend'] = df.start_day.apply(lambda x: 1 if (x == 'Saturday' or x == 'Sunday') else 0)


# In[16]:


col = ['started_at', 'start_day', 'is_weekend']
df[col].sample(5)


# In[17]:


avg_weekend = (df['duration'][df['is_weekend'] == 1]).mean()
print("Average trip duration in weekend: " + str(round(avg_weekend, 3)) + " seconds")


# ### <font color='black'>6) What is the average trip duration (in seconds) in Monday?</font>

# In[18]:


avg_monday = (df['duration'][df['start_day'] == 'Monday']).mean()
print("Average trip duration in monday: " + str(round(avg_monday, 3)) + " seconds")


# ### <font color='black'>7) What is the overall average distance (in km) for non circle trip?</font> <font color='blue'> (non circle trip means that the start station is different with the end station)</font>

# In[5]:


df['is_circle_trip'] = df.apply(lambda x: 1 if x['start_station_id'] == x['end_station_id'] else 0, axis = 1)


# In[6]:


df.sample(5)


# In[7]:


def distance_stations(x):
    start_lat = x['start_lat']
    start_long = x['start_lng']
    end_lat = x['end_lat']
    end_long = x['end_lng']
    return haversine((start_lat,start_long),(end_lat,end_long))


# In[8]:


df['traveled_distance'] = df.apply(distance_stations, axis = 1)


# In[9]:


df.sample(5)


# In[10]:


distance_station_data = df[['start_station_name', 'end_station_name', 'traveled_distance']]
distance_station_data.sample(5)


# In[11]:


avg_dist_noncycle = (df['traveled_distance'][df['is_circle_trip'] == 0]).mean()
print("Average trip distance for non circle: " + str(round(avg_dist_noncycle, 3)) + " km")


# ### <font color='black'>8) What is longest distance (in km)?</font>

# In[12]:


print("Longest trip distance: " + str(round(max(df['traveled_distance']), 3)) + " km")


# ### <font color='black'>9) What is the average distance (in km) for non circle trip for 'member'?</font>

# In[13]:


noncircle_member = df[(df.is_circle_trip==0) & (df.member_casual=='member')]
print("Average trip distance for non circle & member: " + str(round(noncircle_member['traveled_distance'].mean(), 3)) + " km")


# ### <font color='black'>10) How many circle trip?</font>

# In[17]:


circle = df[df['is_circle_trip']==1]
circle.sample(10)


# In[19]:


print("Jumlah circle trip: " + str(len(circle)))

