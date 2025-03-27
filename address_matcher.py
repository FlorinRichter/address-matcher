import pandas as pd
from rapidfuzz import fuzz, process
import argparse
from typing import Tuple

def load_csv(file_path: str) -> pd.DataFrame:
    """Load CSV file and validate required columns."""
    df = pd.read_csv(file_path, sep=';', encoding='iso-8859-1')
    required_columns = {'submissionBaseNr', 'submissionId', 'insurableEntityId', 'address'}
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV must contain columns: {required_columns}")
    return df

def find_best_matches(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """Find best address matches between two dataframes using fuzzy matching."""
    # Create a dictionary of addresses from df2 for faster lookup
    df2_by_baseNr = df2.groupby('submissionBaseNr').apply(lambda x: dict(zip(x.index, x['address']))).to_dict()
    
    # Function to find best match for each address
    def find_match(row) -> Tuple[str, float, int]:
        baseNr = row['submissionBaseNr']
        address = row['address']

        #Only compare addresses with the same submissionBaseNr
        if baseNr not in df2_by_baseNr:
            return None, 0, -1

        df2_addresses = df2_by_baseNr[baseNr]
        if not df2_addresses:
            return None, 0, -1

        match = process.extractOne(
            address,
            df2_addresses,
            scorer=fuzz.token_sort_ratio
        )
        if match:
            matched_idx, score = match[2], match[1]
            return df2.loc[matched_idx, 'insurableEntityId'], score, matched_idx
        return None, 0, -1

    # Apply matching to each row in df1
    results = [find_match(row) for _, row in df1.iterrows()]
    
    # Create result DataFrame
    result_df = pd.DataFrame({
        'Source_QuoteID': df1['submissionBaseNr'],
        'Source_IE_ID': df1['insurableEntityId'],
        'Source_Address': df1['address'],
        'Matched_IE_ID': [r[0] for r in results],
        'Match_Score': [r[1] for r in results],
        'Matched_Address': [df2.loc[r[2], 'address'] if r[2] >= 0 else None for r in results]
    })
    
    return result_df

def main():
    parser = argparse.ArgumentParser(description='Match addresses between two CSV files')
    parser.add_argument('csv1', help='Path to first CSV file')
    parser.add_argument('csv2', help='Path to second CSV file')
    parser.add_argument('output', help='Path to output CSV file')
    parser.add_argument('--min-score', type=float, default=90,
                       help='Minimum matching score (0-100)')
    
    args = parser.parse_args()
    
    try:
        # Load CSV files
        df1 = load_csv(args.csv1)
        df2 = load_csv(args.csv2)
        
        # Find matches
        results = find_best_matches(df1, df2)
        
        # Filter by minimum score if specified
        if args.min_score > 0:
            results = results[results['Match_Score'] >= args.min_score]
        
        # Save results
        results.to_csv(args.output, index=False)
        print(f"Successfully processed {len(df1)} addresses")
        print(f"Found {len(results)} matches with score >= {args.min_score}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
