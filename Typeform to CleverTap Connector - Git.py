#!/usr/bin/env python
# coding: utf-8

# In[155]:


## Picks up data from Typeform with a single question & updates a custom user property of the UserID in Clevertap with the answer of typeform 
## While testing CT post API, use ?dryRun=1 after the post api url - this will help in checking the response without making the changes in CT values
## Code by Yatin Garg - yatingarg87@gmail.com


import pandas as pd
import requests
import json

#GETTING DATA FROM TYPEFORM AS A DICTIONARY OF USERIDS (Hidden parameter in typeform) AS KEYS & USER RESPONSES AS VALUES OF THE CUSTOM USER PROPERTY

# URL of Typeform API along with form ID without <> - XYZ in this case
url_typeform = "https://api.typeform.com/forms/<XYZ>/responses"


# Authorization to access typeform data with Personal token 
headers = {
  'Authorization': 'Bearer <token>'
}

# Packaging get request & convert that into a json format
response = requests.get(url_typeform, headers=headers)
typeform_data = response.json()

# For testing if the intended data is received properly 
# for item in typeform_data['items']:
#     print(item['hidden']['userid'])
#     if item['answers'] and item['hidden']['userid']!= 'xxxxx':
#         print(item['answers'][0]['choice']['label'])


dict_typeform = {} #Declaring an empty dictionary which will carry the key value pairs of data received from typeform
for item in typeform_data['items']:
    if item['answers'] and item['hidden']['userid']!= 'xxxxx': #xxxxx is the default value of userid in typeform's hidden field
        dict_typeform[item['hidden']['userid']] = item['answers'][0]['choice']['label'] #Populating the dictionary
        
# POSTING STUFF TO CLEVERTAP PROFILE IDS  

#Authentication into Clevertap

headers = {
    'X-CleverTap-Account-Id': '<AccountID>',
    'X-CleverTap-Passcode': '<Passcode>',
    'Content-Type': 'application/json; charset=utf-8',
}


# This to test if values against a particular user id from Clevertap 

# params = (
#     ('identity', 'user_id'),
# )

# r = requests.get('https://api.clevertap.com/1/profile.json', headers=headers, params=params)
# json_data = r.json()
# print(json_data)


# Loop to post each value of dictionary one by one to Clevertap (Unoptimized Way)
# for keys,items in dict_typeform.items(): 
#     up_data = str({"d": [{"identity": keys,"type": "profile","profileData": {"Alternate_MOC": items}}]})
#     r2 = requests.post('https://api.clevertap.com/1/upload', headers=headers, data=up_data)
#     print(r2)


up_json={} #JSON which will be passed to CT with POST request
up_array=[] #Array or List of all JSONs
dummy_counter = 1 #Used in the logic of making API call once we have 100 key value pairs to post - CT limitation

#Loop over typeform dictionary created earlier to create a json of all key value pairs from typerform responses
for keys,items in dict_typeform.items():
    temp_json = {"identity": keys,"type": "profile","profileData": {"Alternate_MOC": items}} #Creates a JSON of every typeform response received
    up_array.append(temp_json) #Appends the temp_json to the list
    if dummy_counter%100 == 0:
        up_json['d'] = up_array #Assigns the list of jsons created above to 'd' - as specified in Clevertap documentation
        CT_Update_APIcall = requests.post('https://api.clevertap.com/1/upload', headers=headers, data=str(up_json)) #Post API hit which creates "Alternate_MOC" custom profile property & updates its value
        up_array = []
        up_json = {}
    dummy_counter +=1

if dummy_counter%100 != 0:
    up_json['d'] = up_array #Assigns the list of jsons created above to 'd' - as specified in Clevertap documentation
    CT_Update_APIcall = requests.post('https://api.clevertap.com/1/upload', headers=headers, data=str(up_json)) #Post API hit which creates "Alternate_MOC" custom profile property & updates its value

print(CT_Update_APIcall) #Gives the response code - 200 means success 


# In[ ]:




