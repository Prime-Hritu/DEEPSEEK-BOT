![@Prime-Hritu/DEEPSEEK-BOT](https://socialify.git.ci/Prime-Hritu/DEEPSEEK-BOT/image?custom_description=A+Telegram+bot+that+integrates+MongoDB+and+Huggingface+APIs+to+provide+deep+features.&description=1&font=Jost&forks=1&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZD0iTTEyIDI0YzYuNjI3IDAgMTItNS4zNzMgMTItMTJTMTguNjI3IDAgMTIgMCAwIDUuMzczIDAgMTJzNS4zNzMgMTIgMTIgMTJaIiBmaWxsPSJ1cmwoI2EpIi8%2BPHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik01LjQyNSAxMS44NzFhNzk2LjQxNCA3OTYuNDE0IDAgMCAxIDYuOTk0LTMuMDE4YzMuMzI4LTEuMzg4IDQuMDI3LTEuNjI4IDQuNDc3LTEuNjM4LjEgMCAuMzIuMDIuNDcuMTQuMTIuMS4xNS4yMy4xNy4zMy4wMi4xLjA0LjMxLjAyLjQ3LS4xOCAxLjg5OC0uOTYgNi41MDQtMS4zNiA4LjYyMi0uMTcuOS0uNSAxLjE5OS0uODE5IDEuMjI5LS43LjA2LTEuMjI5LS40Ni0xLjg5OC0uOS0xLjA2LS42ODktMS42NDktMS4xMTktMi42NzgtMS43OTgtMS4xOS0uNzgtLjQyLTEuMjA5LjI2LTEuOTA4LjE4LS4xOCAzLjI0Ny0yLjk3OCAzLjMwNy0zLjIyOC4wMS0uMDMuMDEtLjE1LS4wNi0uMjEtLjA3LS4wNi0uMTctLjA0LS4yNS0uMDItLjExLjAyLTEuNzg4IDEuMTQtNS4wNTYgMy4zNDgtLjQ4LjMzLS45MDkuNDktMS4yOTkuNDgtLjQzLS4wMS0xLjI0OC0uMjQtMS44NjgtLjQ0LS43NS0uMjQtMS4zNDktLjM3LTEuMjk5LS43OS4wMy0uMjIuMzMtLjQ0Ljg5LS42NjlaIiBmaWxsPSIjZmZmIi8%2BPGRlZnM%2BPGxpbmVhckdyYWRpZW50IGlkPSJhIiB4MT0iMTEuOTkiIHkxPSIwIiB4Mj0iMTEuOTkiIHkyPSIyMy44MSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPjxzdG9wIHN0b3AtY29sb3I9IiMyQUFCRUUiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMyMjlFRDkiLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48L3N2Zz4K)

# DEEPSEEK-BOT
**A Telegram bot powered by MongoDB and Huggingface APIs for advanced functionality**  
Developed by [@Prime_Hritu](https://t.me/Prime_Hritu)  
Stay updated via our [Developer Channel](https://t.me/Private_Bots)

---

## 🌟 Overview
**DEEPSEEK-BOT** is a Telegram bot designed to leverage modern APIs and databases to deliver deep functionality to its users.

- It has multiple version of deepseek AIs including Deepseek R1 and Deepseek V3.
---

## ⚙️ Configuration Variables
The bot requires several environment variables to be set. You can use a `.env` file for local development or set these directly in your deployment environment. Below is a table of key configuration variables:

| Variable             | Description                                                                                          |
|----------------------|------------------------------------------------------------------------------------------------------|
| `TOKEN`              | Bot Token generated from [@BotFather](https://t.me/BotFather)                                       |
| `API_HASH`           | Telegram API Hash from [my.telegram.org](https://my.telegram.org/apps)                               |
| `API_ID`             | Telegram API ID from [my.telegram.org](https://my.telegram.org/apps)                                 |
| `OWNER`              | Your Telegram User ID (as retrieved from [@userinfobot](https://t.me/userinfobot))                   |
| `MONGO_URI`          | MongoDB connection URI (if using MongoDB for data storage)                                           |
| `MONGO_NAME`         | MongoDB collection name (defaults to `Deepseek` if not provided)                                     |
| `HUGGINGFACE`        | Huggingface API key for inference tasks                                                            |
| `FORCE`              | Enable/Disable force subscription feature (`true` or `false`)                                        |
| `CHANNEL_LINK`       | URL for the force sub channel (e.g., `https://t.me/Private_Bots`)                                      |
| `CHANNEL_USERNAME`   | Username for the force sub channel (include the `@` prefix, e.g., `@Private_Bots`)                     |
| `PORT`               | Port number for the web server (default: 8000)                                                       |

---

## 🚀 Deployment

### Local Deployment
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Prime-Hritu/DEEPSEEK-BOT.git
   cd DEEPSEEK-BOT
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   - Create a `.env` file based on the `.env-example` and populate it with your credentials.

4. **Run the Bot:**
   ```bash
   python bot.py
   ```

### One-Click Deployments
You can deploy DEEPSEEK-BOT easily on popular platforms:

- [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https://github.com/Prime-Hritu/DEEPSEEK-BOT)
- [![Deploy to Koyeb](https://binbashbanana.github.io/deploy-buttons/buttons/remade/koyeb.svg)](https://app.koyeb.com/services/deploy?name=deepseek-bot&repository=Prime-Hritu%2FDEEPSEEK-BOT&branch=main&type=git&env[TOKEN]=REPLACE_ME&env[API_HASH]=REPLACE_ME&env[API_ID]=REPLACE_ME&env[OWNER]=REPLACE_ME&env[MONGO_URI]=REPLACE_ME&env[MONGO_NAME]=Deepseek&env[HUGGINGFACE]=REPLACE_ME&env[FORCE]=REPLACE_ME&env[CHANNEL_LINK]=REPLACE_ME&env[CHANNEL_USERNAME]=REPLACE_ME&env[PORT]=8000
)
- [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Prime-Hritu/DEEPSEEK-BOT)

---

## 📞 Contact & Support
<image src="https://stylish-social-buttons.vercel.app/?social=telegram&text=Prime_Hritu">

Feel free to open an issue or submit a pull request!


## Libraries Used
You can find the list of libraries used in this project and their purposes in the [Libraries Used](./libraries.md) section.


## 🔖 License
This project is licensed under the [MIT License](LICENSE).

<image x="0" y="0" src="./svg/LOL.svg">