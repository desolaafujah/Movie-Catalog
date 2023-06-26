import requests

url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
	"X-RapidAPI-Key": "147f76a7dfmsh05a16b774a51f81p19d27ejsne6c575a9e237",
	"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())