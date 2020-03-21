from flask import Flask, jsonify, request, current_app

from deterrent_manager import DeterrentManager


app = Flask(__name__)
app.deterrent_manager = DeterrentManager()


@app.route('/', methods=['POST'])
def deter():
    """Takes input in the form of
    {
        'detected_animals': ['racoon']  # list if we ever wanna handle multiple
    }
    """
    data = request.get_json(force=True)
    detected_animals = data['detected_animals']

    # deploy all the deterrents
    deterrent = current_app.deterrent_manager.deploy_deterrent(detected_animals)

    return jsonify({
        'deployed_deterrent': deterrent
    })


def main():
    app.run('0.0.0.0', port=5100)


if __name__ == '__main__':
    main()
