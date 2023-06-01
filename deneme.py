import requests
import random

N_CLASSES = 10
PER_CLASS = 10

def send_feedback(proba):
    
    for i in range(N_CLASSES):
        for j in range(PER_CLASS):
            r = [0] * N_CLASSES
            t = [0] * N_CLASSES
            r[i] = 1
            if random.random() * 100 < proba:
                t = r
            else:
                t[(i+1) % N_CLASSES] = 1
            f_req = {"response": {"data": { "ndarray": r }}, "truth": {"data": { "ndarray": t }}}

            requests.post("http://localhost:8000/metrics", 
                         json=f_req)
            
send_feedback(600)