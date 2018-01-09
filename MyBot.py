import math

import hlt
import argparse
import operator
import logging
from rnn.rnn import RecurrentNeuralNet


def create_feature_list(entity, me):
    out = [entity.x, entity.y, entity.radius, entity.health]

    if entity.owner == me:
        out += [1, 0]
    elif entity.owner is None:
        out += [0, 0]
    else:
        out += [0, 1]

    if isinstance(entity,  hlt.entity.Planet):
        out += [1, 0]
    elif isinstance(entity,  hlt.entity.Ship):
        out += [0, 1]
    else:
        out += [0, 0]

    return out


def sorted_feature_matrix_by_distance(game_map, ship):
    features = [create_feature_list(ship, ship.owner)]
    distances = game_map.nearby_entities_by_distance(ship)
    sorted_distances = sorted(distances.items(), key=operator.itemgetter(0))

    for distance, entities in sorted_distances:
        for entity in entities:
            features.append(create_feature_list(entity, ship.owner))
    return features


class Bot:
    def __init__(self, name='bot'):
        self.game = hlt.Game(name)
        self.brain = RecurrentNeuralNet()

    def play(self):
        while True:
            game_map = self.game.update_map()
            command_queue = []

            for ship in game_map.get_me().all_ships():
                ship_command = False
                if ship.docking_status != ship.DockingStatus.UNDOCKED:
                    continue

                for planet in game_map.all_planets():
                    if planet.is_owned():
                        continue

                    if ship.can_dock(planet):
                        ship_command = ship.dock(planet)
                        break

                if not ship_command:
                    self.brain.reset()
                    result = [0, 0]
                    for feature_list in sorted_feature_matrix_by_distance(game_map, ship):
                        result = self.brain.step(feature_list)
                        logging.info(result)

                    angle = int(math.degrees(result[1]) % 360)
                    ship_command = ship.thrust(abs(result[0]), angle)

                logging.info(ship_command)
                command_queue.append(ship_command)

            self.game.send_command_queue(command_queue)


parser = argparse.ArgumentParser()
parser.add_argument("--name", help="Bot name", default="bot")
args = parser.parse_args()
Bot(args.name).play()
