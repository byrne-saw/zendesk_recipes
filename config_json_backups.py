"""
ToDo: 
    Write docstring
    Incorporate Check Status into paginate fuction
    Dry up automations / ticket fields / triggers code with a loop that goes through endpoints

"""
import requests
import os
import datetime
import json
from dotenv import load_dotenv

# load and set variables from .env file
load_dotenv()

URL = os.environ['ZD_URL']
USER = os.environ['ZD_USER']
PWD = os.environ['ZD_PW']

# timestamp string for file names
time_string = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 

# check status and save file functions

def check_status(response, desc):
    """ 
    expects a requests response object and a str describing the response
    breaks and prints error if there is a problem with the response
    """
    if response.status_code != 200:
        print('Status', response.satus_code, 'Problem with the', desc, 'request. Exiting.')
        exit()

def write_file(json_obj, desc):
    """
    expects a json object and a str describing the response
    returns a json file with a current timestamp and desc in the file name
    """
    file_name = desc + '_' + time_string + '.json'
    with open(file_name, 'w') as f:
        json.dump(json_obj, f, sort_keys=True, indent=4)

def paginate(url, dict_key):
    """
    expects a string url and string dict_key
    returns a json object
    https://developer.zendesk.com/rest_api/docs/support/introduction#pagination
    https://develop.zendesk.com/hc/en-us/articles/360053166453
    """
    s = requests.Session()
    s.auth = (USER, PWD)
    json_obj = {dict_key:[]}
    while url:
        response = s.get(url)
        data = response.json()
        for value in data[dict_key]:
            json_obj[dict_key].append(value)
        url = data['next_page']

    return json_obj


# get automations json and save to file

get_desc = 'automations'
automations_url = URL + get_desc

automations = paginate(automations_url, get_desc)
write_file(automations, get_desc)

# get triggers json and save to file

get_desc = 'triggers'
triggers_url = URL + get_desc

triggers = paginate(triggers_url, get_desc)

write_file(triggers, get_desc)


# get ticket_fields json and save to file


get_desc = 'ticket_fields'
tixfield_url = URL + get_desc

tixfields = paginate(tixfield_url, get_desc)
write_file(tixfields, get_desc)




