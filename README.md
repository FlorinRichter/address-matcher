# Address Matcher

A Python tool to find the best matching addresses between two CSV files using fuzzy string matching.

## Requirements

- Python 3.7+
- pandas
- rapidfuzz

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

The tool expects two CSV files with the following columns:
- QuoteIDs
- InsurableEntity-IDs
- address

Run the tool from command line:
```bash
python address_matcher.py input1.csv input2.csv output.csv [--min-score 70]
```

Arguments:
- `input1.csv`: First CSV file containing addresses to match from
- `input2.csv`: Second CSV file containing addresses to match against
- `output.csv`: Output file path for results
- `--min-score`: Optional minimum matching score (0-100, default: 70)

## Output

The tool generates a CSV file with the following columns:
- Source_QuoteID: QuoteID from the first CSV
- Source_IE_ID: InsurableEntity-ID from the first CSV
- Source_Address: Original address from the first CSV
- Matched_IE_ID: Best matching InsurableEntity-ID from the second CSV
- Match_Score: Fuzzy matching score (0-100)
- Matched_Address: Matching address from the second CSV
