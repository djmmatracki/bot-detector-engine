# from helpers.detectors.schemas import Sample, Score
import tensorflow as tf

class TextDetector:
    def __init__(self, model_path: str) -> None:
        self.model = tf.keras.models.load_model(model_path)

    def detect(self, sample: str):
        return self.model.signatures['serving_default'](tf.constant([sample]))

text_model = TextDetector("models/text_detection")
