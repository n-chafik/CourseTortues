import datetime
import json
import requests
import time
from datetime import datetime

stop = False
n = 1
url = "http://tortues.ecoquery.os.univ-lyon1.fr/race/"
type_of_race = "large"
while not stop:
    time.sleep(3)
    # get information from cluster
    response = requests.get(url+type_of_race)
    data = response.json()

    # Serializing json
    json_object = json.dumps(data, indent=4)

    # Archiving information
    file_name = "archive" + str(n) + ".json"
    with open(type_of_race+"/"+file_name, "w") as outfile:
        outfile.write(json_object)
    print("Archiving in file ", n, " ", datetime.now())

    n = n + 1
    if n == 150:
        stop = True
