import os
import time
from functools import total_ordering

from exif import Image
from datetime import datetime
import cv2
import math

def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    return time


def get_time_difference(image_1, image_2):
    time_1 = get_time(image_1)
    time_2 = get_time(image_2)
    time_difference = time_2 - time_1
    return time_difference.seconds


def convert_to_cv(image_1, image_2):
    image_1_cv = cv2.imread(image_1, 0)
    image_2_cv = cv2.imread(image_2, 0)
    return image_1_cv, image_2_cv

#region ai
def calculate_features(image_1_cv, image_2_cv, feature_number):
    orb = cv2.ORB_create(nfeatures=feature_number)
    keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
    keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
    return keypoints_1, keypoints_2, descriptors_1, descriptors_2


def calculate_matches(descriptors_1, descriptors_2):
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = brute_force.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches


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


def calculate_mean_distance(coordinates_1, coordinates_2):
    all_distances = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference)
        all_distances = all_distances + distance
    return all_distances / len(merged_coordinates)


def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
    distance = feature_distance * GSD / 100000
    print(distance)
    speed = distance / time_difference
    return speed

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

def dms_to_decimal(degrees, minutes, seconds):
    return degrees + (minutes / 60.0) + (seconds / 3600.0)

distances = []
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

def exif_speed(image_num):
    speed = get_distance(image_num) / get_time_difference(images[image_num], images[image_num+1])
    return speed

def init_images():
    directory = "img"
    images = []
    times = []

    for file in os.listdir(directory):
        images.append("img/" + file)
        if (len(images) != 1):
            times.append(get_time_difference(images[images.index("img/" + file) - 1], "img/" + file))


    return images, times

def simulate_images():
    for i in range(len(images) - 1):

        if len(images[i]) != 1:
            print("ai")
            print(get_ai_speed(i))
            print("exif")
            print(exif_speed(i))

            print("sleep for: ")
            print(times[i] - 1)
            time.sleep(times[i - 1])
            if i == len(images):
                time.sleep(100)

images, times = init_images()
simulate_images()
