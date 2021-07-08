pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir db
touch .env
sudo nano .env
python server.py

#ACCESS_ID = 'user_id'
#API_TOKEN = 'your_API_TOKEN'