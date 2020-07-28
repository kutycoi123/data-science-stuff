import sys
from pyspark.sql import SparkSession, functions, types, Row
import re

spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")

def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)

    if m:
        # TODO
        return Row(hostname=m.group(1), bytes=m.group(2))
    else:
        return None


def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    # TODO: return an RDD of Row() objects
    rows = log_lines.map(lambda e: line_to_row(e)).filter(lambda e: not_none(e))
    #print(log_lines)
    return rows





def main(in_directory):
    logs = spark.createDataFrame(create_row_rdd(in_directory))
    num_points = logs.count()

    grouped_host = logs.groupBy('hostname').agg(functions.count('hostname').alias('xi'),\
                                                functions.sum('bytes').alias('yi'),\
                                                functions.pow(functions.count('hostname'), 2).alias('xi^2'),\
                                                functions.pow(functions.sum('bytes'), 2).alias('yi^2'),\
                                                (functions.sum('bytes')*functions.count('hostname')).alias('xiyi')).cache()
    grouped_host = grouped_host.groupBy().agg(functions.count('hostname').alias('n'),\
                                    functions.sum('xi').alias('sum_xi'),\
                                    functions.sum('yi').alias('sum_yi'),\
                                    functions.sum('xi^2').alias('sum_xi^2'),\
                                    functions.sum('yi^2').alias('sum_yi^2'),\
                                    functions.sum('xiyi').alias('sum_xiyi'))

    # TODO: calculate r.

    n, sum_x, sum_y, sum_x_2, sum_y_2, sum_xy = grouped_host.first() 
    r = (n*sum_xy - sum_x*sum_y) / (((n*sum_x_2-sum_x*sum_x) ** 0.5) * ((n*sum_y_2 - sum_y*sum_y) ** 0.5))
    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)
