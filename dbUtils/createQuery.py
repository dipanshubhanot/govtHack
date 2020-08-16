import sqlite3


def insert_img(tableName, fname=None, **kwargs):
    vals = sorted(kwargs.items())
    query = "INSERT INTO " + tableName +"("
    for (key, val) in vals:
        query += str(key)+", "
    query = query[:-2] + ")"
    query += " VALUES ("
    for (key, val) in vals:
        query += str(val) + ","
    query = query[:-1] + ")"
    print(query)
    return query


def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data
