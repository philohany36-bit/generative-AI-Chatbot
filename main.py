from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid

app = FastAPI(title="Nexura Generative AI Chatbot", version="2.0")

# نظام إدارة الذاكرة المؤقتة وسياق المحادثة للجلسات
conversation_sessions = {}

class ChatRequest(BaseModel):
    user_id: str
    message: str

class GenerativeChatEngine:
    def __init__(self):
        self.system_prompt = (
            "أنت مساعد افتراضي ذكي ومتقدم تابع لشركة Nexura Solutions. "
            "مهمتك الإجابة على استفسارات العملاء بمرونة تامة وذكاء اصطناعي توليدي احترافي."
        )

    def get_session(self, user_id: str):
        if user_id not in conversation_sessions:
            conversation_sessions[user_id] = [
                {"role": "system", "content": self.system_prompt}
            ]
        return conversation_sessions[user_id]

    def process_message(self, user_id: str, user_message: str) -> str:
        history = self.get_session(user_id)
        
        # إضافة رسالة العميل للذاكرة
        history.append({"role": "user", "content": user_message})
        
        # محاكاة الرد التوليدي الذكي (يمكنك ربطه لاحقاً بـ OpenAI API أو Google Gemini)
        bot_reply = (
            f"مرحباً بك في Nexura Solutions! 🚀\n"
            f"لقد تلقيت استفسارك الذكي: ( {user_message} ).\n"
            f"بصفتي نظام Generative AI متقدم، أنا جاهز لتحليل طلبك بدقة وتوفير الحل البرمجي أو التقني المناسب لك."
        )
        
        # حفظ رد البوت في السجل
        history.append({"role": "assistant", "content": bot_reply})
        
        return bot_reply

bot_engine = GenerativeChatEngine()

# واجهة ويب تفاعلية حديثة وسلسة للتحدث مع البوت مباشرة
HTML_UI = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexura Generative AI Chatbot</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0b0f19; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .chat-container { width: 100%; max-width: 480px; background: #1e293b; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); display: flex; flex-direction: column; height: 92vh; overflow: hidden; border: 1px solid #334155; }
        .chat-header { background: linear-gradient(135deg, #2563eb, #1d4ed8); padding: 20px; text-align: center; font-weight: bold; font-size: 20px; color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 14px; background: #0f172a; }
        .message { padding: 14px 18px; border-radius: 12px; max-width: 85%; line-height: 1.6; white-space: pre-line; word-break: break-word; font-size: 15px; }
        .user { background: #2563eb; align-self: flex-end; border-bottom-left-radius: 4px; color: #fff; }
        .bot { background: #334155; align-self: flex-start; border-bottom-right-radius: 4px; color: #f1f5f9; }
        .chat-input { display: flex; border-top: 1px solid #334155; padding: 15px; background: #1e293b; gap: 10px; }
        .chat-input input { flex: 1; padding: 12px 16px; border: 1px solid #475569; border-radius: 10px; background: #0f172a; color: #fff; outline: none; font-size: 15px; }
        .chat-input input:focus { border-color: #2563eb; }
        .chat-input button { background: #2563eb; color: white; border: none; padding: 12px 20px; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 15px; transition: background 0.2s; }
        .chat-input button:hover { background: #1d4ed8; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">Nexura AI Chatbot 🤖</div>
        <div class="chat-messages" id="chatMessages"></div>
        <div class="chat-input">
            <input type="text" id="userInput" placeholder="اكتب رسالتك هنا للبوت الذكي..." onkeypress="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">إرسال</button>
        </div>
    </div>

    <script>
        const userId = "client_user_" + Math.floor(Math.random() * 10000);

        function appendMessage(text, sender) {
            const chatMessages = document.getElementById('chatMessages');
            let msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender}`;
            msgDiv.innerText = text;
            chatMessages.appendChild(msgDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // إرسال رسالة ترحيبية تلقائية عند فتح الشات
        window.onload = () => {
            appendMessage("مرحباً بك! أنا مساعد Nexura التوليدي الذكي. كيف يمكنني مساعدتك في مشروعك اليوم؟", "bot");
        };

        function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (!message) return;

            appendMessage(message, 'user');
            input.value = '';

            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, message: message })
            })
            .then(res => res.json())
            .then(data => {
                appendMessage(data.reply, 'bot');
            })
            .catch(err => {
                appendMessage("عذراً، حدث خطأ في الاتصال بالخادم.", "bot");
            });
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_UI

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        reply = bot_engine.process_message(request.user_id, request.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
