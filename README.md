# Poweramp EQ Converter

Convert standard EQ `.txt` preset files into Poweramp-compatible `.json` presets.

## Features

* Converts EQ text files into Poweramp JSON format
* Supports multiple filter types:

  * Low Pass (`LP`)
  * High Pass (`HP`)
  * Band Pass (`BP`)
  * Peaking (`PK`)
  * Low Shelf (`LS`)
  * High Shelf (`HS`)
* Supports wildcard file selection (`*.txt`)
* Automatically processes all `.txt` files if no file is specified
* Preserves:

  * Frequency
  * Gain
  * Q values
  * Preamp settings

---

## Requirements

* Python 3.7+

No external dependencies required.

---

## Usage

### Convert all `.txt` files in the current folder

```bash
python poweramp_eq.py
```

---

### Convert a specific file

```bash
python poweramp_eq.py preset.txt
```

---

### Convert multiple files

```bash
python poweramp_eq.py preset1.txt preset2.txt
```

---

### Convert using wildcards

#### Linux / macOS

```bash
python poweramp_eq.py *.txt
```

#### Windows

```bash
python poweramp_eq.py "*.txt"
```

---

## Input File Format

Example:

```txt
Preamp: -6 dB

Filter 1: ON PK Fc 100 Hz Gain 3 dB Q 1.41
Filter 2: ON LS Fc 60 Hz Gain 5 dB Q 0.71
Filter 3: ON HS Fc 12000 Hz Gain -2 dB Q 1.00
```

---

## Output

For every input file:

```txt
preset.txt
```

the script creates:

```txt
preset_Poweramp.json
```

---

## Supported Filter Types

| Filter     | Aliases           |
| ---------- | ----------------- |
| Low Pass   | `LP`, `LOW`       |
| High Pass  | `HP`, `HIGH`      |
| Band Pass  | `BP`, `BAND`      |
| Peaking    | `PK`, `PEAKING`   |
| Low Shelf  | `LS`, `LOWSHELF`  |
| High Shelf | `HS`, `HIGHSHELF` |

---

## Example

### Command

```bash
python poweramp_eq.py my_eq.txt
```

### Result

```txt
Created: my_eq_Poweramp.json
```

---

## Notes

* Invalid or malformed filter lines are skipped automatically
* Frequencies are rounded to integers for Poweramp compatibility
* Output files are created in the same directory as the source file

