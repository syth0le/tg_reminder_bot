# tg_reminder_bot
telegram bot with async realisation remind functional

## для начала работы проделайте следующие шаги:
* зарегистрируйте нового бота в telegram и возьмите его API_TOKEN 
* узнайте свой user_id в telegram
* установите python 3.8+ для корректной работы с ботом
* склонируйте репозиторий
  > git clone https://github.com/syth0le/tg_reminder_bot.git
* а теперь выполните ряд команд:
    >$ cd tg_reminder_bot
    > 
    >$ pip install virtualenv
    > 
    >$ virtualenv venv
    > 
    >$ source venv/bin/activate
    > 
    >$ pip install -r requirements.txt
* Cоздаем файл с переменными необходимыми в работе бота:
    >$ touch .env
    > 
    >$ sudo nano .env
  * в открытом окошке редактирования файла .env заполните его так:
    > ACCESS_ID = 'user_id'
    > 
    > API_TOKEN = 'your_API_TOKEN'
* сохраняем файл и запускаем бота:
    > python server.py

В будущем напишу shell скрипт для автоматического выполнения шагов.
Приятного пользования!
  