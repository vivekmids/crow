from flask import Flask, request, jsonify


app = Flask(__name__)


def get_images():
    """Here we should return a list of images the customer has already seen
    """
    return []


def save_image(payload):
    """Here we save the images. The input data will be:
            {
                'updated': True,
                'device_id': device_id,
                'cam_id': cam_id,
                'inference_response': inference_response,
                'deterrent_response': deterrent_response
            }

    return:
        Any useful metadata that will be useful for the edge device
        We will simply be logging this data so it doesn't really matter
    """
    return {}


@app.route('/', methods=['GET', 'POST'])
def handle_route():
    if request.method == 'GET':
        return jsonify(get_images())
    elif request.method == 'POST':
        payload = request.get_json(force=True)
        return jsonify(save_image(payload))


def main():
    app.run('0.0.0.0', 8000)


if __name__ == '__main__':
    main()
