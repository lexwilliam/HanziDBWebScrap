import requests
from bs4 import BeautifulSoup
import csv


# Setup for request (utf-8 encoding compatible)
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Url error"


# Decode the pinyin so database can easily search pinyin query (一: yī -> yi)
def decodePinyin(s):
    PinyinToneMark = {
        0: "a\u0101\u00e1\u01ce\u00e0",
        1: "o\u014d\u00f3\u01d2\u00f2",
        2: "e\u0113\u00e9\u011b\u00e8",
        3: "i\u012b\u00ed\u01d0\u00ec",
        4: "u\u016b\u00fa\u01d4\u00f9",
        5: "v\u01d6\u01d8\u01da\u01dc",
        6: "\u00fc\u01d6\u01d8\u01da\u01dc"
    }
    result = ""
    for c in s:
        if ord(c) > 127:
            for i in range(0, 7):
                if c in PinyinToneMark[i]:
                    result = result + PinyinToneMark[i][0]
                    break
        else:
            result = result + c
    return result


# Main program
if __name__ == "__main__":
    # The website url we want to scrape
    hankiDBUrl = "http://hanzidb.org/character-list/by-frequency"

    # Setting up csv writer
    resultFile = open("chinese_dictionary_table.csv", mode="w", encoding="UTF8")
    writer = csv.writer(resultFile)

    # Structuring the table into 3 attributes for each row
    data = [None] * 4

    for i in range(1, 101):
        # Open page from 1 to 100
        pageHtml = getHTMLText("{}?page={}".format(hankiDBUrl, i))
        # BeautifulSoup Setup
        soup = BeautifulSoup(pageHtml, 'html.parser')
        # Get all content from the table
        table = soup.find_all('tr')
        # Write all data from table into the csv file
        for tr in table[1:]:
            data[0] = tr.td.text
            print(data[0], end=" ")
            pinyin = tr.find_all('td')[1:2]
            if pinyin:
                data[1] = pinyin[0].text
                data[2] = decodePinyin(pinyin[0].text)
                print(data[1], end=" ")
            definition = tr.find_all('td')[2:3]
            if definition:
                data[3] = definition[0].text
                print(data[3])
            writer.writerow(data)
