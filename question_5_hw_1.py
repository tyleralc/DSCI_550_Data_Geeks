import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from urllib.request import urlopen
import csv
from pandas._libs.algos import rank_1d

##get all the data gathered and organized##

#place postsecondary school dataset into a pandas dataframe
df3=pd.read_csv('Postsecondary_School_Locations_Current.csv', nrows=7012)
#export the Names to a list 
name=df3['NAME'].tolist()
#place Modified bik dataset into a pandas dataframe
df = pd.read_csv("Modified Bik dataset - papers with endpoint reached.tsv", sep='\t', encoding = "ISO-8859-1", nrows=214)
#export the Affiliated universities to a list 
lst_univs=df['Affiliation University'].tolist()
#place HERD ranking dataset into a pandas dataframe
herd_rank = pd.read_excel('HERDrankings.xlsx', header =[2,3])

##WEATHER JSON EXAMPLE##
''' example row:
 
"CA-001":
{"location":"Alameda County",
"state":"California",
"stateAbbr":"CA",
"value":"60.2",
"rank":"120",
"anomaly":"2.4",
"mean":57.8}

'''
#create lists for the JSON data to be sorted into
codes_lst = []
rank_lst = []
temp_lst = []
anomaly_lst = []
all_county = []
all_state = []
#extract data from json to state_codes variable 
url = 'https://www.ncdc.noaa.gov/cag/county/mapping/110-tavg-202201-12.json'
response = urlopen(url)
data_json = json.loads(response.read())
state_codes = data_json['data']
#iterate to get the various features from the json via state_codes
for i in state_codes:
  codes_lst.append(i)
  counties = state_codes[i]['location']
  all_county.append(counties)

  states = state_codes[i]['stateAbbr']
  all_state.append(states)

  rank = state_codes[i]["rank"]
  rank_lst.append(rank)

  temp = state_codes[i]["mean"]
  temp_lst.append(temp)

  anomaly = state_codes[i]["anomaly"]
  anomaly_lst.append(anomaly)

##create a clean list of universities in the USA to match with post secondary school and HERD datasets##
def univ_clean(lst_univs, name):
  USA="United States of America"
  filtered_lst=[]
  for x in lst_univs:
      if USA in str(x):
          filtered_lst.append(str(x))
      else:
          filtered_lst.append('NaN')
  name_cleaned=[]

  for affil in filtered_lst:
      if affil == 'NaN':
          name_cleaned.append('NaN')
      elif 'University' not in affil:
          name_cleaned.append('NaN')
      else:
          for univ in name:
              if univ in affil:
                  name_cleaned.append(univ)
  return name_cleaned

##functions to get the specific features for each affiliated school##
#function to find the state that the affiliated university is in 
def state(univ):
    name=df3['NAME'].tolist()
    state=df3['STATE'].tolist()
    list_nameandstate=[]
    for index in range(len(name)):
        tup=(name[index],state[index])
        list_nameandstate.append(tup)
    for tup in list_nameandstate:
        if univ in tup[0]:
            return tup[1]
#function to find the locale score of the affiliated university
def locale(univ):
    name=df3['NAME'].tolist()
    locale=df3['LOCALE'].tolist()
    list_nameandlocale=[]
    for index in range(len(name)):
        tup=(name[index],locale[index])
        list_nameandlocale.append(tup)
    
    for tup in list_nameandlocale:
        if univ in tup[0]:
            return tup[1]
#function to find the county that the affiliated university is in 
def county(univ):
    name=df3['NAME'].tolist()
    nmcnty=df3['NMCNTY'].tolist()
    list_nameandnmcnty=[]
    for index in range(len(name)):
        tup=(name[index],nmcnty[index])
        list_nameandnmcnty.append(tup)
    
    for tup in list_nameandnmcnty:
        if univ in tup[0]:
            return tup[1]
#function to get the rank in R&D expenditures in the USA
def R_D_rank(univ):
    name = herd_rank['Institution'].values.tolist()
    rank = herd_rank[(2019, 'Rank')].values.tolist()
    list_nameandrank=[]
    for index in range(len(name)):
        tup=(name[index],rank[index])
        list_nameandrank.append(tup)
    for tup in list_nameandrank:
        if univ in tup[0]:
            return tup[1]
        else:
            return '-1'

#function to get the percentile in R&D expenditures in the USA
def percentile(univ):
    name = herd_rank['Institution'].values.tolist()
    perc = herd_rank[(2019, 'Percentile')].values.tolist()
    list_nameandperc=[]
    for index in range(len(name)):
        tup=(name[index],perc[index])
        list_nameandperc.append(tup)
    for tup in list_nameandperc:
        if univ in tup[0]:
            return tup[1]
        else:
            return '-1'
#function to get the total amount of R&D expenditures in the USA
def R_D_exp(univ):
    name = herd_rank['Institution'].values.tolist()
    R_D = herd_rank[(2019, 'R&D expenditures')].values.tolist()
    list_nameandR_D=[]
    for index in range(len(name)):
        tup=(name[index],R_D[index])
        list_nameandR_D.append(tup)
    for tup in list_nameandR_D:
        if univ in tup[0]:
            return tup[1]
        else:
            return '-1'

##adding all features to the bik dataset##
#creation of list to place into the columns in the bik dataset
county_list=[]
locale_list=[]
state_list=[]
R_D_rank_list=[]
percentile_list=[]
R_D_exp_list=[]
#calling of univ_clean to get the clean list of USA univ to get each feature based on the university
univ_c = univ_clean(lst_univs, name)
for univ in univ_c:
    if univ == 'NaN':
        county_list.append('NaN')
        locale_list.append('NaN')
        state_list.append('NaN')
        R_D_rank_list.append('NaN')
        percentile_list.append('NaN')
        R_D_exp_list.append('NaN')
    else:
        county_list.append(county(univ))
        locale_list.append(locale(univ))
        state_list.append(state(univ))
        R_D_rank_list.append(R_D_rank(univ))
        percentile_list.append(percentile(univ))
        R_D_exp_list.append(R_D_exp(univ))

#weather feature additions(requires completed lists for previous features to work)
#function to get rank of average tempature 
def rank_weather(all_county, all_state, rank_lst, county_list, state_list):
  rank_match = []
  for i in range(len(county_list)):
    for j in range(len(all_county)):
      if county_list[i] == all_county[j] and state_list[i] == all_state[j]:
        rank_match.append(rank_lst[j])
    if len(rank_match) == i:
      rank_match.append('NaN') 
  return rank_match
#function to  get average tempature
def temp_weather(all_county, all_state, temp_lst, county_list, state_list):
  temp_match = []
  for i in range(len(county_list)):
    for j in range(len(all_county)):
      if county_list[i] == all_county[j] and state_list[i] == all_state[j]:
        temp_match.append(temp_lst[j])
    if len(temp_match) == i:
      temp_match.append('NaN') 
  return temp_match
#function to get the anomaly value
def anomaly_weather(all_county, all_state, anomaly_lst, county_list, state_list):
  anomaly_match = []
  for i in range(len(county_list)):
    for j in range(len(all_county)):
      if county_list[i] == all_county[j] and state_list[i] == all_state[j]:
        anomaly_match.append(anomaly_lst[j])
    if len(anomaly_match) == i:
      anomaly_match.append('NaN') 
  return anomaly_match
#call all the function to create lists of the weather information
rank_final=rank_weather(all_county, all_state, rank_lst, county_list, state_list)
temp_final=temp_weather(all_county, all_state, temp_lst, county_list, state_list)
anomaly_final=anomaly_weather(all_county, all_state, anomaly_lst, county_list, state_list)
##placing of all the features into the dataframe##
df['Rank']=rank_final
df['Temperature']=temp_final
df['Anomaly']=anomaly_final
df['County']=county_list
df['Locale']=locale_list
df['State']=state_list
df['R&D Rank']=R_D_rank_list
df['Percentile']=percentile_list
df['R&D Expenditures']=R_D_exp_list
#drop the extra unmaed columns 
df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
##export to a tsv file##
df.to_csv('Final_bik_dataset.tsv',sep ='\t') 