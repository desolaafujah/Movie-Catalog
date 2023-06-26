import requests
import sqlite3

url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
	"X-RapidAPI-Key": "147f76a7dfmsh05a16b774a51f81p19d27ejsne6c575a9e237",
	"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
}

def createTable():
    conn = sqlite3.connect("covid.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS country_data(id INTEGER PRIMARY KEY AUTOINCREMENT, country TEXT, cases INTEGER)""")
    conn.commit()
    conn.close()

def store(country, data):
    cases = data["response"][0]["cases"]["total"]
    conn = sqlite3.connect("covid.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO country_data (country, cases) VALUES (?, ?)", (country, cases))
    conn.commit()
    conn.close()

response = requests.get(url, headers=headers)

def getData(country):
    response = requests.get(url, headers=headers, params={"country": country})
    response.raise_for_status()
    data = response.json()
    cases = data["response"][0]["cases"]["total"]
    store(country, data)
    return data

createTable()
inputCountry = input("Enter a country: ")

if(inputCountry):
    returnData = getData(inputCountry)
    if(returnData):
        print(returnData)