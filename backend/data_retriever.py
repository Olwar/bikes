import requests
import sqlite3
import pandas as pd
import numpy as np

# download csv files from an url
def load_csv(url):
    r = requests.get(url)
    name = url[-11:]
    with open(name, 'wb') as f:
        f.write(r.content)
    dataframe = pd.read_csv(name)
    conn = sqlite3.connect(f'{name[:-4]}.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS trips \
    (departure_time, return_time, departure_station_id, departure_station_name, \
    return_station_id, return_station_name, covered_dist_m, duration_sec)""")
    dataframe.to_sql('trips', conn, if_exists='replace', index=False)
    conn.commit()

def combine_dbs():
    db1 = sqlite3.connect('2021-05.db')
    db2 = sqlite3.connect('2021-06.db')
    db3 = sqlite3.connect('2021-07.db')
    cursor1 = db1.cursor()
    cursor2 = db2.cursor()
    cursor3 = db3.cursor()
    query = "SELECT * FROM trips"
    result = cursor1.execute(query).fetchall()
    result2 = cursor2.execute(query).fetchall()
    result3 = cursor3.execute(query).fetchall()
    all_results = result + result2 + result3
    conn = sqlite3.connect('trips.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS trips \
    (departure_time, return_time, departure_station_id, departure_station_name, \
    return_station_id, return_station_name, covered_dist_m, duration_sec)""")
    c.executemany("INSERT INTO trips VALUES (?,?,?,?,?,?,?,?)", all_results)
    conn.commit()
    cursor1.close()
    cursor2.close()
    cursor3.close()
    db1.close()
    db2.close()
    db3.close()
    
def split_db():
    conn = sqlite3.connect('trips.db')
    dataframe = pd.read_sql_query("SELECT * FROM trips", conn)
    dataframe_list = np.array_split(dataframe, 100)
    for i in range(len(dataframe_list)):
        conn = sqlite3.connect(f'trips_{i}.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS trips \
        (departure_time, return_time, departure_station_id, departure_station_name, \
        return_station_id, return_station_name, covered_dist_m, duration_sec)""")
        dataframe_list[i].to_sql('trips', conn, if_exists='replace', index=False)
        conn.commit()

def main():
    url = [
        "https://dev.hsl.fi/citybikes/od-trips-2021/2021-05.csv", 
        "https://dev.hsl.fi/citybikes/od-trips-2021/2021-06.csv",
        "https://dev.hsl.fi/citybikes/od-trips-2021/2021-07.csv"
    ]
    #for i in range(len(url)):
    #    load_csv(url[i])
    combine_dbs()
    split_db()


if __name__ == '__main__':
    main()
