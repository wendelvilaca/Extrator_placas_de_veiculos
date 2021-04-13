import requests


with open("1.jpg", "rb") as imageFile:
    url = 'http://ec2-54-165-64-132.compute-1.amazonaws.com:80/image'
    headers = {'Content-Type': 'application/octet-stream'}
    try:
        response = requests.post(url, files=[('image_data',('1.jpg', imageFile, 'image/png'))])
        print(response.status_code)
        print(response.json())
    except Exception as e:
        print(e)
    print(response.text)