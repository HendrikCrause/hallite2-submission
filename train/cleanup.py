import os


def cleanup_temp_folder(survivors=()):
    folder = 'temp/'
    survivor_files = [s + '.bot' for s in survivors]
    for the_file in os.listdir(folder):
        if the_file in survivor_files:
            continue

        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def cleanup_games_folder():
    folder = 'games/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def cleanup_logs():
    folder = '.'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path) and file_path.endswith('.log'):
                os.unlink(file_path)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    cleanup_games_folder()
    cleanup_temp_folder()
    cleanup_logs()
