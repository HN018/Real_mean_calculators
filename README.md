# Quantitative Microscopy: Automated Intensity Extraction

## Overview
This repository contains Python data processing pipelines designed to automate the extraction and quantification of fluorescence microscopy data. 

When analyzing subcellular compartments (e.g., lysosomes, lipid droplets), image analysis software (like ImageJ) often outputs data for hundreds of individual segmented puncta per cell. To perform rigorous statistical analysis at the cellular level, these individual data points must be aggregated correctly. This repository provides scripts to automate that aggregation, transitioning raw `.csv` exports into structured, reproducible datasets.

## The Biological Problem: The "Average of Averages" Fallacy
A common error in microscopy quantification is simply averaging the mean intensity of all segmented organelles in a cell. This incorrectly weights a 2-pixel artifact the same as a 200-pixel organelle. When performing analyze particles function, ImageJ provides such "Average of Averages" mean value on the "summary" tab, which should not be taken as the correct mean fluorescence value per cell.

To determine the true cellular fluorescence mean, the data must be weighted by area of individual particles. When particle sizes are variable, the ImageJ mean value deviates significantly from weignhted true mean value. The scripts in this repository calculate the true **Weighted Mean Intensity** using the formula:

$$Weighted Mean = \frac{\sum (Area \times Mean Intensity)}{\sum Area}$$

## Included Scripts

### 1. Base Python Grouping Tool (`real_mean_quantifier.py`)
A robust script built using Python's standard `csv` module, designed for custom data formats where group sizes are explicitly defined in the input file.
* **Features:** Includes extensive error handling, data parsing warnings, and generates detailed terminal logs for data verification before outputting the final calculated values.
* **Input:** 3-column CSV (Number of particles per cell, individual particle Area, individual particle Mean). The number of rows for column 2 or 3 should equal to the sum of cloumn 1.
* **Process:** Groups data to each cell by counting the number of particles provided for each cell, calculates the total intensity product ($Area \times Mean$), and divides by the total area per group.
* **Output:** Generates a clean, single-column output of the true mean intensities (same number of rows as column 1 in imput csv).

### 2. Pandas Aggregation Pipeline designed for timelapse images (`TL_real_mean_quantifier.py`)
utilizes the `pandas` library for high-throughput, vectorized data manipulation. 
* **Input:** Standard 3-column CSV (Area, Mean, Slice/Timepoint). Each input is for one cell over timelapse.
* **Process:** 1. Groups the raw organelle data by `Slice` (representing individual timepoints in the timelapse stack).
    2. Calculates the total intensity product ($Area \times Mean$) for all objects in that frame.
    3. Divides by the total area for that frame to yield the true weighted mean.
* **Output:** Generates a clean, chronological single-column output of the true mean intensities across time. This format is optimized for rapid copy-pasting into statistical software (e.g., GraphPad Prism) to plot kinetic response curves without manual data wrangling.


## Usage
1. Export your segmented time-lapse data from ImageJ/Fiji as a `.csv` file, copy the corrwesponding data to a new quant.csv file containing 3 columns.
2. Update the `file_path` variable in the script to point to your target dataset.
3. Run the script via the terminal or your preferred Python IDE.
