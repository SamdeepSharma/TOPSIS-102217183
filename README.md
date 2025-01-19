# Topsis-Samdeep-102217183

A Python package to implement the TOPSIS method for multi-criteria decision-making. TOPSIS ranks alternatives based on their similarity to the ideal solution and distance from the worst-case scenario. It simplifies complex decision analysis by evaluating multiple criteria and providing a clear ranking, making it an effective tool for informed and objective decision-making in various fields.

## Installation

```bash
pip install Topsis-Samdeep-102217183
```

## Usage

The package can be used through command line:

```bash
topsis <InputDataFile> <Weights> <Impacts> <ResultFileName>
```

### Example

```bash
topsis data.xlsx "1,1,1,1,1" "+,+,+,+,+" output.csv
```

### Input Format
* Input File:
    * The file can be in CSV or Excel format (.csv or .xlsx).
    * The first column should contain the names of the objects/variables.
    * The remaining columns must contain numeric values only (criteria values).
### Parameters
1. <InputDataFile>: The input file name along with its path (e.g., data.csv or data.xlsx).
2. <Weights>: A comma-separated string of numeric weight values for each criterion (e.g., "1,1,1,1").
3. <Impacts>: A comma-separated string of + or - symbols, indicating whether the criterion is beneficial (+) or non-beneficial   (-) (e.g., "+,+,-,+").
4. <ResultFileName>: The desired output file name including its path (e.g., output.csv).

### Output
The output file (CSV format) will include:

All input data columns
Additional columns:
TOPSIS Score: The calculated score for each alternative.
Rank: The rank of each alternative based on the TOPSIS score (higher score = better rank).

## License
MIT License

## Author
Samdeep Sharma
Roll Number: 102217183

If you have any questions or suggestions, feel free to reach out!
