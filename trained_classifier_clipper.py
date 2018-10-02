from clipper_admin import ClipperConnection, DockerContainerManager, KubernetesContainerManager
from clipper_admin.deployers import python as py_deployer
import random
import pandas as pd
from datascience import *
import numpy as np
from sklearn import linear_model

clipper_conn = ClipperConnection(DockerContainerManager())
clipper_conn.connect()

data_table= Table.read_table('output.csv')
def convert_label(label):
    if(label=="down"):
        return 1
    elif(label=="up"):
        return 2
    else:
        return 0
data_table_2 = data_table.with_column("label", data_table.apply(convert_label, 0))

final_table = Table().with_columns("label", data_table.apply(convert_label, 0),
                                  "paddle_y", data_table.column(1)/500.0,
                                  "ball_x", data_table.column(3)/500.0,
                                  "ball_y", data_table.column(4)/500.0,
                                  "ball_dx", data_table.column(5)/500.0,
                                  "ball_dy", data_table.column(6)/500.0,
                                  "x_prev", data_table.column(7)/500.0,
                                  "y_prev", data_table.column(8)/500.0)
data_df = final_table.to_df()
labels = data_df['label']

training_data= data_df.drop(['label'], axis=1)
model = linear_model.LogisticRegression()
model.fit(training_data, labels)

clipper_conn.register_application(name="pong-trained-6", input_type="doubles", 
                                  default_output="-1.0", slo_micros=100000)
def predict(inputs):
    # model.predict returns a list of predictions
    print(inputs)
    print(type(inputs))
    preds = model.predict(inputs)
    print(preds)
    print(type(preds))
    return [str(p) for p in preds]

py_deployer.deploy_python_closure(clipper_conn, name="pong", version=2, input_type="doubles", func=predict, pkgs_to_install=["numpy","scipy", "pandas", "datascience", "sklearn"])

clipper_conn.link_model_to_app('pong-trained-6', 'p-trained-6')

print("CLIPPER ADDRESS: " + clipper_conn.get_query_addr())
