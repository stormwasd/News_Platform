"""
@Description :
@File        : test_upload
@Project     : Img_Upload
@Time        : 2022/4/8 15:18
@Author      : LiHouJian
@Software    : PyCharm
@issue       :
@change      :
@reason      :
"""

import requests
from urllib3 import encode_multipart_formdata

img_url = 'https://www.cscline.com/uploads/allimg/191029/1029533a3-0.png'
file_name = 'test'
upload_url = 'http://127.0.0.1:5000/upload'
res = requests.get(img_url)

file = {
	"file": (file_name, res.content)
}

encode_data = encode_multipart_formdata(file)
file_data = encode_data[0]
headers_form_data = {
	"Content-Type": encode_data[1]
}

response = requests.post(url=upload_url, headers=headers_form_data, data=file_data)
print(response.json())

