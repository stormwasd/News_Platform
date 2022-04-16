"""
@Description : 
@File        : run
@Project     : News_Platform_Front_End
@Time        : 2022/4/16 9:37
@Author      : LiHouJian
@Software    : PyCharm
@issue       : 
@change      : 
@reason      : 
"""

import os
pre_path = os.path.dirname(os.path.realpath(__file__))
os.system('python3 {}/manage.py runserver 0.0.0.0:9000 --insecure'.format(pre_path))
