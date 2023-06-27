import requests
import sqlite3
import json

url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
	"X-RapidAPI-Key": "147f76a7dfmsh05a16b774a51f81p19d27ejsne6c575a9e237",
	"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
}

def createTable():
    conn = sqlite3.connect("covid.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS country_data(id INTEGER PRIMARY KEY AUTOINCREMENT, country TEXT, cases INTEGER, count INTEGER DEFAULT 0)""")
    conn.commit()
    conn.close()

def store(country, data):
    conn = sqlite3.connect("covid.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM country_data WHERE country=?", (country,))
    existing_data = cursor.fetchone()

    if existing_data:
        curr_count = existing_data[3] + 1
        print('what: ', curr_count)
        cursor.execute("UPDATE country_data SET count=? WHERE country=?", (curr_count, country))
        print("Data updated successfully.")
    else:
        cases = data["response"][0]["cases"]["total"]
        cursor.execute("INSERT INTO country_data (country, cases, count) VALUES (?, ?, ?)", (country, cases, 1))
        print("Data stored successfully.")

    conn.commit()
    conn.close()



def getData(country):
    try:
        response = requests.get(url, headers=headers, params={"country": country})
        response.raise_for_status()
        data = response.json()
        if "response" in data and data["response"]:
            store(country, data)
            return data
        else:
            print("No data available for the country:", country)
            return None
    except requests.exceptions.RequestException as error:
        print("Failed to fetch data for the country:", error)
        return None

def printData(data):
    country = data["response"][0]["country"]
    continent = data["response"][0]["continent"]
    population = data["response"][0]["population"]
    total_cases = data["response"][0]["cases"]["total"]
    active_cases = data["response"][0]["cases"]["active"]
    recovered_cases = data["response"][0]["cases"]["recovered"]
    total_deaths = data["response"][0]["deaths"]["total"]
    critical_cases = data["response"][0]["cases"]["critical"]
    print("Country:", country)
    print("Continent:", continent)
    print("Population:", population)
    print("Total cases:", total_cases)
    print("Active cases:", active_cases)
    print("Recovered cases:", recovered_cases)
    print("Total deaths:", total_deaths)
    print("Critical cases:", critical_cases)

createTable()
while True:
    whichInput = int(input("Please Enter 1 search for a specific countries covid 19 data, or 2 to see the latest trending country. Press 3 to quit"))
    if(whichInput == 1):
        inputCountry = input("Enter a country: ")
        if inputCountry:
            returnData = getData(inputCountry)
        if returnData:
            printData(returnData)
    elif(whichInput == 2):
        conn = sqlite3.connect("covid.db")
        cursor = conn.cursor()
        cursor.execute("SELECT country FROM country_data ORDER BY count DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        if result:
            trendingCountry = result[0]
            returnData = getData(trendingCountry)
            printData(returnData)
    elif(whichInput == 3):
        break


    