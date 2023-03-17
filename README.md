ScribbleDiffusionTGBot
---
---

This simple **unofficial** bot uses API of Replicate-powered app [scribblediffusion.com](https://scribblediffusion.com/).

---

[scribblediffusion.com](https://scribblediffusion.com/) is powered by:

🚀 [Replicate](https://replicate.com/jagilley/controlnet-scribble), a platform for running machine learning models in the cloud.

🖍️ [ControlNet](https://github.com/replicate/controlnet), an open-source machine learning model that generates images from text and scribbles.

---
**Usage:**
* Create a Telegram bot using [BotFather](https://core.telegram.org/bots#how-do-i-create-a-bot).
* Clone the repo.
* Add `.env` file with `TELEGRAM_TOKEN = "<your_token>"` to `./app` folder.
* Open the root folder of the repository.
* Run `pip install -r requirements.txt` to install required packages.
* Run `python app/bot.py`.
* Send prompt (image/document with caption) to your bot.

---
Available to deploy on [Railway](https://railway.app/) or [Render](https://render.com/).

---
Example: https://t.me/scribble_diff_bot