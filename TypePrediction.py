import json
import os
import os.path
import matplotlib.pyplot as plt


# Function that returns the speeds recorded between every two Tops

def table_speed(id_tortoise, type_of_race="tiny"):
    list_positions = []
    list_speeds = []
    # Count the number of archives we made
    number_of_files = len(
        [name for name in os.listdir('./raw_data/' + type_of_race)])
    # This loop go into all the files, extract the positions of a given tortoise
    for i in range(number_of_files):
        file_name = "archive" + str(i + 1) + ".json"
        with open('./raw_data/' + type_of_race + "/" + file_name, 'r') as f:
            data = json.load(f)
            for tortoise in data['tortoises']:
                if tortoise['id'] == id_tortoise:
                    # Get the position of this tortoise from each file ( every 1 top )
                    list_positions.append(tortoise['position'])
            f.close()

    for i in range(len(list_positions) - 1):
        # calculate the speeds recorded from the positions
        list_speeds.append(list_positions[i + 1] - list_positions[i])

    return list_speeds


def plot_tortoise(id_tortoise, type_of_race):
    speed = table_speed(id_tortoise, type_of_race)

    plt.plot(speed)
    plt.title('Tortoise {} in the {} race ({} measures)'.format(id_tortoise, type_of_race, len(speed)))
    plt.xlabel('Distance')
    plt.ylabel('Time')
    plt.show()


def is_regular(id_tortoise, type_of_race="tiny"):
    speed = table_speed(id_tortoise, type_of_race)
    if max(speed) == min(speed):
        return True, {"step": speed[0]}
    else:
        return False, {}


def is_cyclic(id_tortoise, type_of_race="tiny"):
    speed = table_speed(id_tortoise, type_of_race)
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


def is_tired(id_tortoise, type_of_race="tiny"):
    speeds = table_speed(id_tortoise, type_of_race)
    table_accelerations = []
    if speeds[0] != speeds[1]:
        for i in range(len(speeds) - 1):
            table_accelerations.append(abs(speeds[i + 1] - speeds[i]))

        size = len(list(set(table_accelerations)))
        if size == 2 or size == 1:
            return True, {"initial": max(speeds), "rhythm": table_accelerations[0]}
        else:
            return False, {}
    else:
        return False, {}


def is_lunatic(id_tortoise, type_of_race="tiny"):
    return True, {}


def model():
    print("start making the model")
    data_model = {"large": [], "tiny": [], "small": [], "medium": []}
    length = {"large": 2000, "medium": 500, "small": 100, "tiny": 10}
    for Type in ["tiny", "small", "medium", "large"]:
        print("Type of race", Type)
        for tortoise in range(length[Type]):
            print("Tortoise : ", tortoise)
            (is_regular_bool, params) = is_regular(tortoise, Type)

            if is_regular_bool:
                data_model[Type].append({"Tortoise": tortoise, "class": 0, "params": params})

            else:
                (is_tired_bool, params) = is_tired(tortoise, Type)
                if is_tired_bool:
                    data_model[Type].append({"Tortoise": tortoise, "class": 1, "params": params})

                else:
                    (is_cyclic_bool, params) = is_cyclic(tortoise, Type)
                    if is_cyclic_bool:
                        data_model[Type].append({"Tortoise": tortoise, "class": 2, "params": params})
                        (is_lunatic_bool, params) = is_lunatic(tortoise, Type)

                    else:
                        if is_lunatic_bool:
                            data_model[Type].append({"Tortoise": tortoise, "class": 3, "params": params})

    with open('./model.json', 'w') as f:
        f.write(json.dumps(data_model, indent=4))


if __name__ == "__main__":
    # print(table_speed(10, "medium"))
    # print(is_cyclic(10, "medium"))
    # print(is_tired(1, "tiny"))
    # plot_tortoise(9, 'tiny')
    # print(is_regular(10, "medium"))

    #model()
    print(table_speed(0,"large"))
    print(is_cyclic(0, "large"))

