import json


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
        return


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
    if initial % rhythm == 0:
        for i in range(initial / rhythm):
            speeds.append(rhythm * (i+1))
        for i in range(initial/rhythm, 1, -1):
            speeds.append(rhythm * (i-1))
    else:
        for i in range(int(initial / rhythm)):
            speeds.append(rhythm * (i+1))
        speeds.append(initial)
        for i in range(1, (int(initial/rhythm))+1):
            speeds.append(initial - (rhythm*i))

    accelerations = []
    current_speed = 0
    for i in range(len(speeds)):
        if speeds[i] == pos2 - pos1:
            current_speed = i
            break

    for i in range(delta_top):
        accelerations.append(speeds[(current_speed + i) % len(speeds)])

    return pos1 + sum(accelerations)








    return


def prediction_lunatic():
    return


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


# print(prediction("tiny", 0, 848157, 71245188, 71245272, 71245356, 24.174806498112467, 0.3100529516794682, 90293))
# print(prediction("tiny", 3, 848157, 181263227, 181263510, 181263603, 0.3100529516794682, 24.174806498112467, 92670))
# print(prediction("large", 12, 847861, 160245918, 160246266, 160246584, 20.980595977843635, 0.863381793014835, 123169))
