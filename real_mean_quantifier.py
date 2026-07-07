import csv
from io import StringIO
from typing import List, Dict, Union


def calculate_mean_intensity(csv_data: str) -> List[Dict[str, Union[str, float, int]]]:
    """
    Calculates the mean intensity for groups defined in a custom CSV format.

    The CSV structure is expected to be:
    Column 1: Group Size (only in the first N rows, where N is the number of groups)
    Column 2: Area measurement
    Column 3: Intensity measurement

    Mean Intensity = Sum(Area * Intensity) / Sum(Area)

    Args:
        csv_data: A string containing the entire content of the CSV file.

    Returns:
        A list of dictionaries, where each dictionary contains the results
        for one group (Group, Size, Total Area, Mean Intensity).
    """

    # Use .strip() on the input data to remove any leading/trailing whitespace
    # and newlines that can interfere with csv.reader.
    cleaned_csv_data = csv_data.strip()
    if not cleaned_csv_data:
        print("Warning: Input CSV data is empty after stripping whitespace.")
        return []

    # Use StringIO to treat the string data like a file object
    reader = csv.reader(StringIO(cleaned_csv_data))

    # Initialize storage for parsed data
    group_sizes: List[int] = []
    all_areas: List[float] = []
    all_intensities: List[float] = []

    # --- 1. First Pass: Parse Group Sizes and Collect All Data ---

    for row in reader:
        # Filter out empty rows or lines that are too short
        if not row or len(row) < 3:
            continue

        try:
            # Column 1: Group Size (may be empty after the first N rows)
            c1_str = row[0].strip()
            if c1_str:
                group_sizes.append(int(c1_str))

            # Column 2 & 3: Area and Intensity (should be present in every data row)
            area = float(row[1].strip())
            intensity = float(row[2].strip())

            all_areas.append(area)
            all_intensities.append(intensity)

        except ValueError as e:
            # Skip rows where conversion fails (e.g., header row, junk data)
            print(f"Warning: Skipping row due to parsing error (likely a header or invalid number): {row}. Error: {e}")
            continue

    if not all_areas:
        print("Error: No valid measurement data (Area and Intensity) found after parsing.")
        return []

    if not group_sizes:
        print(
            "Error: No valid group sizes found in Column 1. Check if Column 1 contains integers for the first N groups.")
        return []

    total_data_points = sum(group_sizes)
    if total_data_points != len(all_areas):
        raise ValueError(
            f"Data mismatch! Expected {total_data_points} data points based on group sizes, "
            f"but found {len(all_areas)} measurement pairs. Check your CSV format."
        )

    # --- 2. Second Pass: Calculate Mean Intensity per Group ---

    results: List[Dict[str, Union[str, float, int]]] = []
    data_index = 0

    for i, size in enumerate(group_sizes):
        group_name = f"Group {i + 1}"
        current_group_areas = all_areas[data_index:data_index + size]
        current_group_intensities = all_intensities[data_index:data_index + size]

        total_intensity_product = 0.0
        total_area = 0.0

        for area, intensity in zip(current_group_areas, current_group_intensities):
            total_intensity_product += area * intensity
            total_area += area

        mean_intensity = 0.0
        if total_area > 0:
            mean_intensity = total_intensity_product / total_area

        results.append({
            "Group": group_name,
            "Size": size,
            "Sum(Area * Intensity)": total_intensity_product,
            "Sum(Area)": total_area,
            "Mean Intensity": mean_intensity
        })

        data_index += size

    return results


# --- Main Execution ---
if __name__ == "__main__":
    # The file path provided by the user (using raw string notation r"" for Windows paths)
    file_path = r"C:\Users\haoning.yang\Desktop\quant.csv"

    try:
        # Read the content of the user's CSV file
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            file_content = f.read()

        # Calculate results from the file data
        calculated_results = calculate_mean_intensity(file_content)

        print("-" * 50)
        print(f"Calculation Results for {file_path}:")
        print("-" * 50)

        if not calculated_results:
            print("No results were generated. Please review the warnings above and ensure the file contains data.")
        else:
            # 1. Detailed Results Output (same as before)
            print("Detailed Group Results:")
            for result in calculated_results:
                print(f"  Group: {result['Group']} (Size: {result['Size']})")
                print(f"    Total Area: {result['Sum(Area)']:,.2f}")
                print(f"    Mean Intensity: {result['Mean Intensity']:,.4f}")

            # 2. Single Column Output (NEW)
            print("\n" + "=" * 50)
            print("Mean Intensities (Single Column for Copying):")
            print("=" * 50)

            for result in calculated_results:
                # Print only the Mean Intensity value, formatted to 4 decimal places
                print(f"{result['Mean Intensity']:,.4f}")

    except FileNotFoundError:
        print(f"\nFATAL ERROR: File not found at the specified path: {file_path}")
    except ValueError as e:
        print(f"\nFATAL ERROR: Data parsing failed. {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

    print("-" * 50)
    print("Execution complete.")
