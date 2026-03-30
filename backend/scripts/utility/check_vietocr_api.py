from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

try:
    config = Cfg.load_config_from_name("vgg_transformer")
    config["cnn"]["pretrained"] = False
    config["device"] = "cpu"
    predictor = Predictor(config)
    print(f"Has predict_batch: {hasattr(predictor, 'predict_batch')}")
except Exception as e:
    print(f"Error: {e}")
