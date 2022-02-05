import json
import os
import os.path


# Function that returns the speeds recorded between every two Tops

def table_speed(id_tortoise, type_of_race):
    list_positions = []
    list_speeds = []
    # Count the number of archives we made
    number_of_files = len(
        [name for name in os.listdir('./' + type_of_race)])
    # This loop go into all the files, extract the positions of a given tortoise
    for i in range(number_of_files):
        file_name = "archive" + str(i + 1) + ".json"
        with open(type_of_race + "/" + file_name, 'r') as f:
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


def is_regular(id_tortoise):
    speed = table_speed(id_tortoise)
    pas = speed[0]
    i = 1
    while i < len(speed):
        if speed[i] != pas:
            print(speed[i], pas)
            return False
        i = i + 1

    return True


def is_cyclic(id_tortoise, type_of_race):
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


for i in range(1000, 1500):
    if isinstance(is_cyclic(i, "large"), list):
        print("Id tortoise : ", i)
        print("speed : ", table_speed(i, "large"))
        print("cycle  : ", is_cyclic(i, "large"))
