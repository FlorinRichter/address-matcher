from flask import Flask, render_template, request, send_file
import pandas as pd
from rapidfuzz import fuzz
from typing import Tuple
import os
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def find_best_match(address: str, comparison_addresses: pd.Series) -> Tuple[int, float]:
    scores = comparison_addresses.apply(lambda x: fuzz.ratio(address, x))
    best_match_idx = scores.argmax()
    return best_match_idx, scores[best_match_idx]

def match_addresses(df1: pd.DataFrame, df2: pd.DataFrame, min_similarity: float = 80.0) -> pd.DataFrame:
    matches = []
    
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
    
    results_df = pd.DataFrame(matches)
    results_df = results_df[results_df['Similarity'] >= min_similarity]
    results_df = results_df.sort_values('Similarity', ascending=False)
    
    return results_df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match():
    if 'file1' not in request.files or 'file2' not in request.files:
        return 'No files uploaded', 400
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    min_similarity = float(request.form.get('min_similarity', 80.0))
    
    if file1.filename == '' or file2.filename == '':
        return 'No files selected', 400
    
    try:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        
        # Validate required columns
        required_columns = ['QuoteID', 'InsurableEntity-ID', 'Address']
        if not all(col in df1.columns for col in required_columns) or \
           not all(col in df2.columns for col in required_columns):
            return 'CSV files must contain columns: QuoteID, InsurableEntity-ID, Address', 400
        
        results_df = match_addresses(df1, df2, min_similarity)
        
        # Create in-memory buffer for CSV
        output = io.StringIO()
        results_df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='address_matches.csv'
        )
        
    except Exception as e:
        return f'Error processing files: {str(e)}', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
