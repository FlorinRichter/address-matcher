import pandas as pd
from rapidfuzz import fuzz
from typing import Tuple

def find_best_match(address: str, comparison_addresses: pd.Series) -> Tuple[int, float]:
    """
    Find the best matching address from a series of comparison addresses.
    
    Args:
        address: The address to find a match for
        comparison_addresses: Series of addresses to compare against
    
    Returns:
        Tuple of (index of best match, similarity score)
    """
    scores = comparison_addresses.apply(lambda x: fuzz.ratio(address, x))
    best_match_idx = scores.argmax()
    return best_match_idx, scores[best_match_idx]

def match_addresses(csv1_path: str, csv2_path: str, output_path: str, 
                   min_similarity: float = 80.0) -> None:
    """
    Match addresses between two CSV files and output the results.
    
    Args:
        csv1_path: Path to first CSV file
        csv2_path: Path to second CSV file
        output_path: Path where to save the results
        min_similarity: Minimum similarity score to consider a match (0-100)
    """
    # Read the CSV files
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)
    
    # Initialize results list
    matches = []
    
    # Find best matches for each address in df1
    for idx1, row1 in df1.iterrows():
        best_match_idx, similarity = find_best_match(row1['Address'], df2['Address'])
        
        matches.append({
            'QuoteID_1': row1['QuoteID'],
            'IE_ID_1': row1['InsurableEntity-ID'],
            'Address_1': row1['Address'],
            'QuoteID_2': df2.iloc[best_match_idx]['QuoteID'],
            'IE_ID_2': df2.iloc[best_match_idx]['InsurableEntity-ID'],
            'Address_2': df2.iloc[best_match_idx]['Address'],
            'Similarity': similarity
        })
    
    # Create results DataFrame
    results_df = pd.DataFrame(matches)
    
    # Filter by minimum similarity if specified
    results_df = results_df[results_df['Similarity'] >= min_similarity]
    
    # Sort by similarity score in descending order
    results_df = results_df.sort_values('Similarity', ascending=False)
    
    # Save to CSV
    results_df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")
    print(f"Found {len(results_df)} matches with similarity >= {min_similarity}%")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Match addresses between two CSV files')
    parser.add_argument('csv1', help='Path to first CSV file')
    parser.add_argument('csv2', help='Path to second CSV file')
    parser.add_argument('output', help='Path to output CSV file')
    parser.add_argument('--min-similarity', type=float, default=80.0,
                      help='Minimum similarity score (0-100) to consider a match')
    
    args = parser.parse_args()
    
    match_addresses(args.csv1, args.csv2, args.output, args.min_similarity)
