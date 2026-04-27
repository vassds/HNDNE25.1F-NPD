import urllib.request

url = "https://www.google.com"

try:
    response = urllib.request.urlopen(url)
    print(f"Response code: {response.getcode()}")
    html_data = response.read(100)
    print(f"responce:{html_data}")
except Exception as e:
        print(f"Connectio Faild!{e}")