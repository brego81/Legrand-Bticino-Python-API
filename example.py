from LegrandBiticinoAPI import LegrandBiticinoAPI
import pprint as pp
import datetime

API = LegrandBiticinoAPI()

# Test the API using and echo endpoint as per documentation
# https://portal.developer.legrand.com/docs/services/echo-api/operations/create-resource
out = API.echo()
if out['status_code'] == 200:
    print("It works fine!")
else:
    raise SystemExit("ERROR: " + str(out['status_code']))

# Plants - Operation used to retrieve all the plants associated to a user.
# https://portal.developer.legrand.com/docs/services/smartherV2/operations/Plants
plants = API.get_plants()
plantId = plants['text']['plants'][0]['id']
print("plantId = " + str(plantId))

# Topology - Operation used to retrieve the complete topology of a plant.
# https://portal.developer.legrand.com/docs/services/smartherV2/operations/Topology
modules = API.get_topology(plantId)
moduleId = modules['text']['plant']['modules'][0]['id']
print("moduleId = " + str(moduleId))

# Chronothermostat Measures - Operation used to retrieve the measured temperature and humidity detected by a chronothermostat.
# https://portal.developer.legrand.com/docs/services/smartherV2/operations/Chronothermostat-Measures
out = API.get_chronothermostat_measures(plantId, moduleId)
if out['status_code'] == 200:
    print('Chronothermostat measures = ')
    pp.pprint(out['text'])
else:
    raise SystemExit("ERROR -> " + str(out))

# Chronothermostat ProgramList - Operation used to retrieve the list of programs managed by a chronothermostat.
# https://portal.developer.legrand.com/docs/services/smartherV2/operations/Chronothermostat-ProgramList
out = API.get_chronothermostat_programlist(plantId, moduleId)
if out['status_code'] == 200:
    print('Chronothermostat programlist = ')
    pp.pprint(out['text'])
else:
    raise SystemExit("ERROR -> " + str(out))

# Get Chronothermostat Status - Operation used to retrieve the complete status of a chronothermostat.
# https://portal.developer.legrand.com/docs/services/smartherV2/operations/Get-Chronothermostat-Status
status = API.get_chronothermostat_status(plantId, moduleId)
if out['status_code'] == 200:
    print('Chronothermostat status = ')
    pp.pprint(status['text'])
else:
    raise SystemExit("ERROR -> " + str(status))

# As example, we want to set to AUTOMATIC if a temeprature is manually defined 
if status['text']['chronothermostats'][0]['mode'] != 'AUTOMATIC':
  print("setPoint = " + status['chronothermostats'][0]['setPoint']['value'] + "\n")
  data = {
          "function": "heating", "mode": "AUTOMATIC",
          "setPoint": { "value": "18.20000", "unit": "C" },
          "programs": [ { "number": 1 }],
          "activationTime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }
  # Set Chronothermostat Status - Operation used to set the status of a chronothermostat.
  # https://portal.developer.legrand.com/docs/services/smartherV2/operations/Set-Chronothermostat-Status
  out = API.set_chronothermostat_status(plantId, moduleId, data)
  print(str(out)  + "\n")

# Get subscriptions to C2C notifications - Operation used to get subscriptions of a user to get Cloud2Cloud notifications of a plant.
# https://portal.developer.legrand.com/docs/services/smartherV2/operations/Get-subscriptions-to-C2C-notifications
subscriptions = API.get_subscriptions_C2C_notifications()
if subscriptions['status_code'] == 204:
    print("No subscription associated with this user")
elif subscriptions['status_code'] == 200:
     pp.pprint(subscriptions['text'])

# Subscribe to C2C notifications - Operation used to subscribe a user to get Cloud2Cloud notifications of a plant.
# https://portal.developer.legrand.com/docs/services/smartherV2/operations/Subscribe-to-C2C-notifications
data = {"EndPointUrl": "http://www.example.com"}
out = API.set_subscribe_C2C_notifications(plantId, data)
print(str(out['status_code']) + "  " + out['text'])

# Delete subscription to C2C notifications - Operation used to delete the subscription of a user to get Cloud2Cloud notifications of a plant.
# https://portal.developer.legrand.com/docs/services/smartherV2/operations/Delete-subscription-to-C2C-notifications
subscriptionId = '123'
out = API.delete_subscribe_C2C_notifications(plantId, subscriptionId)
print(str(out['status_code']) + "  " + out['text'])