from api.api_method import server_run
from web_app.web_server import start
from threading import Thread
th = Thread(target=start)
th.start()
server_run()