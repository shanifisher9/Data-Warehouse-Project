import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES IF EXISTS TO BE ABLE TO CREATE THEM AGAIN

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS song;"
artist_table_drop = "DROP TABLE IF EXISTS artist;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events(num_songs int, artist_id varchar, artist_latitude float, artist_longitude float, artist_location varchar, artist_name varchar, song_id varchar, title varchar, duration float, year int)
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs(artist varchar, auth varchar, firstName varchar, gender varchar, ItemInSession varchar, lastName varchar, length float, level varchar, location varchar, method varchar, page varchar, registration float, sessionId int, song varchar, status varchar, ts bigint, userAgent varchar, userId int)
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay(songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY, start_time timestamp NOT NULL, user_id int NOT NULL, level varchar, song_id varchar, artist_id varchar, session_id int, location varchar, user_agent varchar) 
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users(user_id varchar PRIMARY KEY, first_name varchar, last_name varchar, gender varchar, level varchar)
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS song(song_id varchar PRIMARY KEY, title varchar, artist_id varchar, year int, duration float)
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist(artist_id varchar PRIMARY KEY, name varchar, location varchar, latitude float, longitude float)
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(start_time timestamp PRIMARY KEY, hour int, day int, week int, month varchar, year int, weekday varchar)
""")

# STAGING TABLES - GETTING DATA FROM S3 BUCKETS

staging_events_copy = ("""copy staging_events from {}
iam_role {}
compupdate off
JSON 'auto';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

staging_songs_copy = ("""copy staging_songs from {} 
iam_role {}
compupdate off
JSON {};
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

# INSERTING DATA INTO OUR TABLES CREATED ABOVE


songplay_table_insert = ("""INSERT INTO songplay(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                            SELECT TIMESTAMP 'epoch' + ss.ts/1000 * interval '1 second' as start_date,
                            ss.userId, ss.level, se.song_id, se.artist_id, ss.sessionId, ss.location, ss.userAgent 
                            FROM staging_events se 
                            JOIN staging_songs ss ON (ss.song=se.title AND ss.artist=se.artist_id)
                            WHERE ss.page = 'NextSong'
;
""")

user_table_insert = ("""INSERT INTO users(user_id, first_name, last_name, gender, level)
                        SELECT DISTINCT ss.userId,
                        ss.firstName,
                        ss.lastName,
                        ss.gender,
                        ss.level
                        FROM staging_songs ss WHERE page='NextSong';
""")

song_table_insert = ("""INSERT INTO song(song_id, title, artist_id, year, duration)
                       SELECT DISTINCT se.song_id,
                       se.title,
                       se.artist_id,
                       se.year,
                       se.duration
                       FROM staging_events se;
""")

artist_table_insert = ("""INSERT INTO artist(artist_id, name, location, latitude, longitude)
                        SELECT DISTINCT se.artist_id,
                        se.artist_name,
                        se.artist_location,
                        se.artist_latitude,
                        se.artist_longitude
                        FROM staging_events se;
""")


time_table_insert = ("""INSERT INTO time(start_time, hour, day, week, month, year, weekday)
                        SELECT DISTINCT TIMESTAMP 'epoch' + (ts/1000) * INTERVAL '1 second' as start_time,
                        EXTRACT(HOUR FROM start_time) as hour,
                        EXTRACT(DAY FROM start_time) as day,
                        EXTRACT(WEEK FROM start_time) as week,
                        EXTRACT(MONTH FROM start_time) as month,
                        EXTRACT(YEAR FROM start_time) as year,
                        to_char(start_time, 'Day') as weekday
                        FROM staging_songs;
""")



# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
