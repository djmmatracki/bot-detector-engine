from helpers.detectors.bot_detector import BotDetector

bot_detector = BotDetector(
    text_model_path="models/text_detection",
    user_model_path="models/app_detection/xgb_model_5a.pkl",
)