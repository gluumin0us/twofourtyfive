import random

def generate_timeline() -> list[list]:
    exhibits = ["lobby", "ex1", "ex2", "security", "ex3", "ex4", "artifact"]
    timeline = []
    random.shuffle(exhibits)
    for i in range(len(exhibits)):
        timeline.append([exhibits[i], exhibits[(i+1) % 7]])
    for i in range(7):
        connection = random.sample(exhibits, 2)
        while connection in timeline:
            connection = random.sample(exhibits, 2)
        timeline.append(connection)
    return timeline

def generate_museum() -> list:
    exhibits = ["dino", "cosmos", "inventions", "conflict", "gems", "canvas", "silk", "floral", "faith"]
    museum = random.sample(exhibits, 4)
    return museum

def find_next(timeline: list[list], current_time) -> list:
    next_time = []
    for connection in timeline:
        if connection[0] == current_time:
            next_time.append(connection[1])
    return next_time
