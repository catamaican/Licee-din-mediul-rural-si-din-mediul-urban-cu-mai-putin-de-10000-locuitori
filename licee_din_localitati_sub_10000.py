# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 08:00:58 2020

@author: maica
"""
import pandas as pd

from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from geopy.geocoders import OpenMapQuest
#geolocator = Nominatim(user_agent="licee_din_localitati_sub_10000")
#geolocator = GoogleV3(api_key='AIzaSyCxk0i1WQokYRgUxAZieq')
geolocator = OpenMapQuest(api_key='8s5EdY92L9QYcRIVSfc6yG8OlD0SUnNK')

from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

from tqdm import tqdm
tqdm.pandas()




df = pd.read_csv("d:\loc_med_rural.csv", sep=";")



#case sensitive
df['location_concat'] = df['DENUMIRE'].apply(lambda x: x.replace('"', '')) + ' ' + df['LOCALITATE'] #+ ' ' + df['judet']

#top 5
#df_top5 = df.head().copy()  #copie a obiectlui, ca altfel e doar un "view"/referinta
df_top5 = df.copy()  #copie a obiectlui, ca altfel e doar un "view"/referinta

#print (df_top5)

df_top5['location'] = df_top5['location_concat'].progress_apply(geocode)


punct_tuplu = df_top5['location'].apply(lambda loc: tuple(loc.point) if loc else None)
df_top5['point'] = punct_tuplu

df_top5['p_long'] = df_top5['location'].apply(lambda loc: loc.point.longitude if loc else None)
df_top5['p_lat'] = df_top5['location'].apply(lambda loc: loc.point.latitude if loc else None)

df_top5.to_csv("d:\loc_med_rural_geo.csv", index=False, header=True)


print (df_top5)
