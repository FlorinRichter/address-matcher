# Address Matcher

A Python tool to find the best matching addresses between two CSV files using fuzzy string matching.

## Requirements

- Python 3.7+
- pandas
- rapidfuzz

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

The script expects two input CSV files with the following columns:
- QuoteID
- InsurableEntity-ID
- Address

To run the script:

```bash
python address_matcher.py input1.csv input2.csv output.csv [--min-similarity SCORE]
```

Arguments:
- `input1.csv`: First CSV file
- `input2.csv`: Second CSV file to match against
- `output.csv`: Where to save the results
- `--min-similarity`: Optional minimum similarity score (0-100) to consider a match (default: 80.0)

## Output

The script generates a CSV file containing:
- QuoteID_1, IE_ID_1, Address_1 (from first file)
- QuoteID_2, IE_ID_2, Address_2 (from second file)
- Similarity score (0-100)
