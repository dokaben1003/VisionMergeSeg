import os
import argparse
import pandas as pd
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.validation import make_valid

def calculate_polygon_area(coordinates):
    n = len(coordinates) // 2  # number of vertices
    area = 0.0

    for i in range(n):
        j = (i + 1) % n
        area += coordinates[2*i] * coordinates[2*j+1]
        area -= coordinates[2*j] * coordinates[2*i+1]
    area = abs(area) / 2.0
    return area

def calculate_polygon_ratio(filepath, image_width, image_height):
    polygons = []  # list to store all polygons

    with open(filepath, 'r') as file:
        lines = file.readlines()

    total_pixels = image_width * image_height

    for line in lines:
        data = line.strip().split(' ')
        coordinates = [float(coord) for coord in data[1:] if coord]  # exclude empty strings

        coordinates = [coord * image_width if i % 2 == 0 else coord * image_height for i, coord in enumerate(coordinates)]

        polygon = Polygon([(coordinates[i], coordinates[i+1]) for i in range(0, len(coordinates), 2)])

        if not polygon.is_valid:
            polygon = make_valid(polygon)

        polygons.append(polygon)

    try:
        merged_polygon = unary_union(polygons)
    except Exception as e:
        return str(e), None  # return error message

    total_area = merged_polygon.area if merged_polygon.is_valid else 0.0
    ratio = total_area / total_pixels

    result = {
        "total_area": total_area,
        "total_pixels": total_pixels,
        "ratio": ratio
    }

    return None, result  # No error message, return result


def process_files(directory, image_width, image_height):
    if not os.path.exists(directory):
        print(f"{directory} does not exist.")
        return

    total_pixels = image_width * image_height
    data = []
    processed_nums = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt") and filename.startswith("test_"):
            num = int(filename.split('_')[1].split('.')[0])
            processed_nums.append(num)
            filepath = os.path.join(directory, filename)

            error, result = calculate_polygon_ratio(filepath, image_width, image_height)
            if error:
                print(f"Error processing file {filename}: {error}")
                continue

            data.append({
                "num": num,
                "area_constant": result['total_area'],
                "vol_percentage": result['ratio'] * 100  # Convert ratio to percentage
            })

    # ... [rest of the code remains the same as previous]

    # Add missing numbers with area 0 and percentage 0
    for missing_num in range(min(processed_nums), max(processed_nums) + 1):
        if missing_num not in processed_nums:
            data.append({
                "num": missing_num,
                "area_constant": 0,
                "vol_percentage": 0
            })

    df = pd.DataFrame(data)
    df.sort_values(by="num", inplace=True)
    df.to_csv('polygon_volumes.csv', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate the area and volume percentage of polygons in images.')
    parser.add_argument('--directory', required=True, help='Path to the directory containing the label files')
    parser.add_argument('--width', type=int, required=True, help='The width of the original image in pixels')
    parser.add_argument('--height', type=int, required=True, help='The height of the original image in pixels')

    args = parser.parse_args()

    process_files(args.directory, args.width, args.height)
