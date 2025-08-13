import csv
import os
import re
from turtle import st
import scrython
import scrython.cards
import sys

if (sys.argv.__len__() < 2):
    print("Usage: python manaboxCSV.py <path to txt file>")
    sys.exit(1)
    
if os.path.exists("output.csv"):
    print("Output file 'output.csv' already exists. Remove output.csv? [y,N]")
    if input().strip().lower() == 'y':
        os.remove("output.csv")
    else:
        sys.exit(0)

f = open(sys.argv[1], 'r')
res = []
lines = 0
cards = 0

for line in f:
    if line.strip() == "" or line.startswith("[") or line.startswith("//"):
        continue 

    quant = line[0 : line.find(' ')]

    n = line[line.find(' ') + 1 : line.find('(')-1]
    setcode = line[line.find('(') + 1 : line.find(')')]
    collectorID = line[line.find(')') + 2 : line.find(' ', line.find(')') + 2)]
    foil = line.strip().endswith("*F*")

    try:
        card = scrython.cards.Search(q=f'!"{n}" set:{setcode} number:{collectorID}').data()[0]
    except Exception as e:
        print(f"Error fetching card: {n} from set {setcode} with collector ID {collectorID}")
        print(e)
        continue

    res.append([card["name"], card["set"], card["set_name"], card["collector_number"], "foil" if foil else "normal", card["rarity"], quant, "", card["id"], "0", "false", "false", "near_mint", "en", "USD"])
    cards += int(quant)
    print("\x1b[2K", end='')
    print(f"Processed {cards} cards. {card["name"]}", end='\r')

if os.path.exists("output.csv"):
    os.remove("output.csv")

with open("output.csv", mode="x") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Set code", "Set name", "Collector number", "Foil", "Rarity", "Quantity", "ManaBox ID", "Scryfall ID", "Purchase price", "Misprint", "Altered", "Condition", "Language", "Purchase price currency"])
    writer.writerows(res)

print(f"Successfully processed {cards} cards, output written to {os.path.abspath('output.csv')}")