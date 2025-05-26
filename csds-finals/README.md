# 🎂 Birthday Collision Detector

A simple Python program that detects the **first birthday collision** (same MM-DD) among a list of people from a CSV file. This is a practical demonstration of the **birthday paradox**.

---

## 📋 Features

- Reads a CSV file with columns: `Name` and `Birthday` (formatted as `YYYY-MM-DD`)
- Identifies the **first pair** of people who share the same birthday (MM-DD)
- Handles missing or invalid file inputs gracefully
- Explains the **pigeonhole principle** behind birthday collisions

---

## 🛠️ Requirements

- Python 3.x
- `pandas` library

Install pandas if you don't have it yet:

```bash
pip install pandas
```

---

## 📁 Input CSV Format

The CSV file should have at least the following columns:

```
Name,Birthday
Alice,1990-06-21
Bob,1985-04-12
Charlie,2000-06-21
...
```

---

## ▶️ How to Use

1. Save the script (e.g., `birthday_collision.py`)
2. Run it using Python:

```bash
python birthday_collision.py
```

3. Enter the CSV file name when prompted (e.g., `birthdays.csv`)

---

## 💡 Example Output

```
=== Birthday Collision Detector ===
Enter the CSV file name (e.g., birthdays.csv): sample_birthdays.csv
Collision detected: 'Alice' and 'Charlie' share the birthday 06-21.
```

Or if no collision is found (≤365 entries with unique dates):

```
There is no 2 person that has the same birthday. Therefore there is no collision.
```

---

## 📚 How It Works

- Converts the `Birthday` column to datetime format using `pandas`
- Extracts the `MM-DD` part for each entry
- Uses a dictionary to check if a `MM-DD` has already been seen
- Returns the first two people who share the same birthday

---

## 📄 License

This project is open source and free to use.
