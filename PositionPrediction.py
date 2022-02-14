import json
import argparse


def prediction2(Type, top, pos1, pos2, pos3, temp, quality, delta_top, parameters):
    if Type == 0:
        speed = parameters["step"]
        return prediction_regular(pos1, delta_top, speed)
    if Type == 1:
        initial = parameters["initial"]
        rhythm = parameters["rhythm"]
        return prediction_tired(initial, rhythm, pos1, pos2, pos3, delta_top)
    if Type == 2:
        window = parameters["window"]
        return prediction_cyclic(window, pos1, pos2, pos3, delta_top)
    if Type == 3:
        return prediction_lunatic(pos1, pos2, pos3, temp, quality, delta_top, parameters)


def prediction_regular(pos1, delta_top, speed):
    return pos1 + speed * delta_top


def prediction_cyclic(window, pos1, pos2, pos3, delta_top):
    speeds = []
    current_speed = 0
    for i in range(len(window)):
        if window[i] == pos2 - pos1:
            current_speed = i
            break

    for i in range(delta_top):
        speeds.append(window[(current_speed + i) % len(window)])

    return pos1 + sum(speeds)


def prediction_tired(initial, rhythm, pos1, pos2, pos3, delta_top):
    speeds = [0]
    if initial % rhythm > 0:
        #for i in range(initial / rhythm):
        #    speeds.append((i + 1) * rhythm)

        for i in range(initial):
            speeds.append(rhythm)
        # A complèter


    return


def prediction_lunatic(pos1, pos2, pos3, temp, quality, delta_top, parameters):
    # We use a classic measure distance
    def quadratic_distance(temperature_a, quality_a, temperature_b, quality_b):
        return (temperature_a - temperature_b) ** 2 + (quality_a - quality_b) ** 2

    # We compute each distances to calcul after nearest neighbors
    def distances_vector(dataset, temperature_input, quality_input):
        distances = []
        for j in range(len(dataset)):
            temp = dataset[j]["temperature"]
            qual = dataset[j]["quality"]
            distances.append(quadratic_distance(temp, qual, temperature_input, quality_input))
        return distances

    distances = distances_vector(parameters["intervals"], temp, quality)

    # Because we don't have a lot of data, we implement the KNN with K = 1
    min_distance = 10e10
    comportment = 0
    for i in range(len(distances)):
        if distances[i] <= min_distance:
            min_distance = distances[i]
            # Here we determined the exact comportment of the tortoise
            comportment = parameters["intervals"]["class"][i]

    return prediction2(comportment, pos1, pos2, pos3, temp, quality, delta_top, parameters["comportment"][comportment])


def prediction(course, id, top, pos1, pos2, pos3, temp, quality, delta_top):
    # read the model file
    with open("model.json", 'r') as f:
        knowledge = json.load(f)
        # loop over the file to find the wanted Type
        for Type in knowledge:
            if Type == course:
                # loop into this type and find the tortoise that we want to predict
                for Tortoise in knowledge[Type]:
                    if id == Tortoise["Tortoise"]:
                        Type = Tortoise["class"]
                        parameters = Tortoise["params"]
                        return prediction2(Type, top, pos1, pos2, pos3, temp, quality, delta_top, parameters)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate tortoise postion based on provided data')
    parser.add_argument(
        'course',
        type=str,
        choices=['tiny', 'small', 'medium', 'large'],
        help='Type of course'
    )
    parser.add_argument('id', type=int, help='Id of the tortoise')
    parser.add_argument('top', type=int, help='Current top')
    parser.add_argument('pos1', type=int, help='First position')
    parser.add_argument('pos2', type=int, help='Second position')
    parser.add_argument('pos3', type=int, help='Third position')
    parser.add_argument('temp', type=float, help='Temperature')
    parser.add_argument('qual', type=float, help='Quality of the food')
    parser.add_argument('deltatop', type=int, help='Delta top')

    args = vars(parser.parse_args())

    print(prediction(args['course'], args['id'], args['top'], args['pos1'], args['pos2'], args['pos3'], args['temp'], args['qual'], args['deltatop']))

    # Example command :
    # python PositionPrediction.py "tiny" 3 848157 181263227 181263510 181263603 0.3100529516794682 24.174806498112467 92670