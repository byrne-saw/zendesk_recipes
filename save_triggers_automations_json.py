import requests, os, datetime, json
from dotenv import load_dotenv

# load and set variables from .env file
load_dotenv()

url = os.environ['ZD_URL']
user = os.environ['ZD_USER']
pwd = os.environ['ZD_PW']

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

def write_file(response, desc):
    """
    expects a requests response object and a str describing the response
    returns a json file with a current timestamp and desc in the file name
    """
    data = response.json()
    file_name = desc + time_string + '.json'
    with open(file_name, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
    

# get automations json and save to file

automations_url = url + 'automations'

get_desc = 'automations'
response = requests.get(automations_url, auth=(user, pwd))

check_status(response, get_desc)

write_file(response, get_desc)

# get triggers json and save to file

triggers_url = url + 'triggers'

get_desc = 'triggers'
response = requests.get(triggers_url, auth=(user, pwd))

check_status(response, get_desc)

write_file(response, get_desc)







