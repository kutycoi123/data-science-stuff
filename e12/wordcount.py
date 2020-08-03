import sys
from pyspark.sql import SparkSession, functions as f, types, Row
import string, re
spark = SparkSession.builder.appName('World count').getOrCreate()
spark.sparkContext.setLogLevel('WARN')
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)  # regex that matches spaces and/or punctuation

def main(in_dir, out_dir):
	df = spark.read.text(in_dir, wholetext=True) 
	df = df.select(f.explode(f.split('value', wordbreak)).alias('word'))
	df = df.select(f.lower('word').alias('word'))
	df = df.groupBy('word').agg(f.count('word').alias('count')).orderBy(['count', 'word'], ascending=False).cache()
	df.write.csv(out_dir, mode='overwrite', compression='none')

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)