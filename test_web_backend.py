import requests
import numpy as np
import pickle
from PIL import Image

img = Image.open("/home/ocamlmycaml/Downloads/deer-silo.jpg")
img = img.resize(size=(299, 299))
img = np.array(img)

print("before request")
resp = requests.post('http://localhost:8000/api/inferences', json={
    "cam_id": "0",
    "device_id": "local-test-script",
    'image': pickle.dumps(img).decode('latin-1'),
    "updated": True,
    "inference_response": {
        "detected_animals": "deer",
        "found_something": True
    },
    "deterrent_response": {
        "deployed_deterrent": {
            "played_sound": "/home/pi/crow/edge/deterrent-service/sound/test_script/sound.mp3",
            "type": "sound"
        }
    },
}, headers={
    'Content-type': 'application/json'
})

print(f"Status code: {resp.status_code}")
print(f"Response:\n{resp.text}")
