import pickle
from flask import Flask, jsonify, request
from model import infer, load_model
import numpy as np

app = Flask(__name__)
app.model = load_model()


@app.route('/', methods=['POST'])
def perform_inference():
    """Takes input in the form of
    {
        "image": '..'  # pickle.dumps(image_ndarray).decode('latin-1')
    }
    """
    data = request.get_json(force=True)
    image = pickle.loads(data['image'].encode('latin-1')).astype(np.float32)
    
    #for testing purpose
    #pickle.dump(image, open("img_for_inference", "wb"))

    found_something, detected_animals = infer(app.model, image)

    return jsonify({
        'found_something': found_something,
        'detected_animals': detected_animals
    })


def main():
    app.run('0.0.0.0', port=5050, threaded=False, processes=3)


if __name__ == '__main__':
    main()
