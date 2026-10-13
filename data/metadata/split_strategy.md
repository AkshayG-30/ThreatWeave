# Train/Validation/Test Split Strategy

Given the dataset contains 2,390,275 rows and is highly imbalanced (96% benign, 4% attacks), we will employ the following splitting and sampling strategy for the MVP:

## 1. MVP Sampling Strategy
To create a manageable dataset (100,000 - 250,000 rows) while preserving the rarity of attacks, we will perform a **Stratified Sample** of 150,000 rows based on the `Attack` column. This ensures all attack categories are represented proportionally without overwhelming the MVP with millions of benign records.

## 2. Split Strategy (70 / 15 / 15)
The resulting 150k sample will be split into:
- **Train Set**: 70% (105,000 rows)
- **Validation Set**: 15% (22,500 rows)
- **Test Set**: 15% (22,500 rows)

## 3. Leakage Prevention
- **Split First**: The split is performed *before* any feature scaling (e.g., StandardScaler). 
- **Fit on Train Only**: Scalers will only `fit` on the Training set, and then `transform` the Validation and Test sets. This prevents data leakage where statistics from the test set influence the training transformations.
- **Stratification**: The split uses `stratify=y` to ensure the attack classes are evenly distributed across train, validation, and test splits.
- **Random Seed**: Fixed random seed (`42`) ensures reproducibility.
