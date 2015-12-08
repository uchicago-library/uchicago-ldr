
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from uchicagoldr.newlogging import MessageReceiver

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def receive_message():
    if request.method == 'POST':
        data = request.form
        receiver = MessageReceiver(data)
        if getattr(receiver, 'receipt_date', None):
            level = receiver.level
            getattr(app.logger,level)(str(receiver)

if __name__ == "__main__":
    handler = RotatingFileHandler('ldr.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run()
