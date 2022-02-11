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
    pas = speed[0]
    i = 1
    while i < len(speed):
        if speed[i] != pas:
            print(speed[i], pas)
            return False
        i = i + 1

    return True


def is_cyclic(id_tortoise, type_of_race="tiny"):
    speed = table_speed(id_tortoise, type_of_race)
    # speed = [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7]
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
        return "pas de cycles"
    else:
        for j in range(1, position - 1):
            try:

                if speed[j] != speed[j + position]:
                    return "pas de cycles"
            except:
                return "Maybe Cyclic"

        return window


def is_tired(id_tortoise, type_of_race="tiny"):

    if not is_regular(id_tortoise, type_of_race):

        speeds = table_speed(id_tortoise, type_of_race)
        table_accelerations = []
        for i in range(len(speeds) - 1):
            table_accelerations.append(abs(speeds[i + 1] - speeds[i]))

        size = len(list(set(table_accelerations)))
        if size == 2 or size == 1:
            return 'Tortoise  Tired,  initial : ', max(speeds), '  rhythm  :  ', \
                   table_accelerations[0]
        else:
            return False

if __name__ == "__main__":
    # print(table_speed(10, "medium"))
    # print(is_cyclic(10, "medium"))
    # print(is_tired(1, "tiny"))
    plot_tortoise(9, 'tiny')
    # print(is_regular(10, "medium"))
