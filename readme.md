# ManaBox CSV Converter

This script converts a [ManaBox](https://manabox.app/) text decklist into a CSV. It fetches card data from [Scryfall](https://scryfall.com/) via [Scrython](https://github.com/NandaScott/Scrython) and outputs a structured CSV including set info, rarity, and pricing.

---

## Project Structure

The recommended directory layout:

```
.
├── manaboxCSV.py
└── decks/
    ├── input/
    │   └── example.txt
    └── output/
        └── example.csv
```

- `decks/input/` → place your decklist `.txt` files here  
- `decks/output/` → generated CSV files will go here  

---

## Requirements

- Python 3.x
- `scrython`

Install dependency:

```
pip install scrython
```

---

## Usage

Basic command:

```
python manaboxCSV.py <input.txt> [output.csv]
```
---

## Input Format

The input file is assumed to be imported via scan from the ManaBox app; each line should look like this:

```
<quantity> <card name> (<set code>) <collector number>
```

### Example:

```
1 Sol Ring (cmm) 123
2 Counterspell (mh2) 45
1 Lightning Bolt (lea) 150
```

Rules:
- Blank lines are ignored
- Lines starting with `[` or `//` are ignored
---

## Output

The script generates a CSV with the following columns:

```
Name, Set code, Set name, Collector number, Foil, Rarity,
Quantity, ManaBox ID, Scryfall ID, Purchase price,
Misprint, Altered, Condition, Language, Purchase price currency
```

- Output is ready for import into ManaBox
- Prices are pulled from Scryfall (USD when available)

---

## Notes

### Rate Limiting

The script includes a built-in delay between API requests to comply with Scryfall’s rate limits.

- Default: **0.5 seconds per request**
- This keeps usage well below Scryfall’s limit

---

## Tips

- Keep one `.txt` file per deck in `decks/input/`
- Name outputs consistently (e.g., `deckname.csv`)
- Use git to track changes to your CSVs over time

---

## Example Workflow

```
# Add a new deck
cp mydeck.txt decks/input/

# Convert to CSV
python manaboxCSV.py decks/input/mydeck.txt decks/output/mydeck.csv

# Import into ManaBox
# (use the generated CSV)
```

---
