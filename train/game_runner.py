import argparse
import json
import os
import subprocess
import zstd


def run_halite_game(bots):
    if len(bots) == 0:
        return {}

    command = [
        './halite',
        '-q'
    ]

    for bot in bots:
        command.append('"python3 MyBot.py --name {}"'.format(bot))

    run = subprocess.run(' '.join(command), stdout=subprocess.PIPE, shell=True)
    return json.loads(run.stdout.decode())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--bots", help="Json object describing bot1 parameters", nargs='*')
    args = parser.parse_args()

    bots = args.bots if args.bots is not None else ['bot1', 'bot2']

    if len(bots) not in [2, 4]:
        raise Exception('Only accepting 2 or 4 bots, not {}'.format(len(bots)))

    result = run_halite_game(bots)

    ranks = dict([(bots[idx], result['stats'][str(idx)]['rank']) for idx in range(len(bots))])
    print(ranks)

    with open(result['replay'], 'rb') as replay:
        raw_replay_data = zstd.loads(replay.read())

    os.remove(result['replay'])
    replay_data = json.loads(raw_replay_data.decode())

    with open('./games/test_replay.json', 'w') as output:
        output.write(json.dumps(replay_data))

