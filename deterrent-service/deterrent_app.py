from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/', methods=['POST'])
def deter():
    """Takes input in the form of
    {
        "image": '..'  # pickle of image
    }
    """
    data = request.get_json(force=True)
    detected_animals = data['detected_animals']

    # deploy all the deterrents

    return jsonify({
        'deployed_deterrent': 'sound',  # or whatever
    })


def main():
    app.run(port=5100)


if __name__ == '__main__':
    main()
