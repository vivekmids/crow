import logging
import numpy as np
import os
import RPi.GPIO as gpio
import time


def _is_day():
    localtime = time.localtime().tm_hour
    return localtime<20 and localtime>6


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
                    path = os.path.join(os.path.dirname(__file__), "sound", predator)
                    sound_files = os.listdir(path)

                    self.predator_sound_map[predator] = [
                        os.path.join(path, sound_file)
                        for sound_file in sound_files
                    ]
                except Exception as e:
                    logging.error("Sound files for %s in folder %s not found", pest, predator)
                    raise e
                    
        gpio.setmode(gpio.BOARD)
        gpio.setup(11, gpio.OUT)

    def deploy_deterrent(self, detected_animal):
        """Here we deploy a deterrent"""
        if _is_day():
            predator = np.random.choice(self.predator_map[detected_animal])
            played_sound = self.play_sound(predator)

            return {
                'type': 'sound',
                'played_sound': played_sound
            }
        else:
            self.flash_light(detected_animal)

            return {
                'type': 'light',
            }

    def play_sound(self, predator):
        sound_file = np.random.choice(self.predator_sound_map[predator])
        if os.path.isfile(sound_file):
            os.system('omxplayer -o both ' + sound_file)
            return sound_file
        else:
            logging.error("Sound file %s not found", sound_file)
            return None

    def flash_light(self, detected_animal):
        for i in range(4):
            gpio.output(11, True)
            time.sleep(np.random.random()*2+.2)
            gpio.output(11, False)
            if i<3:
                time.sleep(np.random.random()+.2)
