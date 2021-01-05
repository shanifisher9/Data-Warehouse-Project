### Creating Redshift DataWarehouse

When dealing with a large amount of data also called big data, it may not be possible to store all of it on a local machine. It can take up a lot of space, a long time to load, or may crash your computer. Therefore, cloud computing has become available. This is a large amount of servers in one place that allows a big amount of data to be run and stored. There are a few different providers for the cloud but the biggest one is AWS (Amazon Web Service).

At Sparkify you are constantly growing and acquiring more data. Therefore, I decided to create a Redshift cluster on AWS to help extract and analyse your data. Redshift is a Data Warehouse that can grab data from an s3 bucket(storage container) and get the data you need in the database. You will need to pay for AWS services. However,since you will be having a lot of data as your company grows it is worth it to store you data in the cloud. This will help you get the most out of your data and you will be able to analyse it and make business decisions. It makes sense to set up the structure in the cloud and pay the costs so you will not need to transfer over all your data in a few years once you get large amounts.

# Data

The data is stored in 2 JSON files in an S3 bucket.

An S3 bucket is a storage container in AWS that allows you to keep your data there. Once the data is in the S3 bucket I will be able to extract it and load it into the tables that we will need to analyse the data and make it easy to read.

# Table Design

I have created a star schema database design to store your data. A star schema database has a fact table and dimension tables. The fact table has the core information about the songs played and the dimension tables has more informtaion about the instance that happened ex: which user played the songs, which artists were played, etc. I created this type of database because it is easy to read and easy to access the data using joins.


# Tables

In the Database there are 5 different tables

1. Songplays - This is information about the songs played on Sparkify. This is the fact table.
    Columns: songplay_id, start_time, user_id, level, artist_id, location, user_agen

2. Song - This is a list all your songs on Sparkify. This is a dimension table.
    Columns: song_id, title, artist_id, year, duration

3. Users - This is a list of your users. This is a dimension table.
    Columns: user_id, first_name, last_name, gender, level
    
4. Artists - This is information about the artists who's songs are played on Sparkify. This is a dimension table.
    Columns: artist_id, name, location, latitude, longitude

5. Time - This is a list of times that are generated from the Songplays start_time column. This is a dimension table
    Columns: start_time, hour, day, week, month, year, weekday

The first column of all the dimension tables are the primary keys to help join to the fact table. The primary keys help you join correctly to the fact table so your data is correct. It is best practice to join using these keys.

# ETL - Extract Transform Load

Sparify's data is currently in JSON format in an S3 bucket. 

To access the data from the S3 bucket I am using Redshift to grab the data and transform it into the tables that I specified. This was a fairly easy process but Redshift needs to have permission to get the data from the S3 bucket. Therefore, I created an IAM role to grant Redshift access.

# Running The Scripts

There are 2 different scripts that you need to run to get and access the data.

1. create_tables.py - This created the tables discussed earlier and drops the tables if they already exist.

2. etl.py - This gets the data from the s3 bucket and transforms it into the tables created in the create_tables.

To run these scripts open a new console editor and run the scripts.

In both of these processes the script will connect to AWS and the Redshift cluster. Additionally it will connect to the postgresql so you can run some queries and analyse the data.

Before running either of these scripts you will need to create a Redshift Cluser, IAM role and put your data in the S3 buckets. After all of this has been done you will need to fill out dwh.cfg and put in your information about your Redshift cluster, IAM role and S3 bucket.

Some definitions:
Cluster = Redshift
IAM role = permission to access the S3 bucket
S3 bucket = file storage container

Now that your data is in the cloud and is accessable. You can run some queries using postrgresql in an editor or on AWS inerface to learn more about your data and customers.
