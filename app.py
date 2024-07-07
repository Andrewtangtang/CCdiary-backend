from flask import Flask, request, jsonify
from processdiary import DiaryFeedback
from diseasechatbot import DiseaseChatbot
from sentiment_analysis import SentimentAnalyser
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
app = Flask(__name__)


@app.route('/feedback', methods=['POST'])
def get_feedback():
    query = request.get_json()
    diary_description = query["diary_description"]
    if query["language"] == "zh_Hant_TW":
        language = "Traditional Chinese"
    else:
        language = "English"
    print(diary_description)
    feed_back = diary_feedback.process(diary_description, language)
    print(feed_back)
    return jsonify({'feedback': feed_back})


@app.route('/query', methods=['POST'])
def get_answer():
    query = request.get_json()
    question = query["question"]
    if query["language"] == "zh_Hant_TW":
        language = "Traditional Chinese"
    else:
        language = "English"
    answer = disease_chatbot.get_answer(question, language)
    return jsonify({'answer': answer})
@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    diary_feedback = DiaryFeedback()
    disease_chatbot = DiseaseChatbot()
    # sentiment_analyser = SentimentAnalyser()
    app.run(host='0.0.0.0', port=5000, debug=True)
