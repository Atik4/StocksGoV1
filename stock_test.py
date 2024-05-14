import requests

url = "https://alpha-vantage.p.rapidapi.com/query"

querystring = {"interval":"15min","function":"TIME_SERIES_DAILY","symbol":"HAL.BSE","datatype":"json","output_size":"compact"}

headers = {
    "X-RapidAPI-Key": "3853b61d53mshdf908a83515c541p17b5f2jsn0e8f904623b5",
    "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring, verify=False)

print(response.json())