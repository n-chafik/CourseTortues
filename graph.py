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


if __name__ == "__main__":
    plot_tortoise(7, "small")


