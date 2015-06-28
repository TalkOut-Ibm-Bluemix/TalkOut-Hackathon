#!/bin/env python
from gevent import monkey
import os
monkey.patch_all()
from app import create_app, socketio

app = create_app(True)

if __name__ == '__main__':
    port = os.getenv('VCAP_APP_PORT', '5000')
    socketio.run(app,host='0.0.0.0', port=int(port))
