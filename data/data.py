from pyspark import SparkContext
from time import sleep
import MySQLdb



# sleep(4)
sc = SparkContext("spark://spark-master:7077", "PopularGroups")

data = sc.textFile("/data/access.log", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split())   # tell each worker to split each line of it's partition
pages = pairs.map(lambda pair: (pair[1], 1))      # re-layout the data to ignore the user id
count = pages.reduceByKey(lambda x,y: int(x)+int(y))        # shuffle the data so that each key is only on one worker
                                                  # and then reduce all the values by adding them together

output = count.collect()                          # bring the data back to the master node so we can print it out
for page_id, count in output:
    print ("page_id %s count %d" % (page_id, count))
print ("Popular groups done")

sc.stop()

db = MySQLdb.connect(host = 'db', user='www', database='cs4501',password='$3cureUS')
cursor = db.cursor()
cursor.execute("TRUNCATE TABLE Recommendation")

row = {1,"1"}
cursor.execute("INSERT INTO Recommendation (group_id, recommended_groups) VALUES (%s, %s)", row)

db.commit()

cursor.close()
db.close()
