from prometheus_client import Gauge, generate_latest, REGISTRY

my_metric = Gauge('my_metric', 'Description of my metric')

global_accuracy = Gauge('global_accuracy', 'Description of Global Accuracy')

global_loss = Gauge('global_loss', 'Description of Global Loss')

global_precision = Gauge('global_precision', 'Description of Global Precision')

global_recall = Gauge('global_recall', 'Description of Global Recall')

global_f1_score = Gauge('global_f1_score', 'Description of Global F1 Score')

