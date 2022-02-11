import datetime
import json
import requests
import time
from datetime import datetime
import os
import matplotlib.pyplot as plt
import numpy as np

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
            time.sleep(2)
            # This sleep time depends of the internet connection and the computer.
            # On slow computer reduce it.
        except Exception as e:
            print("An error have occured : ", e)


def group_data_by_id():
    nb_tortues = {
        "large": 2000,
        "medium": 500,
        "small": 100,
        "tiny": 10,
    }
    print("=== Creating a file per tortoise ===")
    for type_of_race in ['large', 'medium', 'small', 'tiny']:
        print(" * Starting with the {} race".format(type_of_race))
        for tortue in range(nb_tortues[type_of_race]):
            files = os.listdir('./raw_data/' + type_of_race)
            data = []
            for index_file in range(1, len(files)):
                file = './raw_data/{}/archive{}.json'.format(type_of_race, str(index_file))
                with open(file, 'r') as f:
                    file_data = json.load(f)
                    data.append({
                        "top": file_data["tortoises"][tortue]["top"],
                        "position": file_data["tortoises"][tortue]['position'],
                        "qualite": file_data["qualite"],
                        "temperature": file_data["temperature"],
                    })
            file = './data_by_id/{}/tortoise{}.json'.format(type_of_race, str(tortue))
            with open(file, 'w') as f:
                f.write(json.dumps(data))
                print("   - Tortoise file {} written".format(file))


def plot_tortoise(type_of_race, id):
    file = './data_by_id/{}/tortoise{}.json'.format(type_of_race, str(id))
    with open(file, 'r') as f:
        data = json.load(f)

    top = np.empty(len(data))
    position = np.empty(len(data))
    for i, step in enumerate(data):
        top[i] = step["top"]
        position[i] = step["position"]

    plt.plot(top, position)
    plt.title('Tortoise {} in the {} race ({} measures)'.format(id, type_of_race, len(top)))
    plt.xlabel('Distance')
    plt.ylabel('Time')
    plt.show()


def detect_tortoise(type_of_race, id):
    file = './data_by_id/{}/tortoise{}.json'.format(type_of_race, str(id))
    with open(file, 'r') as f:
        data = json.load(f)

    top = np.empty(len(data))
    position = np.empty(len(data))
    for i, step in enumerate(data):
        top[i] = step["top"]
        position[i] = step["position"]

    speed = (np.roll(position, -1) - position)[:-1]

    (is_regular_bool, params) = is_regular(speed)
    if is_regular_bool:
        print('Regular tortoise with average speed of {}'.format(params))
        return
    (is_tired_bool, params) = is_tired(speed)
    if is_tired_bool:
        print('Regular tortoise with average speed of {}'.format(params))
        return


def is_regular(speed):
    if np.min(speed) == np.max(speed):
        return True, speed[0]
    else:
        return False, 0


def is_tired(speed):
    acceleration = (np.roll(speed, -1) - speed)[:-1]
    print(acceleration)
    if - np.min(acceleration) == np.max(acceleration) and np.all(acceleration):
        return True, {"initial": np.max(speed), "rythm": acceleration[0]}
    else:
        return False, {}


if __name__ == "__main__":
    # retrieving_infos(50)
    # group_data_by_id()
    plot_tortoise('tiny', 7)
    detect_tortoise('tiny', 7)
