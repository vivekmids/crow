import tensorflow as tf
from tensorflow.python.keras.applications.inception_v3 import preprocess_input

class StupidModel(object):
    def __call__(self, image):
        return "racoon"


def load_model():
    """Here lies logic to load the model"""
    # load model from h5 file

    model = tf.lite.Interpreter(model_path="model/converted_quant_model_v1_top_layer.tflite")
    model.allocate_tensors()
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

    classes = ['rodent','squirrel','rabbit','bird','deer','raccoon','skunk','opossum']
    classes_dict_lookup = dict(zip(range(10), classes + ['other'] + ['empty']))

    # run inference
    image = preprocess_input(image)
    model.set_tensor(1, image)
    model.invoke()

    predicted_id = model.get_tensor(0)
    predicted_name = classes_dict_lookup[predicted_id.argmax()]

    if predicted_name in classes:
        return True, predicted_name
    else:
        return False, None
