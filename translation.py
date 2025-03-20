class TEXT:
    START = """
🌟 **Welcome to the DeepSeek AI Bot!** 🤖

<i>Hello there! I’m your AI-powered assistant here to help you with:</i>
🔍 **Research & Information**
📚 **Learning & Knowledge**
✍️ **Writing & Editing**
🧠 **Brainstorming & Problem-Solving**
...and much more!

<i>Simply type your question or task, and I’ll do my best to assist you.</i>

<b>Let’s get started! How can I help you today? 😊</b>
"""
    ABOUT = """
<b>🤖 DeepSeek AI Telegram Bot</b>

<i>Welcome to <b>DeepSeek AI</b>, your intelligent assistant powered by cutting-edge AI technology! This bot is designed to provide you with smart, context-aware responses and assistance for a wide range of tasks.</i>

<b>📌 Features:</b><i>
- Intelligent conversation handling 🧠
- Context-aware responses 📚
- Quick and efficient performance ⚡
- Easy-to-use interface 💬</i>

<b>🛠️ Technical Details:</b><i>
- Built with <b>Python 3.10</b> 🐍
- Powered by the <b>Pyrogram</b> framework 🔥
- Hosted on a reliable server for 24/7 availability 🌐</i>

Stay tuned for more updates and improvements! 🚀
"""
    HELP = """
<b>🤖 DeepSeek AI Bot Help</b>

Welcome to the <b>DeepSeek AI Telegram Bot</b>! 🚀
This bot provides access to advanced AI models for intelligent and conversational interactions. Here’s how to use it:

<b>🎯 Available Models:
<i>The bot supports the following AI models:</i></b>
<i>🧠 <code>DeepSeek-V3</code></i>
<i>🧠 <code>DeepSeek-R1</code></i>
<i>🧠 <code>DeepSeek-R1-Distill-Qwen-1.5B</code></i>
<i>🧠 <code>DeepSeek-R1-Distill-Qwen-14B</code></i>

<b>⚙️ /settings:</b>
You can switch between the available models and languages in the <b>/settings</b> menu. Simply select your preferred model, and the bot will use it for all future interactions.

<b>🔄 /restart:</b>
Use this command to restart the bot in case of any issues or if you want to refresh the session.

<b>ℹ️ /about:</b>
Learn more about DeepSeek AI, its capabilities, and the technology powering this bot.

<b>💬 Chat:</b>
Just type your message, and the bot will respond using the currently selected model.

<b>❓ Need Help? /help</b>
If you have any questions or issues, feel free to reach out!

Happy chatting! 🎉
"""
    SETTINGS = """
<b>🤖 DeepSeek AI Bot Settings</b>
                     
<b>✅ Models: </b><i>Models are the backbone of AI, enabling it to understand and generate human-like responses during conversations. They rely on complex algorithms, training data, and continuous improvements to perform effectively.</i>
<i>*Changing the model will effect the response*</i>
                     
<i>*Upon changing language bot will respond in that (selected) language*</i>
"""
    FORCE_SUB_TEXT = (
        "<b>Please Join [ </b><a href='{}'>{}</a> <b>] to continue using this bot.</b>"
    )
    BROADCAST = "<b><i>Broadcast Status:\n\nSuccess: {}\nFailed: {}</i></b>"
    FETCHING_DATABSE = "<b><i>⚙️ Fetching database...</i></b>"
    STATUS = "<b>Status:</b>\n\n<i>Total Users: {}</i>"
