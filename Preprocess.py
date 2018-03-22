# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 22:43:42 2017

@author: fandong
"""
import os
import pandas as pd
import numpy as np


np.random.seed(1)
os.chdir('C:/Users/fando/Box Sync/Springboard/Capstone Project/Data')
content = pd.read_csv("ContentTable.csv")
allData = pd.DataFrame()

fileList = list(range(1,21))
calendar = pd.read_csv('calendar_1.csv', dtype={'listing_id':str})
id_list = calendar.listing_id.unique()  
id_list = np.random.choice(id_list, int(len(id_list)*(1/5)), replace=False)

for f in fileList:
    calendar = pd.read_csv('calendar_'+str(f)+'.csv', dtype={'listing_id':str})
    listings = pd.read_csv('listings_'+str(f)+'.csv', dtype={'id':str, 'zipcode': str})
    print(listings.shape)
    calendar['file_index'] = f
    listings = listings.rename(columns={'id' : 'listing_id'})
    calendar['date'] = pd.to_datetime(calendar['date'])
    listings['last_scraped'] = pd.to_datetime(listings['last_scraped'])
    date_cutoff = pd.to_datetime(content.Date[content.Index==f+1])
    calendar = calendar[calendar['date']<date_cutoff.iloc[0]]
    calendar_sample = calendar[calendar['listing_id'].isin(id_list)]
    allData = allData.append(pd.merge(calendar_sample, listings, on='listing_id'))
    print(len(allData))

by_id = allData.groupby('listing_id')
by_id = by_id.size().reset_index()
by_id = by_id.loc[by_id[0]>730]
id_complete = by_id.listing_id
allData = allData[allData['listing_id'].isin(id_complete)]

dtype_dict = allData.dtypes.apply(lambda x: x.name).to_dict()
dtype_dict.update({'date': 'object', 'last_scraped': 'object'})
np.save('dtype_dict.npy', dtype_dict) 
allData.to_csv('allData.txt', index=False, sep=' ', header=True)

#remove columns: price_y
#impute NAs: access, bathrooms, bedrooms, beds, cleaning_fee, description, host_about, host_acceptance_rate //
#            host_has_profile_pic, host_identity_verified, host_is_superhost, host_listings_count, host_location//
#            host_name, host_neighbourhood, 