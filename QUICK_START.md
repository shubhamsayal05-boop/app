# Quick Start Guide - Excel-like Spreadsheet Application

## Installation

```bash
# Install dependencies
pip install -r requirements_excel.txt
```

## Running the Application

```bash
python excel_app.py
```

The application will start on http://127.0.0.1:8050

## Features

### Cell Editing
- Click any cell to edit
- Type a value or formula
- Press Enter or click elsewhere to save

### Basic Values
```
Cell A1: 100
Cell A2: 200
Cell A3: Hello World
```

### Formulas
Start with `=` to create a formula:

**Arithmetic**
```
=10+20          → 30
=50-25          → 25
=8*3            → 24
=100/5          → 20
=(10+5)*2       → 30
```

**Cell References**
```
If A1=10 and B1=20:
=A1+B1          → 30
=A1*B1          → 200
=B1/A1          → 2
```

**SUM Function**
```
If A1=10, A2=20, A3=30:
=SUM(A1:A3)     → 60
=SUM(A1:A10)    → Sum of all values in A1 to A10
```

**AVERAGE Function**
```
If B1=10, B2=20, B3=30, B4=40, B5=50:
=AVERAGE(B1:B5) → 30
```

**Complex Formulas**
```
If A1=10, A2=20:
=SUM(A1:A2)*2   → 60 (sum is 30, then *2)
=(A1+A2)/2      → 15 (average calculated manually)
```

## Toolbar Buttons

- **Clear Sheet**: Removes all data from the spreadsheet
- **Export JSON**: Exports cell data to console (for debugging)
- **Sample Data**: Loads example data with formulas

## Sample Data

Click "Sample Data" to see examples:
- Column A: Values (10, 20, 30, 40, 50)
- Column B: Formulas that double Column A (=A1*2, =A2*2, etc.)
- Column C: Formulas that combine values (=A1+B1, =SUM(A1:A5), =AVERAGE(A1:A5))

## Tips

1. **Formula Bar**: Shows the raw content of the selected cell (including formulas)
2. **Status Bar**: Shows feedback messages (green for success, blue for info)
3. **Formulas Update**: When you change a cell value, formulas referencing it automatically recalculate
4. **Error Messages**: If a formula has an error, it will show `#ERROR: [message]`

## Troubleshooting

### Application won't start
- Make sure dependencies are installed: `pip install -r requirements_excel.txt`
- Check Python version: Python 3.8 or higher required

### Formulas not working
- Make sure to start with `=`
- Check that cell references exist (e.g., A1, B2)
- For ranges, use format A1:A10 (colon separator)

### Port already in use
Edit `excel_app.py` and change the port:
```python
app.run(debug=True, port=8051)  # Change 8050 to 8051
```

## Next Steps

See `EXCEL_APP_README.md` for the full roadmap and upcoming features!
