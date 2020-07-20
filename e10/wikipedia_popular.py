import sys
import os
from pyspark.sql import SparkSession, types, functions
spark = SparkSession.builder.appName('wikipedia').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

wiki_schema = types.StructType([
    types.StructField('language', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('count', types.IntegerType()),
    types.StructField('bytes', types.IntegerType())
])

def extract_hour(path):
    head, filename = os.path.split(path)
    l = len(filename)
    hour = filename[filename.index('-')+1:l-7]
    return hour
    
    
def main(in_dir, out_dir):
    path_to_hour = functions.udf(extract_hour, returnType=types.StringType())
    wiki = spark.read.csv(in_dir, sep=' ', schema=wiki_schema)\
        .withColumn('filename', functions.input_file_name())\
        .withColumn('hour', path_to_hour('filename'))\
    
    df = wiki.filter(~(wiki.name.contains('Main_Page')) & 
                     ~(wiki.name.contains('Special')))
    df = df.filter(df['language'] == 'en')

    max_df = df.groupBy('hour').agg(functions.max('count').alias('count'))
    max_df.show()
    joined = max_df.join(df, ['hour', 'count'], 'inner')\
                   .orderBy(['hour', 'name'], ascending=True)\
                   .drop('filename','language','bytes')
    joined.write.csv(out_dir,mode='overwrite')
    

if __name__ == '__main__':
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    main(in_dir, out_dir)
