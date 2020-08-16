import pandas as pd
from numpy import NaN
from shapely.geometry import Point, Polygon
import geopandas as gpd

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 17)

habitat_df = pd.read_csv("data/SiteConditionAssessment.csv", encoding="ISO-8859-1")
habitat_df = habitat_df[["decimalLatitude", "decimalLongitude", "Overall Condition Rating"]]

hospital_df = pd.read_csv("data/Hospital_Locations.csv")
hospital_df = hospital_df[["X", "Y", "LabelName", "Postcode"]]

def create_Polygon(lat, lon):
    top_left = (lat + 0.1, lon - 0.1)
    top_right = (lat + 0.1, lon + 0.1)
    bottom_left = (lat - 0.1, lon - 0.1)
    bottom_right = (lat - 0.1, lon + 0.1)
    return Polygon([top_left, top_right, bottom_right, bottom_left])

def get_hospitals_within(givenLat, givenLon):
    zone = create_Polygon(givenLat, givenLon)
    count = 0
    for i in range(hospital_df.shape[0]):
        lat = hospital_df["Y"][i]
        lon = hospital_df["X"][i]
        if Point(lat, lon).within(zone):
            count += 1

    return count

def get_habitat_score_within(givenLat, givenLon):
    zone = create_Polygon(givenLat, givenLon)
    score = 0
    for i in range(habitat_df.shape[0]):
        lat = habitat_df["decimalLatitude"][i]
        lon = habitat_df["decimalLongitude"][i]
        if Point(lat, lon).within(zone):
            score += habitat_df["Overall Condition Rating"][i]

    return score

def get_Address(lat,lon):
    GOOGLE_API_KEY = 'AIzaSyAac10LTG_KTdy4yKwT0o3vxLn6ME4xXNo'
    from geopy.geocoders import GoogleV3
    geo_info = {}
    geolocator = GoogleV3(api_key=GOOGLE_API_KEY)
    coordinates = lat, lon
    locations = geolocator.reverse(coordinates)

    geo_info["full_address"] = locations.address
    geo_info["country"] = locations.address.split(",")[-1].strip()
    geo_info["post_code"] = locations.address.split(",")[-2].split(" ")[-1]

    return geo_info

def get_bushfire_polygons():
    bushfire_shp = gpd.read_file("mapData/Bushfire Prone Area/bushfire_prone_area.shp")
    polygons = []
    for geos in bushfire_shp['geometry']:
        try:
            if len(geos) > 1:
                for poly in geos:
                    polygons.append(poly)
        except:
            continue


    return polygons

def get_Bushfire_prone(lat,lon):
    zone = create_Polygon(lat, lon)
    # print(zone)
    polygons = get_bushfire_polygons()
    count = 0

    for poly in polygons:
        # print("!!!!!")
        if zone.intersects(poly):
            print("Fireeeeeeeeee!!!!!")
            count += 1
    return count

def get_region_insights(lat, lon, bushfire = False):
    import json
    return_list = {}
    hospital_insight_dict = {"source": "Hospital Data",
                             "metric": "Number of Hospitals in the 11km radius",
                             "value": get_hospitals_within(lat, lon)}
    return_list["HOSPITAL"] = hospital_insight_dict

    habitat_insight_dict = {"source": "Habitat Condition Data", "metric": "Overall ",
                            "value": get_habitat_score_within(lat, lon)}
    return_list["HABITAT"] = habitat_insight_dict

    hazard_data = {}

    if bushfire:
        hazard_data["priority_value"] = hospital_insight_dict["value"] - habitat_insight_dict["value"] - get_Bushfire_prone(lat, lon)
        print("Bushfire Count: ", get_Bushfire_prone(lat, lon))
    else:
        hazard_data["priority_value"] = hospital_insight_dict["value"] - habitat_insight_dict["value"]

    if hazard_data["priority_value"] <= 0:
        hazard_data["priority_index"] = "NO RESOURCE"
    elif hazard_data["priority_value"] <= 1:
        hazard_data["priority_index"] = "REQUIRE RESOURCE"
    elif hazard_data["priority_value"] <= 2:
        hazard_data["priority_index"] = "ADEQUATE RESOURCE"
    else:
        hazard_data["priority_index"] = "SUFFICIENT RESOURCE"

    return_list["HAZARD_INFO"] = hazard_data

    return_list["GEO_INFO"] = get_Address(lat,lon)

    return json.dumps(return_list)


# def triggerSMS():
#     trigger = True
#     clean_api_data_and_save()
#     epa_api_df = pd.read_pickle("./pickle_data/epa_api_data_df.pkl")
#
#     print(len(epa_api_df["healthAdvice"]))
#     for i in range(len(epa_api_df["healthAdvice"])):
#         if epa_api_df["healthAdvice"][i] == "Good":
#             trigger = False
#         elif epa_api_df["healthAdvice"][i] == "Moderate":
#             # readJson = get_region_insights(lat,lon)
#             trigger = True
#         elif epa_api_df["healthAdvice"][i] == "Poor":
#             # readJson = get_region_insights(lat, lon)
#             trigger = True
#         elif epa_api_df["healthAdvice"][i] == "Very poor":
#             # readJson = get_region_insights(lat, lon)
#             trigger = True
#         elif epa_api_df["healthAdvice"][i] == "Hazardous":
#             trigger = True
#
#         return trigger

#
# triggerSMS()
# lat = -37.828728
# lon = 145.132400
#
#
# lat = -36.57954599999999
# lon = 142.92605
# # RUN THE FOLLOWING LINE TO GET YOUR JSON DATA
# print(get_region_insights(lat, lon, True))






