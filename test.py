import time
from datetime import datetime

a= '1.23.1993'
now= datetime.now()
now=now.strftime("%d.%m.%Y")
print ( now,'\n',a)
if now<a:

    print(1)