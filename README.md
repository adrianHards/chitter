<div align="center">
  <img src="https://github.com/adrianHards/makers-solutions/assets/93719632/981ef8f2-bf8e-424c-835c-d586e319a862" alt="kiwi" width="300">
</div>

# Chitter

A Twitter clone built using [Flask](https://flask.palletsprojects.com/en/2.3.x/), [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) and [Peewee ORM](https://docs.peewee-orm.com/en/latest/peewee/quickstart.html). Users are able to post and interact with messages in real-time!

## Installation

Please ensure that you have `Python` and `Node.js` installed on your system. The following instructions were written for macOS/Linux users.

### Database
Open a terminal, enter `psql`, and then the following commands:
```sql
CREATE DATABASE chitter;
CREATE DATABASE chitter_test;
\l
\q
```

### ENV
1. Open a terminal and navigate to the root folder of the cloned repository.
2. run `echo "SECRET_KEY='my_secret_key_value'" | tee .env`

### App
1. Open a terminal and navigate to the root folder of the cloned repository.

```bash
# 2. create a virtual environment (assuming you have Python 3 installed) by running the following command:
python3 -m venv venv

# 3. activate the virtual environment:
source venv/bin/activate

# 4. install the Python dependencies:
pip install -r requirements.txt

# 4.1 at this point you may want to run the following before continuing:
deactivate
source venv/bin/activate

# 5.1 install the Node.js dependencies using pnpm. If you don't have pnpm installed, you can install it globally by running:
npm install -g pnpm

# 5.2 then, from the root folder of the repository:
pnpm install

# 6. build the Tailwind CSS styles:
pnpm run build:css --watch

# 7. in another terminal tab from the same root folder, start the Flask web server:
python app.py
```

This should start the server, and you should see output indicating that the app is running locally.

8. Open a web browser and visit [http://localhost:5000](http://localhost:5000) to see the app in action.

### WebSocket
Be sure to open the app in two different browsers (or with one window in incognito mode) to test out WebSocket. You'll need two different user accounts in order to see it in action. Have fun!
