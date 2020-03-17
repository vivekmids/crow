from tensorflow.python.keras.models import load_model as keras_load_model

class StupidModel(object):
    def __call__(self, image):
        return "racoon"


def load_model():
    """Here lies logic to load the model"""
    # load model from h5 file
    model = keras_load_model('model/combined_model.h5')
    return model


def infer(model, image):
    """Here is the code that to perform inference using the model.
    Expect this to be the model you return in `load_model()`

    Args:
        model: one built using load_model
        image: numpy array as created by opencv

    Returns: bool, list(string)
        - a boolean to signal we found something
        - name of identified animals
    """
    
    classes = ['skunk','fox','rodent','dog','squirrel','cat','rabbit','bird','cow','bobcat','deer','raccoon','coyote','opossum']
    classes_dict_lookup = dict(zip(range(15), classes+['other']))
    
    # run inference
    predicted_id = model.predict(image)
    predicted_name = classes_dict_lookup[predicted_id.argmax()]
    
    if predicted_name in classes:
        return True, predicted_name
    else:
        return False, None
