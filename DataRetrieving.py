import datetime
import json
import requests
import time
from datetime import datetime

stop = False
url = "http://tortues.ecoquery.os.univ-lyon1.fr/race/"


def retrieving_infos(n):
    previous_data = {
        "large": [],
        "medium": [],
        "small": [],
        "tiny": [],
    }

    i = 1
    while i <= n:
        try:
            for type_of_race in ['tiny', 'large', 'medium', 'small']:
                # get information from cluster
                response = requests.get(url + type_of_race)
                data = response.json()

                # Check if we have downloaded the same data than the previous tick
                if previous_data[type_of_race] != data:
                    # Serializing json
                    json_object = json.dumps(data, indent=4)

                    # Archiving information
                    file_name = "archive" + str(i) + ".json"
                    with open("./raw_data/" + type_of_race + "/" + file_name, "w") as outfile:
                        outfile.write(json_object)
                        previous_data[type_of_race] = data
                    print("Archiving in file ", i, " ", datetime.now())
                else:
                    print("File already downloaded")
                    i -= 1
                    break
            i += 1
            time.sleep(1)
            # This sleep time depends of the internet connection and the computer.
            # On slow computer reduce it.
        except Exception as e:
            print("An error have occured : ", e)


if __name__ == "__main__":
    retrieving_infos(24 * 20 * 60)
