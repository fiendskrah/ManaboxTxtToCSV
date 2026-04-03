import csv
import os
import sys
import time
import scrython.cards

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: python manaboxCSV.py <path to txt file> [output.csv]")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2] if len(sys.argv) >= 3 else "output.csv"

# conservative rate limiter: 0.5 seconds between requests (~2 req/sec)
REQUEST_DELAY = 0.5
RATE_LIMIT_WAIT = 60
MAX_RETRIES = 3

if not os.path.exists(input_path):
    print(f"Input file not found: {input_path}")
    sys.exit(1)

if os.path.exists(output_path):
    print(f"Output file '{output_path}' already exists. Remove it? [y/N]")
    if input().strip().lower() == 'y':
        os.remove(output_path)
    else:
        sys.exit(0)

res = []
cards = 0

def fetch_card(name, setcode, collector_id):
    query = f'!"{name}" set:{setcode} number:{collector_id}'

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            time.sleep(REQUEST_DELAY)
            return scrython.cards.Search(q=query).data()[0]

        except Exception as e:
            msg = str(e).lower()

            if "rate" in msg or "429" in msg:
                if attempt < MAX_RETRIES:
                    print(f"\nRate limited. Waiting {RATE_LIMIT_WAIT}s before retry {attempt + 1}/{MAX_RETRIES}...")
                    time.sleep(RATE_LIMIT_WAIT)
                    continue

            raise

with open(input_path, 'r') as f:
    for line in f:
        if line.strip() == "" or line.startswith("[") or line.startswith("//"):
            continue

        quant = line[0:line.find(' ')]
        n = line[line.find(' ') + 1: line.find('(') - 1]
        setcode = line[line.find('(') + 1: line.find(')')]
        collectorID = line[line.find(')') + 2: line.find(' ', line.find(')') + 2)]
        foil = line.strip().endswith("*F*")

        try:
            card = fetch_card(n, setcode, collectorID)
        except Exception as e:
            print(f"\nError fetching card: {n} ({setcode} #{collectorID})")
            print(e)
            continue
        
        price = ""
        if foil:
            price = card["prices"].get("usd_foil") or card["prices"].get("usd") or ""
        else:
            price = card["prices"].get("usd") or ""
    
            res.append([
                card["name"],
                card["set"],
                card["set_name"],
                card["collector_number"],
                "foil" if foil else "normal",
                card["rarity"],
                quant,
                "",
                card["id"],
                price,
                "false",
                "false",
                "near_mint",
                "en",
                "USD"
            ])
           
        cards += int(quant)
        print("\x1b[2K", end="")
        print(f"Processed {cards} cards. {card['name']}", end="\r")

with open(output_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Name", "Set code", "Set name", "Collector number", "Foil",
        "Rarity", "Quantity", "ManaBox ID", "Scryfall ID",
        "Purchase price", "Misprint", "Altered", "Condition",
        "Language", "Purchase price currency"
    ])
    writer.writerows(res)

print(f"\nSuccessfully processed {cards} cards.")
print(f"Output written to {os.path.abspath(output_path)}")
