import hlt
import argparse
import logging
from rnn import RecurrentNeuralNet


def create_feature_list(entity, me):
    out = [entity.x, entity.y, entity.radius, entity.health]

    if entity.owner == me:
        out += [1, 0, 0]
    elif entity.owner is None:
        out += [0, 1, 0]
    else:
        out += [0, 0, 1]

    return out


class Bot:
    def __init__(self, name='bot'):
        self.game = hlt.Game(name)
        self.brain = RecurrentNeuralNet()

    def play(self):
        while True:
            game_map = self.game.update_map()
            logging.info(game_map)
            command_queue = []

            planets = game_map.all_planets()
            me = game_map.get_me()
            my_ships = me.all_ships()
            enemy_ships = []
            for player in game_map.all_players():
                if player != me:
                    enemy_ships += player.all_ships()

            for ship in my_ships:
                feature_list = create_feature_list(ship, me)

                if ship.docking_status != ship.DockingStatus.UNDOCKED:
                    continue

                for planet in game_map.all_planets():
                    if planet.is_owned():
                        continue

                    if ship.can_dock(planet):
                        command_queue.append(ship.dock(planet))
                    else:
                        navigate_command = ship.navigate(
                            ship.closest_point_to(planet),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED/2),
                            ignore_ships=True)
                        if navigate_command:
                            command_queue.append(navigate_command)
                    break

            self.game.send_command_queue(command_queue)


parser = argparse.ArgumentParser()
parser.add_argument("--name", help="Bot name", default="bot")
args = parser.parse_args()
Bot(args.name).play()
