import json
import os
import os.path
import matplotlib.pyplot as plt


# Function that returns the speeds recorded between every two Tops
def table_speed(id_tortoise, type_of_race="tiny"):
    list_positions = []
    list_speeds = []
    list_temperature = []
    list_quality = []
    # Count the number of archives we made
    number_of_files = len(
        [name for name in os.listdir('./raw_data/' + type_of_race)])
    # This loop go into all the files, extract the positions of a given tortoise
    for i in range(10000, number_of_files):
        file_name = "archive" + str(i + 1) + ".json"
        with open('./raw_data/' + type_of_race + "/" + file_name, 'r') as f:
            data = json.load(f)
            list_quality.append(data["qualite"])
            list_temperature.append(data["temperature"])
            for tortoise in data['tortoises']:
                if tortoise['id'] == id_tortoise:
                    # Get the position of this tortoise from each file ( every 1 top )
                    list_positions.append(tortoise['position'])

            f.close()

    for i in range(len(list_positions) - 1):
        # calculate the speeds recorded from the positions
        list_speeds.append(list_positions[i + 1] - list_positions[i])

    return list_speeds, list_quality, list_temperature


def plot_tortoise(id_tortoise, type_of_race):
    (speed, quality, temperatures) = table_speed(id_tortoise, type_of_race)

    quality = [x * 100 for x in quality]

    plt.plot(speed, label="Vitesse")
    plt.plot(quality, label="Qualité (en %)")
    plt.plot(temperatures, label="Température")
    plt.title('Tortoise {} in the {} race ({} measures)'.format(id_tortoise, type_of_race, len(speed)))
    plt.xlabel('Temps')
    plt.ylabel('Vitesse')
    plt.legend(loc="upper left")
    plt.figure(figsize=(30, 15), dpi=300)

    plt.show()


def is_regular(speed):
    if max(speed) == min(speed):
        return True, {"step": speed[0]}
    else:
        return False, {}


def is_cyclic(speed):
    first_element = speed[0]
    window = [first_element]
    position = None
    for i in range(0, len(speed) - 1):
        if speed[i + 1] != first_element:
            window.append(speed[i + 1])
        else:
            position = i + 1
            break

    if position == 1 or position is None:
        return False, {}
    else:
        for j in range(1, position - 1):
            try:
                if speed[j] != speed[j + position]:
                    return False, {}
            except:
                return True, {"window": window}

        return True, {"window": window}


def is_tired(speed):
    table_accelerations = []
    if speed[0] != speed[1]:
        for i in range(len(speed) - 1):
            table_accelerations.append(abs(speed[i + 1] - speed[i]))

        size = len(list(set(table_accelerations)))
        if size == 2 or size == 1:
            return True, {"initial": max(speed), "rhythm": table_accelerations[0]}
        else:
            return False, {}
    else:
        return False, {}


def is_lunatic(speed, temperature, quality):
    current_temp = temperature[0]
    current_quality = quality[0]
    intervals = []
    # We calculate each intervals of (temperature, quality)
    for i in range(len(temperature)):
        if current_quality != quality[i] or current_temp != temperature[i]:
            intervals.append(i)
            current_quality = quality[i]
            current_temp = temperature[i]

    params = {
        "comportment": {
        },
        "intervals": [],
    }

    for i in range(len(intervals[:-1])):
        (is_regular_bool, regular_params) = is_regular(speed[intervals[i]:intervals[i+1]])
        if is_regular_bool:
            params["comportment"][1] = regular_params
            params["intervals"].append({"class": 1, "temperature": temperature[intervals[i+1]], "quality": quality[intervals[i+1]]})

        else:
            (is_tired_bool, tired_params) = is_tired(speed[intervals[i]:intervals[i+1]])
            if is_tired_bool:
                params["comportment"][2] = tired_params
                params["intervals"].append({"class": 2, "temperature": temperature[intervals[i+1]], "quality": quality[intervals[i+1]]})

            else:
                (is_cyclic_bool, cyclic_params) = is_cyclic(speed[intervals[i]:intervals[i+1]])
                if is_cyclic_bool:
                    params["comportment"][3] = cyclic_params
                    params["intervals"].append({"class": 3, "temperature": temperature[intervals[i+1]], "quality": quality[intervals[i+1]]})

    return True, params


def model():
    print("start making the model")
    data_model = {"large": [], "tiny": [], "small": [], "medium": []}
    length = {"large": 2000, "medium": 500, "small": 100, "tiny": 10}
    for Type in ["tiny", "small", "medium", "large"]:
        print("Type of race", Type)
        for tortoise in range(length[Type]):
            print("Tortoise : ", tortoise)
            (speed, quality, temperature) = table_speed(tortoise, Type)
            (is_regular_bool, params) = is_regular(speed)

            if is_regular_bool:
                data_model[Type].append({"Tortoise": tortoise, "class": 0, "params": params})

            else:
                (is_tired_bool, params) = is_tired(speed)
                if is_tired_bool:
                    data_model[Type].append({"Tortoise": tortoise, "class": 1, "params": params})

                else:
                    (is_cyclic_bool, params) = is_cyclic(speed)
                    if is_cyclic_bool:
                        data_model[Type].append({"Tortoise": tortoise, "class": 2, "params": params})
                        (is_lunatic_bool, params) = is_lunatic(tortoise, Type)

                    else:
                        # if is_lunatic_bool:
                        data_model[Type].append({"Tortoise": tortoise, "class": 3, "params": params})

    with open('./model.json', 'w') as f:
        f.write(json.dumps(data_model, indent=2))


if __name__ == "__main__":
    model()
