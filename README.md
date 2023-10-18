# Polygon Area Calculation Script

This script, "Polygon Area Calculation," is designed to calculate the area of polygons within an image and express their collective area as a percentage of the entire image. It reads labeled text files, computes the area for each polygon, and calculates the ratio of that area to the overall image dimensions provided.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.x.
- You have installed the necessary Python packages: pandas and Shapely. You can install these using pip:


```
pip install pandas Shapely
```


## Using the Polygon Area Calculation Script

To use the script from the command line, follow these steps:

1. Clone this repository to your local machine or download the script file directly.
2. Open a terminal and navigate to the directory containing the script.
3. Run the script using the following syntax:


```
python <script_name> --directory <path_to_directory_with_text_files> --width <image_width> --height <image_height>
```


Replace `<script_name>` with the name of the script file, `<path_to_directory_with_text_files>` with the path to the directory containing the labeled text files, and `<image_width>` and `<image_height>` with the dimensions of the original image in pixels.

Example:

```
python polygon_area_calculator.py --directory ./labels --width 1920 --height 1080
```


## Output

The script generates a CSV file named `polygon_volumes.csv`. This file contains the polygon information for each text file in the directory. Each record includes the file number, the total polygon area in pixels, and the percentage of the image that the polygon occupies.

## Important Notes

- The script assumes that the text files follow a specific format. Ensure your files are formatted correctly.
- If the script encounters an error or cannot find a file, it records 0 for both the area and percentage for the corresponding entry.
