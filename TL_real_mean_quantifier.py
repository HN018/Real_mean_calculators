import pandas as pd
import numpy as np

# 1. Load the data, telling pandas to ignore the ImageJ row numbers
file_path = r'C:\Users\------\Desktop\quant.csv'
# If your CSV does NOT have row numbers, remove index_col=0
df = pd.read_csv(file_path, index_col=0) 

# 2. Identify columns by index safely
area_col = df.columns[0]
mean_col = df.columns[1]
slice_col = df.columns[2]

# 3. Calculate Weighted Mean grouping by the Slice column
df['total_intensity'] = df[area_col] * df[mean_col]
grouped = df.groupby(slice_col).agg({
    'total_intensity': 'sum',
    area_col: 'sum'
})

# 4. Final calculation with protection against blank frames (ZeroDivision)
# Uses np.where to output 0 (or you can use np.nan) if area is 0
grouped['Mean_Intensity'] = np.where(
    grouped[area_col] > 0, 
    grouped['total_intensity'] / grouped[area_col], 
    0
)

# 5. Print ONLY the mean column
print(grouped['Mean_Intensity'].to_string(index=False))
