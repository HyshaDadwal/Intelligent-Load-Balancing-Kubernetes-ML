import pickle
import numpy as np

class MLPredictor:
    def __init__(self, model_path="load_balancer/ml/model.pkl"):
        with open(model_path, "rb") as file:
            self.model = pickle.load(file)

    def predict_best_server(self, server_metrics):
        predictions = []

        for server in server_metrics:
            features = np.array([[server["cpu"], server["memory"]]])
            score = self.model.predict(features)[0]
            predictions.append((score, server))

        best_server = min(predictions, key=lambda x: x[0])[1]
        return best_server