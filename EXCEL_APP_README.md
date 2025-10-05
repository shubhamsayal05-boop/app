# Excel-like Spreadsheet Application

## Overview

This project aims to build a full-featured Excel-like spreadsheet application with 100% parity with Microsoft Excel. Development is being done incrementally, implementing features sheet by sheet.

## Quick Start

### Installation

```bash
# Install required dependencies
pip install dash dash-bootstrap-components
```

### Running the Application

```bash
python excel_app.py
```

Then open your browser to: http://127.0.0.1:8050

## Current Features (Phase 1)

### ✅ Implemented

1. **Basic Spreadsheet Grid**
   - 100 rows × 26 columns (A-Z)
   - Cell editing by clicking
   - Real-time value updates
   - Fixed header row for easy navigation

2. **Cell Value Storage**
   - Automatic storage of cell values
   - Clear sheet functionality
   - Data persistence during session

3. **Simple Formulas**
   - **Arithmetic Operations**: `=10+20`, `=A1*2`, `=B1/A1`
   - **Cell References**: `=A1+B1`, `=C3*D4`
   - **SUM Function**: `=SUM(A1:A10)` - Sum a range of cells
   - **AVERAGE Function**: `=AVERAGE(B1:B5)` - Average a range of cells
   - **Formula Chaining**: Formulas can reference other cells with formulas

4. **User Interface**
   - Clean, Excel-like interface
   - Formula bar for editing
   - Toolbar with quick actions
   - Status bar with feedback
   - Sample data button for testing

### Examples

Try these formulas in the spreadsheet:

```
Cell A1: 10
Cell A2: 20
Cell A3: 30
Cell B1: =A1*2          → Result: 20
Cell B2: =A2*2          → Result: 40
Cell C1: =A1+B1         → Result: 30
Cell C2: =SUM(A1:A3)    → Result: 60
Cell C3: =AVERAGE(A1:A3) → Result: 20
```

## Development Roadmap

### Phase 1: Core Spreadsheet Engine ✅ (Current)
- [x] Basic spreadsheet grid with cell editing
- [x] Cell value storage and retrieval
- [x] Simple formula evaluation (SUM, AVERAGE, basic arithmetic)
- [x] Basic UI with sheet tabs
- [x] Cell selection and navigation

### Phase 2: Formula Engine Enhancement (Next)
- [ ] More Excel functions (IF, COUNT, MIN, MAX, ROUND)
- [ ] VLOOKUP and HLOOKUP functions
- [ ] Logical functions (AND, OR, NOT)
- [ ] Text functions (CONCATENATE, LEFT, RIGHT, MID)
- [ ] Date/Time functions (TODAY, NOW, DATE)
- [ ] Enhanced error handling with Excel-like error messages
- [ ] Circular reference detection
- [ ] Dependency graph for efficient recalculation

### Phase 3: Formatting Features
- [ ] Font styling (bold, italic, underline)
- [ ] Font size and family
- [ ] Text color and background color
- [ ] Cell borders (all sides, styles)
- [ ] Number formatting (currency, percentage, date, scientific)
- [ ] Cell alignment (left, center, right, justify)
- [ ] Text wrapping
- [ ] Conditional formatting

### Phase 4: Advanced Spreadsheet Features
- [ ] Multiple worksheet support (Sheet1, Sheet2, etc.)
- [ ] Copy/Paste functionality
- [ ] Cut/Copy/Paste with formats
- [ ] Undo/Redo stack
- [ ] Row operations (insert, delete, hide, resize)
- [ ] Column operations (insert, delete, hide, resize)
- [ ] Freeze panes (rows and columns)
- [ ] Split panes
- [ ] Cell merging
- [ ] Find and replace

### Phase 5: Data Operations
- [ ] Sorting (single and multi-column)
- [ ] Filtering (auto-filter)
- [ ] Advanced filtering
- [ ] Data validation (dropdowns, numeric ranges)
- [ ] Remove duplicates
- [ ] Text-to-columns
- [ ] Flash Fill

### Phase 6: Charts and Visualization
- [ ] Column charts
- [ ] Bar charts
- [ ] Line charts
- [ ] Pie charts
- [ ] Scatter plots
- [ ] Area charts
- [ ] Chart customization (titles, legends, colors)
- [ ] Chart data binding

### Phase 7: Pivot Tables and Analysis
- [ ] Pivot table creation
- [ ] Pivot table configuration
- [ ] Grouping and aggregation
- [ ] Calculated fields
- [ ] Pivot charts

### Phase 8: File Operations
- [ ] Import Excel files (.xlsx, .xls)
- [ ] Export to Excel (.xlsx)
- [ ] Import/Export CSV
- [ ] Import/Export TSV
- [ ] Native JSON format save/load
- [ ] Auto-save functionality
- [ ] Template support

### Phase 9: Collaboration Features
- [ ] Comments and notes
- [ ] Cell locking
- [ ] Sheet protection
- [ ] Workbook protection
- [ ] Track changes
- [ ] Share and collaborate (multi-user)
- [ ] Version history

### Phase 10: Advanced Excel Parity
- [ ] Macros (VBA-like scripting)
- [ ] Custom functions
- [ ] Sparklines
- [ ] Slicers
- [ ] Power Query equivalent
- [ ] What-if analysis (Goal Seek, Scenarios)
- [ ] Solver functionality
- [ ] Named ranges
- [ ] Array formulas

## Architecture

### Technology Stack
- **Frontend Framework**: Dash (Plotly)
- **UI Components**: Dash Bootstrap Components
- **Language**: Python 3.x
- **Data Structure**: JSON-based cell storage

### Key Components

1. **FormulaEvaluator**: Handles formula parsing and evaluation
2. **Cell Data Store**: Maintains spreadsheet state
3. **Spreadsheet Table**: Interactive grid component
4. **Callback System**: Handles user interactions and updates

### Data Structure

Cell data is stored in a dictionary format:

```python
{
    "A1": {"value": "10"},
    "B1": {"value": "=A1*2"},
    "C1": {"value": "=SUM(A1:A10)"}
}
```

## Testing

### Manual Testing Checklist (Phase 1)

- [ ] Cell editing works by clicking and typing
- [ ] Numbers are stored correctly
- [ ] Text values are stored correctly
- [ ] Simple arithmetic formulas work (=10+20)
- [ ] Cell references work (=A1+B1)
- [ ] SUM function works with ranges
- [ ] AVERAGE function works with ranges
- [ ] Formulas update when referenced cells change
- [ ] Clear sheet button works
- [ ] Sample data button loads correctly
- [ ] Export functionality works

### Future Testing

Unit tests and integration tests will be added in Phase 2 for:
- Formula evaluation
- Cell reference resolution
- Range operations
- Error handling

## Contributing

### Development Guidelines

1. **Incremental Development**: Add features one at a time
2. **Test Coverage**: Add tests for new features
3. **Documentation**: Update README with new features
4. **Excel Compatibility**: Match Excel behavior exactly
5. **Performance**: Optimize for large spreadsheets (1M+ cells)

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings for functions
- Keep functions focused and small

## Known Limitations (Phase 1)

1. No persistent storage (data lost on refresh)
2. Limited to 100 rows × 26 columns
3. Only basic functions (SUM, AVERAGE)
4. No formatting options
5. No copy/paste
6. No undo/redo
7. Single sheet only

These limitations will be addressed in future phases.

## Performance Considerations

- Current implementation handles up to ~2,600 cells efficiently
- Formula recalculation is done on-demand
- Future optimization needed for large datasets (Phase 4+)

## License

[To be determined]

## Changelog

### Version 0.1.0 (Phase 1) - Current
- Initial release with basic spreadsheet functionality
- Cell editing and value storage
- Simple formulas: arithmetic, SUM, AVERAGE
- Basic UI with toolbar and status bar

---

**Last Updated**: 2024
**Current Phase**: Phase 1 - Core Spreadsheet Engine
**Next Milestone**: Phase 2 - Enhanced Formula Engine
