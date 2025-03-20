![@Prime-Hritu/DEEPSEEK-BOT](https://socialify.git.ci/Prime-Hritu/DEEPSEEK-BOT/image?custom_description=An+advanced+deepseek+AI+telegram+bot+with+mutiple+language+support.&description=1&font=KoHo&forks=1&name=1&owner=1&pattern=Floating+Cogs&stargazers=1&theme=Auto)

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

---

<br><br>
<p align="center">
<a href="https://www.buymeacoffee.com/hritu" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;">
</a>
</p>
<image x="0" y="0" src="./svg/LOL.svg">