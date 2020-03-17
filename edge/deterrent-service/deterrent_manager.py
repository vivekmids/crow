import logging
import numpy as np
import os
# note: we keep these two functions separate since our logic to decide
# which deterrent to deploy might get pretty complicated.
class Deter:
    def __init__(self):
        self.predator_map = {'skunk':['dog', 'human', 'coyote'],
                             'rodent':['dog', 'human', 'coyote', 'cat'],
                             'squirrel':['dog', 'human', 'coyote', 'cat'],
                             'rabbit':['dog', 'human', 'coyote', 'hawk'],
                             'bird': ['dog', 'human', 'coyote', 'gun', 'hawk'],
                             'deer': ['human', 'coyote', 'cheetah', 'cougar', 'bobcat', 'leopard', 'tiger'],
                             'raccoon':['dog', 'human', 'coyote'],
                             'opossum':['dog', 'human', 'coyote', 'gun', 'hawk']}
        self.predator_sound_map = {}
        for pest, predators in self.predator_map.items():
            self.predator_sound_map[pest] = []
            for predator in predators:
                try:
                    path = os.path.join("sound",predator)
                    sound_files = os.listdir(path)
                    sound_files = [os.path.join(path, sound_file) for sound_file in sound_files]
                    self.predator_sound_map.get(pest).extend(sound_files)
                except Exception as e:
                    logging.error("Sound files for %s in folder %s not found", pest, predator)
                    raise e

    def deploy_deterrent(self, detected_animal):
        if self.day():
            """Here we choose deterrent to deploy"""
            sounds = self.predator_sound_map.get(detected_animal, 'NOT FOUND')
            if sounds != 'NOT FOUND':
                sound = np.random.choice(sounds)
                if os.path.isfile(sound): 
                    os.system('omxplayer -o both ' + sound)
                else:
                    logging.error("Sound file %s not found", sound)
                    
            else:
                logging.error("No sound files found for %s", detected_animal)
                return False
            
            return sound
        
        else:
            pass
            #code for deploying light 


    def day(self):
        #TODO implement code for day vs night
        return True
        
