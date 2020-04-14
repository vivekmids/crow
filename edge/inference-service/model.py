import tensorflow as tf
import logging
import time
from tensorflow.python.keras.applications.inception_v3 import preprocess_input

class StupidModel(object):
    def __call__(self, image):
        return "racoon"


def load_model():
    """Here lies logic to load the model"""
    # load model from h5 file
    logging.warning('Starting load model')
    start = time.perf_counter()
    model = tf.lite.Interpreter(model_path="model/converted_quant_model_v2.tflite")
    model.allocate_tensors()
    end = time.perf_counter()
    logging.warning(f'Model loaded in {end-start} seconds')
    input_index = model.get_input_details()[0]['index']
    output_index = model.get_output_details()[0]['index']

    with open('edge/inference-service/prediction_map.pickle', 'rb') as f:
        prediction_map = pickle.load(f)

    return model, input_index, output_index, prediction_map


def infer(model, image, input_index, output_index, prediction_map):
    """Here is the code that to perform inference using the model.
    Expect this to be the model you return in `load_model()`

    Args:
        model: one built using load_model
        image: numpy array as created by opencv

    Returns: bool, list(string)
        - a boolean to signal we found something
        - name of identified animals
    """
    
    #classes = ['skunk','fox','rodent','dog','squirrel','cat','rabbit','bird','cow','bobcat','deer','raccoon','coyote','opossum']
    #classes_dict_lookup = dict(zip(range(15), classes+['other']))

    # run inference
    image = preprocess_input(image)
    model.set_tensor(input_index, image)
    model.invoke()
    
    predicted_id = model.get_tensor(output_index)
    predicted_name = prediction_map[predicted_id.argmax()]
    
    logging.warning('Probability of top class is '+ str(predicted_id.max()))
    
    if predicted_name != 'empty':
        return True, predicted_name
    else:
        return False, None
