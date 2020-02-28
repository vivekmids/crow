import pickle

from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/', methods=['POST'])
def infer():
    """Takes input in the form of
    {
        "image": '..'  # pickle.dumps(image_ndarray).decode('latin-1')
    }
    """
    data = request.get_json(force=True)
    image = pickle.loads(data['image'].encode('latin-1'))

    # do all the inferences

    return jsonify({
        'found_something': True,  # was an inference made and successful,
        'detected_animals': ['racoon']  # what did we find
    })


def main():
    app.run(port=5050)


if __name__ == '__main__':
    main()
