import tensorflow as tf
import logging
import time
import pickle

class StupidModel(object):
    def __call__(self, image):
        return "racoon"

with open('inference-service/prediction_map.pickle', 'rb') as f:
    prediction_map = pickle.load(f)

def load_model():
    """Here lies logic to load the model"""
    # load model from h5 file
    logging.warning('Starting load model')
    start = time.perf_counter()
    model = tf.lite.Interpreter(model_path="model/converted_quant_model_v2.tflite")
    model.allocate_tensors()
    end = time.perf_counter()
    logging.warning(f'Model loaded in {end-start} seconds')
#    input_details = model.get_input_details()
#    output_details = model.get_output_details()
    
    # Test model on random input data.
#    input_shape = input_details[0]['shape']
#    input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
#    model.set_tensor(input_details[0]['index'], input_data)

#    model.invoke()

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
    
    #classes = ['skunk','fox','rodent','dog','squirrel','cat','rabbit','bird','cow','bobcat','deer','raccoon','coyote','opossum']
    #classes_dict_lookup = dict(zip(range(15), classes+['other']))
#     with open('inference-service/prediction_map.pickle', 'rb') as f:
#         prediction_map = pickle.load(f)

    # run inference
    #logging.warning(str(model.get_input_details()))
    model.set_tensor(312, image)
    model.invoke()
    
    predicted_id = model.get_tensor(0)
    logging.warning('predicted_id.argmax() '+ str(predicted_id.argmax()))
    logging.warning('predicted_id.shape '+ str(predicted_id.shape))
    predicted_name = prediction_map[predicted_id.argmax()]
    
    logging.warning('Probability of top class is '+ str(predicted_id.max()))
    
    if predicted_name != 'empty':
        return True, predicted_name
    else:
        return True, 'rabbit'
