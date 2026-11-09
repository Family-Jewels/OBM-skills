# sheetcalc specification

Build `sheetcalc`, a single-sheet spreadsheet engine in Python. It stores what a user types into cells, evaluates formulas, and keeps every value current as cells change.

- Python 3.10 or later, standard library only.
- A package named `sheetcalc` importable from the repository root (`import sheetcalc` works when the root is on `sys.path`).
- Where this spec is silent, behave as Microsoft Excel does.

## 1. API

```python
from sheetcalc import Workbook, CellError

wb = Workbook()
wb.set("A1", "5")              # store input text; "" clears the cell
wb.get("A1")                   # current value (section 2)
wb.get_raw("A1")               # input text exactly as stored ("" if empty)
wb.define_name("Rate", "$B$1") # named reference (section 9)
wb.copy("A1", "B2")            # copy one cell's input, adjusting references (section 7)
wb.insert_rows(3, 2)           # insert 2 empty rows before row 3 (section 8)
wb.delete_rows(3, 2)           # delete rows 3 and 4
wb.insert_cols("C", 1)         # insert 1 empty column before column C
wb.delete_cols("C", 1)         # delete column C
wb.to_csv()                    # computed values as CSV text (section 10)
Workbook.from_csv(text)        # new workbook whose cells are set from CSV fields
```

Cell addresses are case-insensitive (`"a1"` is `"A1"`). Columns run from `A` to `ZZ` (702 columns) and rows from 1 to 100000. Any other address passed to the API raises `ValueError`.

## 2. Values

`get` returns one of:

| Kind | Python value |
| --- | --- |
| Empty | `None` |
| Number | `float` (an `int` is also accepted) |
| Text | `str` |
| Boolean | `bool` |
| Error | a `CellError` |

`CellError(code)` has a `.code` attribute (for example `"#DIV/0!"`), and two `CellError`s are equal when their codes are equal. Codes:

| Code | Meaning |
| --- | --- |
| `#DIV/0!` | Division by zero, or `MOD` by zero, or `AVERAGE` of no numbers |
| `#VALUE!` | Wrong type, such as text that is not a number used in arithmetic |
| `#REF!` | A reference that no longer exists (sections 7 and 8) |
| `#NAME?` | Unknown function or undefined name |
| `#N/A` | `VLOOKUP` found no match |
| `#CYCLE!` | The cell is part of, or depends on, a circular reference |
| `#ERROR!` | The formula cannot be parsed |

## 3. Input

`set(address, text)` interprets `text` in this order:

1. `""` clears the cell.
2. Text starting with `=` is a formula. A formula that cannot be parsed is still stored; its value is `#ERROR!`.
3. Text starting with `'` is text; the apostrophe is dropped from the value but kept in `get_raw`.
4. Text that is a decimal number (optional sign, digits, optional decimal point, optional exponent: `5`, `-2.5`, `.5`, `1e3`) is a number. Surrounding spaces are allowed. Thousands separators and currency symbols are not numbers.
5. `TRUE` or `FALSE`, in any case, is a boolean.
6. Anything else is text, stored exactly as given.

Error codes typed as input (`#N/A`) are text, not errors.

## 4. Formulas

### 4.1 Elements

- Numbers: `1`, `2.5`, `.5`, `1e3`.
- Text in double quotes; a doubled quote inside is one quote: `"say ""hi"""`.
- `TRUE`, `FALSE` (any case).
- References: `A1`, `$A$1`, `A$1`, `$A1` (any case). Ranges: `A1:B3`, with either corner first.
- Names (section 9).
- The literal `#REF!`, which evaluates to that error.
- Function calls: `NAME(arg, ...)`, function names in any case.
- Parentheses and spaces anywhere between elements.

### 4.2 Operators, from lowest to highest precedence

| Operators | Associativity |
| --- | --- |
| `=` `<>` `<` `>` `<=` `>=` | left |
| `&` (join as text) | left |
| `+` `-` | left |
| `*` `/` | left |
| `^` | left, so `2^3^2` is 64 |
| unary `-` and `+` | binds tighter than `^`, so `-2^2` is 4 |
| `%` (postfix, divides by 100) | highest |

### 4.3 Types and coercion

- Arithmetic (`+ - * / ^`, unary minus, `%`) converts each operand to a number: numbers stay; `TRUE` is 1 and `FALSE` is 0; empty is 0; text that would be a number under section 3 rule 4 is that number; any other text gives `#VALUE!`.
- `&` converts each operand to text: empty is `""`; booleans are `TRUE` and `FALSE`; numbers use `format(x, ".15g")`, so `0.1+0.2` joins as `0.3` and `3` joins as `3`.
- Comparisons:
  - Numbers compare numerically, booleans compare `FALSE < TRUE`.
  - **Text compares case-insensitively**: `="apple"="Apple"` is `TRUE` and `="a"<"B"` is `TRUE`.
  - Across types, every number is less than every text, and every text is less than every boolean. So `=1="1"` is `FALSE`, and `=2<"a"` is `TRUE`.
  - Empty acts as `0` when compared with a number, `""` with text, and `FALSE` with a boolean.
- A formula that is a bare reference to an empty cell (`=A1`) has value `0`.
- A range used where a single value is needed (`=A1:A3+1`) gives `#VALUE!`.

### 4.4 Errors

An error in an operand makes the result that error, and this is checked before any type conversion, so `="x"+1/0` is `#DIV/0!`. When both operands of an operator are errors, the left one wins. A function returns the first error it meets among its arguments, reading arguments left to right and ranges row by row, except where section 5 says otherwise.

## 5. Functions

An unknown function gives `#NAME?`. A known function with the wrong number of arguments gives `#VALUE!`.

**Aggregates.** `SUM`, `AVERAGE`, `MIN`, `MAX`, `COUNT` take one or more arguments, each a value or a range.

- Inside ranges, only numbers count; text, booleans and empty cells are skipped. Errors in ranges still propagate.
- A direct argument (not a range) is converted with the arithmetic rule: `=SUM("3", TRUE)` is 4, and `=SUM("x")` is `#VALUE!`. A reference to a single cell (`A1`) is a range for this purpose.
- `COUNT` counts numbers in ranges, and direct arguments that convert to a number. It skips everything else, errors included, and never returns an error.
- `AVERAGE` of no numbers is `#DIV/0!`. `MIN` and `MAX` of no numbers are 0.

`COUNTA(...)` counts non-empty values, including errors, and never propagates an error.

**Logic.**

- `IF(cond, then, [else])` evaluates only the branch it picks; `else` defaults to `FALSE`. `cond` is converted to a boolean: numbers are `TRUE` unless 0, `"TRUE"`/`"FALSE"` text (any case) converts, other text is `#VALUE!`.
- `AND(...)`, `OR(...)` take values or ranges; within ranges, text and empty are skipped. If nothing remains, `#VALUE!`.
- `NOT(x)`.
- `IFERROR(x, alt)`: `alt` if `x` is any error, otherwise `x`.

**Math.**

- `ABS(x)`.
- `INT(x)` rounds down toward negative infinity.
- `MOD(n, d)` takes the sign of `d`, as `n - d*INT(n/d)`.
- `ROUND(x, digits)` rounds half away from zero, on the number's shortest decimal form (`repr`), so `ROUND(2.5, 0)` is 3, `ROUND(-2.5, 0)` is -3 and `ROUND(2.675, 2)` is 2.68. `digits` may be negative: `ROUND(1234, -2)` is 1200. `digits` is truncated to an integer.

**Text.** Arguments are converted with the `&` rule. Numeric arguments are truncated to integers.

- `LEN(t)`, `UPPER(t)`, `LOWER(t)`.
- `TRIM(t)` removes leading and trailing spaces and turns runs of inner spaces into one.
- `CONCAT(...)` joins any number of values or ranges (ranges row by row, empty cells as `""`).
- `LEFT(t, [n])` and `RIGHT(t, [n])`: `n` defaults to 1. A negative `n` gives `#VALUE!`.
- `MID(t, start, n)`: `start` counts from 1. `start` < 1 or `n` < 0 gives `#VALUE!`.

**Lookup and conditional.**

- `VLOOKUP(value, range, col)` finds the first row whose first-column cell equals `value` (exact match, text case-insensitive, using the comparison rules in 4.3) and returns that row's cell in column `col` (1 is the first column). Empty cells in the first column never match. No match gives `#N/A`. `col` < 1 or wider than the range gives `#REF!`.
- `COUNTIF(range, criterion)` and `SUMIF(range, criterion, [sum_range])`. A criterion is either:
  - a number or boolean, which matches cells equal to it; or
  - text, optionally starting with `=`, `<>`, `<`, `>`, `<=` or `>=` followed by an operand. If the operand is a number under section 3 rule 4, numeric cells are compared with it; otherwise text cells are compared with it case-insensitively. A `<>` criterion matches every cell the matching `=` criterion would not, including empty cells, errors and cells of other types. A plain criterion with no operator means `=`.
  - `sum_range` defaults to `range`. It is aligned to `range` by position from its top-left cell; only numbers in it are added. Errors in `range` never propagate in `COUNTIF` or `SUMIF`.

## 6. Circular references, recalculation and scale

- Every cell in a cycle, including a cell that refers to itself, has value `#CYCLE!`. Cells that depend on a cycle get `#CYCLE!` through normal error propagation. Breaking the cycle restores normal values.
- `get` always reflects every `set` made before it.
- Chains of at least 10,000 cells that depend on each other (`A2` is `=A1+1`, `A3` is `=A2+1`, ...) must work without errors.
- Changing a cell must not recompute cells that do not depend on it. Concretely, on a workbook with 10,000 formula cells, 1,000 rounds of setting one cell and reading a cell that depends on it must take under one second in total, as long as only a few cells depend on the one being set.

## 7. Copying cells

`copy(src, dst)` sets `dst` to `src`'s input, with each relative part of each reference shifted by the offset from `src` to `dst`. `$` parts do not move. A reference that would move off the sheet (before column A or row 1, or past the limits) becomes `#REF!`; for a range, the whole range becomes `#REF!`.

Only references change; every other character of the input, including spacing, case, function names and text inside quotes, stays exactly as typed. A reference that changes is written in upper case; one that does not change stays as typed. Names do not move.

```
B1 holds  =A1+$C$1*sum(D1:D3)&"A1"
copy("B1", "C3") stores  =B3+$C$1*sum(E3:E5)&"A1"
```

## 8. Inserting and deleting rows and columns

These change the sheet and rewrite every reference in every formula and every name, `$` parts included, so that each still points at the same cell. As in section 7, only references in the text change.

- **Insert** `count` rows before row `r`: cells at row `r` and below move down. A range grows when the insertion falls strictly inside it (start row < `r` <= end row). Inserting at a range's first row moves the whole range; inserting just past its last row leaves it unchanged.
- **Delete** `count` rows from row `r`: those cells are removed and cells below move up. A reference to a removed cell becomes `#REF!`. A range keeps the surviving rows between its corners; if no rows survive, the whole range becomes `#REF!`.
- Columns work the same way. Column arguments are letters (`"C"`).
- Cells that would move past the sheet's limits are dropped.
- A row or column argument outside the sheet, or a `count` below 1, raises `ValueError`.

```
A1 holds =SUM(B2:B10)+B5+C1
delete_rows(4, 2) stores =SUM(B2:B8)+#REF!+C1
```

## 9. Names

`define_name(name, ref)` sets a workbook-wide name for a cell or range reference, such as `"$B$1"` or `"A1:A10"`. Names are case-insensitive, start with a letter or underscore, contain only letters, digits and underscores, and must not look like a cell reference (`AB12`) or be `TRUE` or `FALSE`. An invalid name or reference raises `ValueError`. Redefining a name replaces it. An undefined name in a formula gives `#NAME?`. Formulas that use a name update when the name is defined or redefined.

## 10. CSV

`to_csv()` returns the computed values of the rectangle from `A1` to the last used row and column, as CSV text: fields quoted only when needed (as Python's `csv` module does with its defaults), rows ending in `\n`. Empty cells are empty fields; numbers use `format(x, ".15g")`; booleans are `TRUE` and `FALSE`; errors are their codes. An empty workbook gives `""`.

`Workbook.from_csv(text)` returns a new workbook where field *j* of line *i* is `set` into the cell at column *j*, row *i*, so `=` fields become formulas.
