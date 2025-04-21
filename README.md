# Mini Excel

Mini Excel is a small spreadsheet application written in Python with Tkinter. It lets you enter values and formulas, format cells, and save or load your work from a text file.

## Features

- Grid of editable cells displayed in a Tkinter window.
- Live recalculation: when you change a cell, any dependent formulas update automatically.
- Supported formulas:
  * `SUM`, `AVG`, `MIN`, `MAX` for ranges such as `A1:A5` or for comma‑separated cells such as `A1,B2,B3`.
  * `MATH()` for arithmetic expressions that mix numbers and cell references, for example `MATH(A1+2*B3)`.
- Cell formatting: change background colour and font from the toolbar.
- Save the current sheet to a text file and load it later.

## Quick start

```bash
git clone https://github.com/<your-user>/mini_excel.git
cd mini_excel
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Basic use

| Task                 | Steps                                                         |
|----------------------|---------------------------------------------------------------|
| Edit a cell          | Click a cell, type text or a formula, press **Enter**.        |
| Move between cells   | Use **Tab** or **Shift+Tab**.                                 |
| Change colour/font   | Select a colour or font from the toolbar drop‑downs.          |
| Save a sheet         | Click *Save File* and choose a location.                      |
| Load a sheet         | Click *Load File* and pick a previously saved file.           |

## Requirements

- Python 3.9 or newer
- `tkinter` (included with the standard Python installer)
- `ttkthemes` (installed automatically from *requirements.txt*)

