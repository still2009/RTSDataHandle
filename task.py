# coding:UTF-8
from update2file import *
from datetime import datetime
now = datetime.now()
if now.hour == 8 and now.minute == 55:
    update2file.run()
