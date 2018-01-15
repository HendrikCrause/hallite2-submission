import argparse
import json
import os
import glob
import subprocess
import zstd


def run_halite_game(bots=(), cleanup=False):
    if len(bots) == 0:
        return {}

    command = [
        './halite',
        '-q'
    ]

    for bot in bots:
        command.append('"python3 bots/bot.py --uuid {}"'.format(bot))

    run = subprocess.run(' '.join(command), stdout=subprocess.PIPE, shell=True)
    result = json.loads(run.stdout.decode())

    if cleanup:
        os.remove(result['replay'])
        for file in glob.glob(r'./*.log'):
            os.remove(file)
    else:
        os.rename(result['replay'], './games' + result['replay'][1:])
        for file in glob.glob(r'./*.log'):
            os.rename(file, './logs' + file[1:])

    return result


def determine_ranks(result, bots):
    return dict([(result['stats'][str(idx)]['rank'], bots[idx]) for idx in range(len(bots))])


def uncompress_replay(filename):
    with open(filename, 'rb') as replay:
        raw_replay_data = zstd.loads(replay.read())

    replay_data = json.loads(raw_replay_data.decode())

    with open(filename + '.json', 'w') as output:
        output.write(json.dumps(replay_data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--bots", help="Json object describing bot1 parameters", nargs='*')
    parser.add_argument("--save-replay", help="Don't delete replay file")
    args = parser.parse_args()

    bots = args.bots if args.bots is not None else ['bot1', 'bot2']

    if len(bots) not in [2, 4]:
        raise Exception('Only accepting 2 or 4 bots, not {}'.format(len(bots)))

    result = run_halite_game(bots)
    print(result)
    print(determine_ranks(result, bots))
