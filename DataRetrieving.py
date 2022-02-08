import datetime
import json
import requests
import time
from datetime import datetime

stop = False
n = 30
url = "http://tortues.ecoquery.os.univ-lyon1.fr/race/"


def retrieving_infos(n):
    previous_data = {
        "large": [],
        "medium": [],
        "small": [],
        "tiny": [],
    }

    for loop in range(1, n):
        try:
            for type_of_race in ['large', 'medium', 'small', 'tiny']:
                # get information from cluster
                response = requests.get(url + type_of_race)
                data = response.json()

                # Check if we have downloaded the same data than the previous tick
                if previous_data[type_of_race] != data:
                    # Serializing json
                    json_object = json.dumps(data, indent=4)

                    # Archiving information
                    file_name = "archive" + str(loop) + ".json"
                    with open("./raw_data/" + type_of_race + "/" + file_name, "w") as outfile:
                        outfile.write(json_object)
                        previous_data[type_of_race] = data
                    print("Archiving in file ", loop, " ", datetime.now())
                else:
                    print("File already downloaded")
                    break

            time.sleep(2.5)
        except Exception as e:
            print("An error have occured : ", e)


def group_data_by_id():
    pass

