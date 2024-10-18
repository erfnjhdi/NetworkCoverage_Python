import json
import random
import sys
import math
from collections import defaultdict
#COMP348 Assignment 2, by Erfan Jahedi, ID: 40224280. This program will read data from a json file and analyze it.

# Define functions for each menu option
def display_global_statistics(data):
    #this variable will store the base stations list data from the json file
    base_stations = data['baseStations']
    #the total number of base stations, the length of the baseStations list
    total_base_stations = len(base_stations)
    
    #this variable will store the total number of antennas
    total_antennas = 0
    #this list will contain the antennas per each base station, will be updated as we iterate through
    bs_antennas = []
    #calculate the total number of antennas and their distribution per base station by iterating through the base stations and updating our variables
    for bs in base_stations:
        #variable updated by taking the length of the ants list for each base station
        num_antennas = len(bs['ants'])
        total_antennas += num_antennas
        bs_antennas.append(num_antennas)
    #now we can use the bs_antennas list to find the maximum, minimum and average number of antennas
    max_bs_antennas = max(bs_antennas)
    min_bs_antennas = min(bs_antennas)
    avg_bs_antennas = sum(bs_antennas) / total_base_stations
    
    #the coverage of points by antennas
    #first initialize an empty dictionary to count the coverage of each point by antennas
    points = defaultdict(int)

    #iterate over each base station
    for bs in base_stations:
        #iterate over each antenna in the base station
        for antenna in bs['ants']:
            #iterate over each point covered by the antenna
            for pt in antenna['pts']:
                #we take the data from the point and store it
                lat = pt[0]
                lon = pt[1]
                point = (lat, lon)
                #then increment the count of antennas covering this point in the dictionary, each point is essentially a key and has a count value
                points[point] += 1

    #calculate the number of points covered by exactly one antenna
    #empty variable to hold result
    points_covered_by_one = 0
    #iterate through the values in the dictionary
    for count in points.values():
        #if only one count then it means only one antenna is covering it
        if count == 1:
            points_covered_by_one += 1

    #the number of points covered by more than one antenna
    points_covered_by_more_than_one = 0
    #similarly we iterate through dictionary values
    for count in points.values():
        #if count is more than 1 then we incrmement the variable
        if count > 1:
            points_covered_by_more_than_one += 1

    #find the maximum number of antennas covering a single point
    #set max to 0 initially
    max_antennas_covering_one_point = 0
    #iterate through values and if one is more than max keep updating that value to be the new max
    for count in points.values():
        if count > max_antennas_covering_one_point:
            max_antennas_covering_one_point = count

    #calculate the total coverage and the total number of points
    total_coverage = 0
    total_points = 0
    #iterate through all dictionary values
    for count in points.values():
        #incrmement coverage by count so it has the total number of counts
        total_coverage += count
        #increment total points by 1 each iteration
        total_points += 1

    #calculate the average number of antennas covering a point
    avg_antennas_covering_one_point = total_coverage / total_points
    
    #calculate the total number of points in the area based on data extracted from the file
    min_lat = data['min_lat']
    max_lat = data['max_lat']
    min_lon = data['min_lon']
    max_lon = data['max_lon']
    step = data['step']
    #total points is now recalculated using this data
    total_points = int(((max_lat - min_lat) / step + 1) * ((max_lon - min_lon) / step + 1) + 1)
    #to find the points not covered by any antenna we can take the length of the dictionary which is the amount of covered points and subtract it from the total points
    points_not_covered = total_points - len(points)
    #formula to find the percentage of covered area based on total and the number of covered points
    percentage_covered_area = (len(points) / total_points) * 100
    
    #the antenna and base station covering the maximum number of points
    max_coverage_antenna = None
    max_coverage = 0
    #iterate through all base stations
    for bs in base_stations:
        #iterate through all antennas
        for ant in bs['ants']:
            #store the number of points held by that antenna
            coverage = len(ant['pts'])
            #update max
            if coverage > max_coverage:
                max_coverage = coverage
                max_coverage_antenna = (bs['id'], ant['id'])
    
    #print all the global statistics together
    print("Global Statistics:")
    print("Total number of base stations: ", total_base_stations)
    print("Total number of antennas: ", total_antennas)
    print("Max, min, and average number of antennas per base station: ", max_bs_antennas, ", ", min_bs_antennas, ", ", round(avg_bs_antennas, 1))
    print("Total number of points covered by exactly one antenna: ", points_covered_by_one)
    print("Total number of points covered by more than one antenna: ", points_covered_by_more_than_one)
    print("Total number of points not covered by any antenna: ", points_not_covered)
    print("Maximum number of antennas that cover one point: ", max_antennas_covering_one_point)
    print("Average number of antennas covering a point: ", round(avg_antennas_covering_one_point, 1))
    print("Percentage of the covered area: ", round(percentage_covered_area, 2), "%")
    if max_coverage_antenna:
        print("ID of the base station and antenna covering the maximum number of points: base station ", max_coverage_antenna[0], ", antenna ", max_coverage_antenna[1])

#helper function to display statistics for a specific base station which takes in the data from the file and also a given station id
def display_station_statistics(data, station_id):
    #list of base stations
    base_stations = data['baseStations']
    
    #find the base station with the given ID by iterating through base stations and checking their ids
    station = None
    for bs in base_stations:
        if bs['id'] == station_id:
            station = bs
            break
    #print message if base station was not found.
    if not station:
        print(f"No base station found with ID: {station_id}")
        return
    #the total number of antennas in the bs
    total_antennas = len(station['ants'])

    #new dictionary to store the points as keys and the number of antennas storing them as value
    points = defaultdict(int)
    #iterate through each antenna
    for antenna in station['ants']:
            #iterate over each point covered by the antenna
            for pt in antenna['pts']:
                #we take the data from the point and store it
                lat = pt[0]
                lon = pt[1]
                point = (lat, lon)
                #then increment the count of antennas covering this point in the dictionary, each point is essentially a key and has a count value
                points[point] += 1

    #calculate the number of points covered by exactly one antenna
    #empty variable to hold result
    points_covered_by_one = 0
    #iterate through the values in the dictionary
    for count in points.values():
        #if only one count then it means only one antenna is covering it
        if count == 1:
            points_covered_by_one += 1

    #the number of points covered by more than one antenna
    points_covered_by_more_than_one = 0
    #similarly we iterate through dictionary values
    for count in points.values():
        #if count is more than 1 then we incrmement the variable
        if count > 1:
            points_covered_by_more_than_one += 1

    #find the maximum number of antennas covering a single point
    #set max to 0 initially
    max_antennas_covering_one_point = 0
    #iterate through values and if one is more than max keep updating that value to be the new max
    for count in points.values():
        if count > max_antennas_covering_one_point:
            max_antennas_covering_one_point = count

    #calculate the total coverage and the total number of points
    total_coverage = 0
    total_points = 0
    #iterate through all dictionary values
    for count in points.values():
        #incrmement coverage by count so it has the total number of counts
        total_coverage += count
        #increment total points by 1 each iteration
        total_points += 1

    #calculate the average number of antennas covering a point
    avg_antennas_covering_one_point = total_coverage / total_points

    
    #calculate the total number of points in the area based on data extracted from the file
    min_lat = data['min_lat']
    max_lat = data['max_lat']
    min_lon = data['min_lon']
    max_lon = data['max_lon']
    step = data['step']
    #total points is now recalculated using this data
    total_points = int(((max_lat - min_lat) / step + 1) * ((max_lon - min_lon) / step + 1))
    #to find the points not covered by any antenna we can take the length of the dictionary which is the amount of covered points and subtract it from the total points
    points_not_covered = total_points - len(points)
    #formula to find the percentage of covered area based on total and the number of covered points
    percentage_covered_area = (len(points) / total_points) * 100
    
    #the antenna and base station covering the maximum number of points
    max_coverage_antenna = None
    max_coverage = 0
    #iterate through all antennas
    for ant in station['ants']:
        #store the number of points held by that antenna
        coverage = len(ant['pts'])
        #update max
        if coverage > max_coverage:
            max_coverage = coverage
            max_coverage_antenna = (bs['id'], ant['id'])
    
    print("\nStatistics for Base Station ID: " ,station_id)
    print("The total number of antennas =", total_antennas)
    print("The total number of points covered by exactly one antenna =", points_covered_by_one)
    print("The total number of points covered by more than one antenna =", points_covered_by_more_than_one)
    print("The total number of points not covered by any antenna =", points_not_covered)
    print("The maximum number of antennas that cover one point =", max_antennas_covering_one_point)
    print("The average number of antennas covering a point =", round(avg_antennas_covering_one_point, 1))
    print("The percentage of the covered area =", round(percentage_covered_area, 2), "%")
    if max_coverage_antenna:
        print(f"The id of the antenna covering the maximum number of points = antenna {max_coverage_antenna}")

#function to choose a random id for a station
def choose_random_id(data):
    #stores a list of station ids
    station_ids = [bs['id'] for bs in data['baseStations']]
    #choose randomly from list
    random_station_id = random.choice(station_ids)
    #pass id to helper function to display the stations stats
    display_station_statistics(data, random_station_id)
#function to ask user for station id and store it.
def choose_station_id(data):
    #ask user to enter id as input
    station_id = int(input("Enter the station ID: "))
    #if the id is less than 1 or more 2 print message and return because we only have two stations
    if (station_id < 1) or (station_id > 2):
        print("Not a valid station id, try again.")
        return
    #otherwise pass the id to helper function to display station stats
    display_station_statistics(data, station_id)

#function to check coverage for a given coordinate
def check_coverage(data):
    #prompt user to enter a latitude and longitude and store them as float values
    lat = float(input("Enter the latitude: "))
    lon = float(input("Enter the longitude: "))

    #point tuple storing the lat and lon
    point = (lat, lon)
    #boolean to check if the point is covered
    point_covered = False
    #list will store all stations and antennas covering the area.
    covered = []

    #check if the point is covered by any antenna by iteration
    for bs in data['baseStations']:
        for ant in bs['ants']:
            for pt in ant['pts']:
                #if point is found
                if (pt[0], pt[1]) == point:
                    #make boolean true and add its data to list
                    point_covered = True
                    covered.append((bs['id'], ant['id'], pt[2]))
    #if point is covered print the following.
    if point_covered:
        print("The point is covered by the following base stations and antennas:")
        for info in covered:
            print(f"Base Station ID: {info[0]}, Antenna ID: {info[1]}, Received Power: {info[2]}")
    
    else:
        # If the point is not explicitly covered, find the nearest antenna
        nearest_antenna = None
        min_distance = float('inf')
        #iterate through stations, antennas and points
        for bs in data['baseStations']:
            for ant in bs['ants']:
                for pt in ant['pts']:
                    #calculate Euclidean distance between two points
                    distance = math.sqrt((lat - pt[0]) ** 2 + (lon - pt[1]) ** 2)
                    #update minimum distance and nearest antenna info
                    if distance < min_distance:
                        min_distance = distance
                        nearest_antenna = (bs['id'], ant['id'], pt[0], pt[1])
        #show the nearest antenna data
        if nearest_antenna:
            print("The point is not covered. Nearest antenna is:")
            print(f"Base Station ID: {nearest_antenna[0]}, Antenna ID: {nearest_antenna[1]}, Nearest Point Coordinates: ({nearest_antenna[2]}, {nearest_antenna[3]})")


#function to display the menu and handle user input
def display_menu():
    #while loop to have a repeating menu
    while True:
        #print statements
        print("\nMenu:")
        print("1. Display Global Statistics")
        print("2. Display Base Station Statistics")
        print("\t2.1. Statistics for a random station")
        print("\t2.2. Choose a station by Id.")
        print("3. Check Coverage")
        print("4. Exit")
        #store the users choice
        choice = input("Enter your choice: ")

        #if 1 call function to display global statistics
        if choice == '1':
            display_global_statistics(data)
        #if 2 then ask the user if they would like a random station id or to pick one and call appropriate functions
        elif choice == '2':
            sub_choice = input("Enter your choice, 2.1 or 2.2? ")
            if sub_choice == '2.1':
                choose_random_id(data)
            elif sub_choice == '2.2':
                choose_station_id(data)
            else:
                print("Invalid choice. Please choose 2.1 or 2.2.")
        #if they choose 3 call the check coverage method
        elif choice == '3':
            check_coverage(data)
        #if they choose 4 terminate the program
        elif choice == '4':
            print("\nProgram termianted.")
            exit()
        #any other choice is invalid.
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

#load JSON data from file
def load_json(file_path):
    with open(file_path, 'r') as file:
        #return the data
        return json.load(file)
#main
if __name__ == "__main__":
    #data will store all the json file data, and the json file path is picked from the command line
    data = load_json(sys.argv[1])
    #menu is displayed.
    display_menu()
