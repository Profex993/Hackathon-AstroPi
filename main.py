import os
import threading
import time

from exif import Image
from datetime import datetime
import cv2
import math
import json




# Gets metadata time from the image
def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    return time

# Calculates time difference between two images and returns seconds
def get_time_difference(image_1, image_2):
    time_1 = get_time(image_1)
    time_2 = get_time(image_2)
    time_difference = time_2 - time_1
    return time_difference.seconds

# Converts two images into computer vision
def convert_to_cv(image_1, image_2):
    image_1_cv = cv2.imread(image_1, 0)
    image_2_cv = cv2.imread(image_2, 0)
    return image_1_cv, image_2_cv

# Calculates keypoints and descriptors of each image
def calculate_features(image_1_cv, image_2_cv, feature_number):
    orb = cv2.ORB_create(nfeatures=feature_number)
    keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
    keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
    return keypoints_1, keypoints_2, descriptors_1, descriptors_2

# Calculate the matches between descriptors
def calculate_matches(descriptors_1, descriptors_2):
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = brute_force.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

# Finds matching coordinates
def find_matching_coordinates(keypoints_1, keypoints_2, matches):
    coordinates_1 = []
    coordinates_2 = []
    for match in matches:
        image_1_idx = match.queryIdx
        image_2_idx = match.trainIdx
        (x1, y1) = keypoints_1[image_1_idx].pt
        (x2, y2) = keypoints_2[image_2_idx].pt
        coordinates_1.append((x1, y1))
        coordinates_2.append((x2, y2))
    return coordinates_1, coordinates_2

# Calculates the mean distance between two coordinates
def calculate_mean_distance(coordinates_1, coordinates_2):
    all_distances = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference)
        all_distances = all_distances + distance
    return all_distances / len(merged_coordinates)

# Calculates the speed in kilometers per second between distances
def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
    distance = feature_distance * GSD / 100000
    print(distance)
    speed = distance / time_difference
    return speed

# Gets speed from this image to the next one
def get_ai_speed(image_num):
    time_difference = get_time_difference(images[image_num], images[image_num+1])
    image_1_cv, image_2_cv = convert_to_cv(images[image_num], images[image_num + 1])
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000)
    matches = calculate_matches(descriptors_1, descriptors_2)
    coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
    average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
    speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)
    return speed
#endregion ai

# Converts degrees minutes and seconds into degrees with decimal points
def dms_to_decimal(degrees, minutes, seconds):
    return degrees + (minutes / 60.0) + (seconds / 3600.0)

distances = []

# Gets the distance from two images
def get_distance(image_num):
    total_distance = 0
    R = 6371.0

    img1 = Image(images[image_num])
    img2 = Image(images[image_num + 1])

    # Extract GPS data
    lon1 = img1.gps_longitude
    lat1 = img1.gps_latitude
    lon2 = img2.gps_longitude
    lat2 = img2.gps_latitude

    # Convert DMS to decimal degrees
    lon1 = dms_to_decimal(*lon1)
    lat1 = dms_to_decimal(*lat1)
    lon2 = dms_to_decimal(*lon2)
    lat2 = dms_to_decimal(*lat2)

    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = map(math.radians, [lat1, lon1])
    lat2, lon2 = map(math.radians, [lat2, lon2])

    # Differences in coordinates
    difference_lat = lat2 - lat1
    difference_lon = lon2 - lon1

    # Haversine formula
    a = math.sin(difference_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(difference_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance
    distance = R * c

    distances.append(distance)

    for distance in distances:
        total_distance = total_distance + distance

    total_distance = total_distance / len(distances)
    print(total_distance)

    return total_distance

# Returns speed from image
def exif_speed(image_num):
    speed = get_distance(image_num) / get_time_difference(images[image_num], images[image_num+1])
    return speed

# Initializes the images
def init_images():
    directory = "img"
    images = []
    times = []

    for file in os.listdir(directory):
        images.append("img/" + file)
        if (len(images) != 1):
            times.append(get_time_difference(images[images.index("img/" + file) - 1], "img/" + file))

    return images, times

# Simulates the images
def simulate_images():
    for i in range(len(images) - 1):
        out = '{ "ai" : 0, "exif" : 0, "img": "img", "img1": 0}'
        val = json.loads(out)
        if len(images[i]) != 1:
            print("ai")
            print(get_ai_speed(i))
            val["ai"] = get_ai_speed(i)
            print("exif")
            print(exif_speed(i))
            val["exif"] = exif_speed(i)
            val["img"] = images[i]
            val["img1"] = images[i - 1]
            print("sleep for: ")
            print(times[i] - 1)
            val["sleep"] = times[i] - 1
            with open("webFolder/data.json", "w") as outfile:
                json.dump(val, outfile)
            time.sleep(times[i - 1])
            if i == len(images):
                time.sleep(100)


images, times = init_images()

def task1():
    simulate_images()

def task2():
    app.run()

thread1 = threading.Thread(target=task1)
thread2 = threading.Thread(target=task2)

thread1.start()
thread2.start()

from flask import Flask, send_from_directory, send_file

app = Flask(__name__)

WEB_FOLDER = "webFolder"

@app.route("/")
def serve_index():
    return send_from_directory(WEB_FOLDER, "index.html")

@app.route("/<path:filename>")
def serve_static_files(filename):
    return send_from_directory(WEB_FOLDER, filename)

@app.route('/get-image', methods=['GET'])
def get_image(): # Path inside the static folder
    if os.path.exists("img"):
        return send_from_directory('img', 'photo_0673.jpg')  # Serve the file from the static folder
    else:
        return "Image not found", 404

