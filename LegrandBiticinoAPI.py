import time, json, yaml, requests,os

class LegrandBiticinoAPI:
  def __init__(self):
    self.configFile = "config.yaml"
    self.CONFIG = self.load_yaml()

    # As a very first step let's initialise the config file
    for parameter in ['client_id', 'client_secret', 'redirect_uri', 'Ocp-Apim-Subscription-Key']:
      if parameter not in self.CONFIG.keys():
        in_value =  input("          >> Paste here your " + parameter + ": ")
        self.save_to_yaml({parameter:in_value})

    # If not availbe, generate the Authorize Code
    if 'authorize_code' not in self.CONFIG.keys():
      self.get_authorize_code()

    # If not availbe, generate the Access Token
    if 'access_token' not in self.CONFIG.keys():
      self.get_access_token()
    
    # If needed refresh the Access Token
    self.refresh_token_if_needed()

    # Default https request header
    self.header = { 'Ocp-Apim-Subscription-Key': self.CONFIG['Ocp-Apim-Subscription-Key'],
                    'Authorization': self.CONFIG['access_token'],
                    'Content-Type': 'application/json'}
  
  def load_yaml(self):
    local_path = os.path.dirname(__file__)
    with open(local_path + "/" + self.configFile, "r") as f:
      return yaml.safe_load(f)
  
  def save_to_yaml(self,data):
    for k in data.keys():
      self.CONFIG[k] = data[k]
    with open(self.configFile,'w') as f:
        yaml.safe_dump(self.CONFIG, f)
    self.CONFIG = self.load_yaml()

  def get_access_token(self):
    url = "https://partners-login.eliotbylegrand.com/token"
    payload={'code': self.CONFIG['authorize_code'],
            'grant_type': 'authorization_code',
            'client_secret': self.CONFIG['client_secret'],
            'client_id': self.CONFIG['client_id']}
    response = requests.request("POST", url, headers={}, data=payload, files=[])
    if response.status_code == 200:
      access_token = 'Bearer ' + str(json.loads(response.text)['access_token'])
      refresh_token = str(json.loads(response.text)['refresh_token'])
      access_token_expires_on = json.loads(response.text)['expires_on']
      self.save_to_yaml({'access_token' : access_token, 'refresh_token' : refresh_token, 'access_token_expires_on' : access_token_expires_on })
      return {'status_code' : response.status_code, 'text' : json.loads(response.text)}
    elif response.status_code == 400:
      self.get_authorize_code()
      return self.get_access_token()
      
  def get_refresh_token(self):
    url = "https://partners-login.eliotbylegrand.com/token"
    payload={'refresh_token': self.CONFIG['refresh_token'],
            'grant_type': 'refresh_token',
            'client_secret': self.CONFIG['client_secret'],
            'client_id': self.CONFIG['client_id']}
    response = requests.request("POST", url, headers={}, data=payload, files=[])
    access_token = 'Bearer ' + str(json.loads(response.text)['access_token'])
    refresh_token = str(json.loads(response.text)['refresh_token'])
    access_token_expires_on = json.loads(response.text)['expires_on']
    self.save_to_yaml({'access_token' : access_token, 'refresh_token' : refresh_token, 'access_token_expires_on' : access_token_expires_on })
    #print('Access_token = ' + access_token + "\nRefresh_token = " + refresh_token + "\n")
    self.__init__()
    return {'status_code' : response.status_code, 'text' : json.loads(response.text)}

  def refresh_token_if_needed(self):
    if 'access_token_expires_on' not in self.CONFIG.keys():
      self.get_access_token()
    if int(time.time()) > self.CONFIG['access_token_expires_on']:
      self.get_refresh_token()
  
  def get_authorize_code(self):
    state = str(int(time.time()))  # Random string 
    url_auth = ("https://partners-login.eliotbylegrand.com/authorize?" +
                "client_id=" + self.CONFIG['client_id'] + 
                "&response_type=code" +
                "&state=" + state +
                "&redirect_uri=" + self.CONFIG['redirect_uri'])
    print("""
          *********************************************************************
          This flow should be done once during account linking, afterwards
          you should use the get_access_token() and refresh_token_if_needed().
          *********************************************************************
          Follow those steps to obtain you authentication code:
          1\ Open this URL in your browser : """ + url_auth + """
          2\ Complete the username & password Sign-in
          3\ Accept the permissions to access your data
          4\ Finally, after the redirection copy and paste here following the browser URL containing the code
          """)
    redirect_url =  input("          >> Paste here the browser URL:")
    if redirect_url.find(state) != -1 and redirect_url.find('code=') != -1:
      code = redirect_url[redirect_url.find('code=')+5 : redirect_url.find('&state')]
      #print("\nAuthorize Code = " + str(code))
      self.save_to_yaml({'authorize_code' : code})
      return code
    else:
      raise SystemExit("ERROR: Unable to identify the Authorize Code, you may provided an invalid URL. Please try again.") 

  def echo(self):
    self.refresh_token_if_needed()
    url = "https://api.developer.legrand.com/echo/resource"
    response = requests.request("POST", url, headers=self.header, data=json.dumps({"Test1": "OK", "Test2": 1}))
    return {'status_code' : response.status_code, 'text' : response.text}

  def get_plants(self):
    self.refresh_token_if_needed()
    url = "https://api.developer.legrand.com/smarther/v2.0/plants"
    response = requests.request("GET", url, headers=self.header, data={})
    return {'status_code' : response.status_code, 'text' : json.loads(response.text)}

  def get_topology(self, plantId):
    self.refresh_token_if_needed()
    url = "https://api.developer.legrand.com/smarther/v2.0/plants/" + plantId + "/topology"
    response = requests.request("GET", url, headers=self.header, data={})
    return {'status_code' : response.status_code, 'text' : json.loads(response.text)}

  def set_chronothermostat_status(self,plantId, moduleId, data):
    self.refresh_token_if_needed()
    url = ("https://api.developer.legrand.com/smarther/v2.0/chronothermostat/thermoregulation/addressLocation/plants/" + plantId +
            "/modules/parameter/id/value/" + moduleId )
    response = requests.request("POST", url, headers=self.header, data=json.dumps(data))
    return {'status_code' : response.status_code, 'text' : response}

  def get_chronothermostat_status(self,plantId, moduleId):
    self.refresh_token_if_needed()
    url = ("https://api.developer.legrand.com/smarther/v2.0/chronothermostat/thermoregulation/addressLocation/plants/" + plantId +
            "/modules/parameter/id/value/" + moduleId )
    response = requests.request("GET", url, headers=self.header, data={})
    return {'status_code' : response.status_code, 'text' : json.loads(response.text)}

  def get_chronothermostat_measures(self,plantId, moduleId):
    self.refresh_token_if_needed()
    url = ("https://api.developer.legrand.com/smarther/v2.0/chronothermostat/thermoregulation/addressLocation/plants/" + plantId +
            "/modules/parameter/id/value/" + moduleId + "/measures" )
    response = requests.request("GET", url, headers=self.header, data={})
    return {'status_code' : response.status_code, 'text' : json.loads(response.text)}

  def get_chronothermostat_programlist(self,plantId, moduleId):
    self.refresh_token_if_needed()
    url = ("https://api.developer.legrand.com/smarther/v2.0/chronothermostat/thermoregulation/addressLocation/plants/" + plantId +
            "/modules/parameter/id/value/" + moduleId + "/programlist" )
    response = requests.request("GET", url, headers=self.header, data={})
    return {'status_code' : response.status_code, 'text' : json.loads(response.text)}

  def get_subscriptions_C2C_notifications(self):
    self.refresh_token_if_needed()
    url = ("https://api.developer.legrand.com/smarther/v2.0/subscription")
    response = requests.request("GET", url, headers=self.header, data={})
    return {'status_code' : response.status_code, 'text' : json.loads(response.text) if response.status_code == 200  else response.text }

  def set_subscribe_C2C_notifications(self,plantId,data):
    self.refresh_token_if_needed()
    url = ("https://api.developer.legrand.com/smarther/v2.0/plants/" + plantId + "/subscription")
    response = requests.request("POST", url, headers=self.header, data=json.dumps(data))
    return {'status_code' : response.status_code, 'text' : response.text}

  def delete_subscribe_C2C_notifications(self,plantId,subscriptionId):
    self.refresh_token_if_needed()
    url = ("https://api.developer.legrand.com/smarther/v2.0/plants/" + plantId + "/subscription/" + subscriptionId)
    response = requests.request("DELETE", url, headers=self.header, data={})
    return {'status_code' : response.status_code, 'text' : response.text}
