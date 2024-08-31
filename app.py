from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
from g4f.client import Client
from g4f.providers import Aichat  # Import provider mà bạn muốn sử dụng
import os

app = Flask(__name__)
app.secret_key = 'huankk123@@'  # Thay thế 'your_secret_key' bằng một chuỗi ngẫu nhiên an toàn
CORS(app)
client = Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')

    if 'conversation' not in session:
        session['conversation'] = []

    # Thêm tin nhắn người dùng vào cuộc trò chuyện
    session['conversation'].append({"role": "user", "content": user_input})

    # Gửi toàn bộ lịch sử cuộc trò chuyện đến GPT-4
    print("Lịch sử cuộc trò chuyện gửi đi:", session['conversation'])  # Log lịch sử cuộc trò chuyện

    try:
        # Sử dụng provider từ g4f, ví dụ: Aichat
        response = client.chat.completions.create(
            model="gpt-4",
            messages=session['conversation'],
            provider=Aichat()  # Thay đổi provider ở đây nếu cần
        )
        
        reply = response.choices[0].message.content
        print("Phản hồi từ GPT-4:", reply)  # Log phản hồi từ GPT-4

        # Thêm phản hồi của chatbot vào lịch sử cuộc trò chuyện
        session['conversation'].append({"role": "assistant", "content": reply})

        return jsonify({'reply': reply})

    except Exception as e:
        print(f"Lỗi xảy ra: {e}")
        return jsonify({'reply': "Hiện tại hệ thống đang gặp sự cố, vui lòng thử lại sau."})

if __name__ == '__main__':
    app.run()
