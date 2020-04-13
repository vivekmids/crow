import logging
import numpy as np
import os
import time
import base64


def _is_day():
    localtime = time.localtime().tm_hour
    return localtime < 20 and localtime > 6


class DeterrentManager(object):
    def __init__(self):
        self.predator_map = {'skunk': ['dog', 'human', 'coyote'],
                             'rodent': ['dog', 'human', 'coyote', 'cat'],
                             'squirrel': ['dog', 'human', 'coyote', 'cat'],
                             'rabbit': ['dog', 'human', 'coyote', 'hawk'],
                             'bird': ['dog', 'human', 'coyote', 'gun', 'hawk'],
                             'deer': ['human', 'coyote', 'cheetah', 'cougar', 'bobcat', 'leopard', 'tiger'],
                             'raccoon': ['dog', 'human', 'coyote'],
                             'opossum': ['dog', 'human', 'coyote', 'gun', 'hawk']}

        self.predator_sound_map = {}
        for pest, predators in self.predator_map.items():
            for predator in predators:
                self.predator_sound_map[predator] = []
                try:
                    path = os.path.join(
                        os.path.dirname(os.path.dirname(__file__)),
                        "deterrent-service",
                        "sound",
                        predator)
                    sound_files = os.listdir(path)

                    self.predator_sound_map[predator] = [
                        os.path.join(path, sound_file)
                        for sound_file in sound_files
                    ]
                except Exception as e:
                    logging.error("Sound files for %s in folder %s not found", pest, predator)
                    raise e

    def deploy_deterrent(self, detected_animal):
        """Here we deploy a deterrent"""
        if _is_day():
            predator = np.random.choice(self.predator_map[detected_animal])
            played_sound = np.random.choice(self.predator_sound_map[predator])
            return {
                'type': 'sound',
                'played_sound': played_sound
            }
        else:
            return {
                'type': 'light',
            }

    def get_sound_to_play(self, sound_file):
        with open(sound_file, 'rb'):
            return base64.b64encode(sound_file.read())
