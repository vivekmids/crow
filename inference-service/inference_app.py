import pickle

from flask import Flask, jsonify, request

from model import infer, load_model


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
    image = pickle.loads(data['image'].encode('latin-1'))

    found_something, detected_animals = infer(app.model, image)

    return jsonify({
        'found_something': found_something,
        'detected_animals': detected_animals
    })


def main():
    app.run(port=5050)


if __name__ == '__main__':
    main()
