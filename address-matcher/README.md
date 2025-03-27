# Address Matcher

A Python tool to find the best matching addresses between two CSV files using fuzzy string matching. Available both as a command-line tool and a web application.

## Requirements

For local development:
- Python 3.7+
- pandas
- rapidfuzz
- flask (for web interface)

OR

- Docker (for containerized usage)

## Installation & Usage

### Option 1: Local Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

### Option 2: Docker (Recommended for cross-platform use)

1. Build the Docker image:
```bash
docker build -t address-matcher .
```

2. Run the container:
```bash
docker run -p 5000:5000 address-matcher
```

3. Open your web browser and visit: http://localhost:5000

## Web Interface Usage

1. Visit the web interface in your browser
2. Upload two CSV files with the following required columns:
   - QuoteID
   - InsurableEntity-ID
   - Address
3. Set your minimum similarity score (0-100)
4. Click "Match Addresses" to get your results

## Command Line Usage

If you prefer using the command line version:

```bash
python address_matcher.py input1.csv input2.csv output.csv --min-similarity 80
```

## Output

The script generates a CSV file containing:
- QuoteID_1, IE_ID_1, Address_1 (from first file)
- QuoteID_2, IE_ID_2, Address_2 (from second file)
- Similarity score (0-100)
