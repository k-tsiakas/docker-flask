import time
from flask import Flask, render_template, request
app = Flask(__name__)
import socket

@app.route('/')
def welcome():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print (f"Hostname:{host_name}, IP:{host_ip}")
        client_ip = request.remote_addr
        return render_template('index.html',
                                host_name=host_name,
                                host_ip=host_ip,
                                client_ip=client_ip)
    except:
        return "Unable to get Hostname and IP"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
