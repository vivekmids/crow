

class StupidModel(object):
    def __call__(self, image):
        return "racoon"


def load_model():
    """Here lies logic to load the model"""
    # TODO: load an actual model
    return StupidModel()


def infer(model, image):
    """Here is the code that to perform inference using the model.
    Expect this to be the model you return in `load_model()`

    Args:
        model: one built using load_model
        image: numpy array as created by opencv

    Returns: bool, list(string)
        - a boolean to signal we found something
        - a list of found animals
    """
    return True, [model.__call__(image)]
