from clipper_admin import ClipperConnection, DockerContainerManager
from clipper_admin.deployers import python as py_deployer
import random

cl = ClipperConnection(DockerContainerManager())
clipper_url="http://localhost:1337/pong/predict"

headers = {'Content-Type': 'application/json'}
start = datetime.now()
clipper_response = requests.post(clipper_url, headers=headers, data=json.dumps(req_json))



