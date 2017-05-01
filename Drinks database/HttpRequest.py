import json
from pprint import pprint
import urllib2
import Drink


# Scrapes the web page of the Absolut Drinks Database.
def scrapePage(nextUrl, firstScrape):
    urlToApi = "http://addb.absolutdrinks.com"
    apiKey = "/?apiKey=4093c8e39ec5436391012017bc354c01"
    url = urlToApi + "/" + "drinks" + apiKey

    if nextUrl:
        url = nextUrl
    if not nextUrl and not firstScrape:
        return

    return json.load(urllib2.urlopen(url))


# Creates the database of drinks.
def createDatabase(data):
    for element in data.get("result"):
        info = getInfo(element)
        makeDrink = getattr(Drink, "createDrink")
        drink = makeDrink(info[0], info[1], info[2], info[3], info[4], info[5],
            info[6],info[7], info[8], info[9], info[10], info[11])
        print drink.name


# Retrieves the properties of the drinks and returns them in a list.
def getInfo(drink):
    properties = ["name", "descriptionPlain", "color", "skill", "isAlcoholic",
    "isCarbonated", "isHot", "ingredients", "tastes", "occasions", "tools",
    "actions"]
    info = []

    for drinkProperty in properties:
        propertyValue = drink.get(drinkProperty)
        if isinstance(propertyValue, list):
            propertyValue = jsonToArray(propertyValue)
        if isinstance(propertyValue, dict):
            propertyValue = propertyValue.get("name")
        info.append(propertyValue)
    return info


# Converts a JSON array into an array that only holds the text values.
def jsonToArray(jsonArray):
    array = []
    for element in jsonArray:
        string = element.get("text")
        string = string.replace("[", "")
        string = string.replace("]", "")
        array.append(string)
    return array


if __name__ == "__main__":
    nextUrl = ""
    firstScrape = True

    while True:
        data = scrapePage(nextUrl, firstScrape)
        if data:
            createDatabase(data)
            nextUrl = data.get("next")
            if nextUrl:
                nextUrl = nextUrl.replace("pageSize=25", "pageSize=1000")
            firstScrape = False
        else:
            break
