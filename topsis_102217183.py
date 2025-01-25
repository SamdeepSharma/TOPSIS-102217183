import pandas as pd
import numpy as np
import sys

def read_input_file(input_file):
    """Read input file (either CSV or Excel)"""
    try:
        if input_file.endswith('.xlsx'):
            return pd.read_excel(input_file)
        elif input_file.endswith('.csv'):
            return pd.read_csv(input_file)
        else:
            raise ValueError("Input file must be either .csv or .xlsx format")
    except FileNotFoundError:
        raise FileNotFoundError("Input file not found")
    except Exception as e:
        raise Exception(f"Error reading input file: {str(e)}")

def validate_inputs(input_file, weights, impacts):
    try:
        # Read input file
        df = read_input_file(input_file)

        # Check for minimum columns
        if len(df.columns) < 3:
            raise ValueError("Input file must contain three or more columns")

        # Convert weights and impacts to lists
        weights = [float(w) for w in weights.split(',')]
        impacts = impacts.split(',')

        # Validate numeric values in columns from 2nd to last
        for col in df.columns[1:]:
            if not pd.to_numeric(df[col], errors='coerce').notnull().all():
                raise ValueError(f"Column {col} contains non-numeric values")

        # Check if number of weights equals number of numeric columns
        if len(weights) != len(df.columns[1:]):
            raise ValueError("Number of weights must equal number of columns (excluding first column)")

        # Check if number of impacts equals number of numeric columns
        if len(impacts) != len(df.columns[1:]):
            raise ValueError("Number of impacts must equal number of columns (excluding first column)")

        # Validate impacts are either + or -
        if not all(impact in ['+', '-'] for impact in impacts):
            raise ValueError("Impacts must be either '+' or '-' and separated by commas")

    except FileNotFoundError:
        raise FileNotFoundError("Input file not found")
    except Exception as e:
        raise Exception(f"Error validating inputs: {str(e)}")

    return df, weights, impacts

def calculate_topsis(df, weights, impacts):
    try:
        # Create numeric matrix excluding the first column
        numeric_matrix = df.iloc[:, 1:].values.astype(float)

        # Step 1: Normalize the matrix
        normalized_matrix = numeric_matrix / np.sqrt(np.sum(numeric_matrix**2, axis=0))

        # Step 2: Calculate weighted normalized matrix
        weights = np.array(weights)
        weighted_normalized = normalized_matrix * weights

        # Step 3: Determine ideal best and worst solutions
        ideal_best = np.zeros(len(df.columns) - 1)
        ideal_worst = np.zeros(len(df.columns) - 1)

        for i in range(len(df.columns) - 1):
            if impacts[i] == '+':
                ideal_best[i] = np.max(weighted_normalized[:, i])
                ideal_worst[i] = np.min(weighted_normalized[:, i])
            else:
                ideal_best[i] = np.min(weighted_normalized[:, i])
                ideal_worst[i] = np.max(weighted_normalized[:, i])

        # Step 4: Calculate separation measures
        s_best = np.sqrt(np.sum((weighted_normalized - ideal_best) ** 2, axis=1))
        s_worst = np.sqrt(np.sum((weighted_normalized - ideal_worst) ** 2, axis=1))

        # Step 5: Calculate TOPSIS score
        topsis_score = s_worst / (s_best + s_worst)

        # Calculate ranks
        ranks = topsis_score.argsort()[::-1].argsort() + 1

        return topsis_score, ranks
    except Exception as e:
        raise Exception(f"Error calculating TOPSIS: {str(e)}")

def main():
    try:
        # Validate command line arguments
        if len(sys.argv) != 5:
            print("Usage: python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>")
            sys.exit(1)

        input_file = sys.argv[1]
        weights = sys.argv[2]
        impacts = sys.argv[3]
        output_file = sys.argv[4]

        # Validate inputs and get processed data
        df, processed_weights, processed_impacts = validate_inputs(input_file, weights, impacts)

        # Calculate TOPSIS
        topsis_score, ranks = calculate_topsis(df, processed_weights, processed_impacts)

        # Add TOPSIS Score and Rank columns to the dataframe
        df['Topsis Score'] = topsis_score.round(4)  # Round to 4 decimal places
        df['Rank'] = ranks

        # Save results
        df.to_csv(output_file, index=False)
        print(f"Results successfully saved to {output_file}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
