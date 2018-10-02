from clipper_admin import ClipperConnection, DockerContainerManager
from clipper_admin.deployers import python as py_deployer
import random

cl = ClipperConnection(DockerContainerManager())
cl.stop_all()
cl.start_clipper()

# cl.register_application(name="pong", input_type="doubles", slo_micros=1000000, default_output="1")


def random_predict(xs):
    action = random.randint(0, 2)
    return [str(action) for _ in xs]


# cl.register_application(name="pong", input_type="doubles", default_output="-1.0", slo_micros=100000)

# py_deployer.deploy_python_closure(cl, name="rand-model", version=1, input_type="doubles", func=random_predict, registry="hsubbaraj")

# cl.link_model_to_app(app_name="pong", model_name="rand-model")

py_deployer.create_endpoint(cl, name="pong", input_type="doubles", func=random_predict,
                            default_output="0", slo_micros=100000)

print("CLIPPER ADDRESS: " + cl.get_query_addr())
