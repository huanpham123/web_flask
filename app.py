from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
from g4f.client import Client
import os
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
CORS(app)
client = Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('message')

        if 'conversation' not in session:
            session['conversation'] = []

        # Thêm tin nhắn người dùng vào cuộc trò chuyện
        session['conversation'].append({"role": "user", "content": user_input})

        # Gửi toàn bộ lịch sử cuộc trò chuyện đến GPT-4
        logger.info("Lịch sử cuộc trò chuyện gửi đi: %s", session['conversation'])
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=session['conversation'],
        )
        
        reply = response.choices[0].message.content
        logger.info("Phản hồi từ GPT-4: %s", reply)

        # Thêm phản hồi của chatbot vào lịch sử cuộc trò chuyện
        session['conversation'].append({"role": "assistant", "content": reply})

        return jsonify({'reply': reply})
    
    except Exception as e:
        logger.error("Lỗi khi xử lý yêu cầu: %s", str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run()
