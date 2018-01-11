import argparse
import json

import hlt
import operator
import logging
from rnn.rnn import DeepRecurrentNeuralNet


class Bot:
    def __init__(self, name='bot', structure=None):
        self.game = hlt.Game(name)
        self.brain = DeepRecurrentNeuralNet(structure)

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
                    for feature_list in self.sorted_feature_matrix_by_distance(game_map, ship):
                        result = self.brain.step(feature_list)

                    speed = int(abs(result[0]) * hlt.constants.MAX_SPEED)
                    angle = int(round(abs(result[1]) * 360))
                    ship_command = ship.thrust(speed, angle)

                logging.info(ship_command)
                command_queue.append(ship_command)

            self.game.send_command_queue(command_queue)

    def sorted_feature_matrix_by_distance(self, game_map, ship):
        features = [self.create_feature_list(ship, ship.owner)]
        distances = game_map.nearby_entities_by_distance(ship)
        sorted_distances = sorted(distances.items(), key=operator.itemgetter(0))

        for distance, entities in sorted_distances:
            for entity in entities:
                features.append(self.create_feature_list(entity, ship.owner))
        return features

    @staticmethod
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--uuid", help="Bot uuid which should correspond to a saved structure file")
    args = parser.parse_args()

    try:
        with open('../temp/' + args.uuid + '.bot') as file:
            name = args.uuid
            structure = json.loads(file.read())
    except Exception:
        name = 'RandomBot'
        structure = None

    Bot(name, structure).play()
