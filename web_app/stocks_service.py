import requests

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=abc123"

res = requests.get(request_url)

print(res)

print(res.status_code)
print(type(res.text))

parsed_res = json.loads(res.text)
print(type(parsed_res))
print(parsed_res.keys())
