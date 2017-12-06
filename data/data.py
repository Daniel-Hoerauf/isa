from pyspark import SparkContext
from time import sleep
import MySQLdb
import itertools


while True:
    sleep(180)
    sc = SparkContext("spark://spark-master:7077", "PopularGroups")

    data = sc.textFile("/data/access.log", 2).distinct()     # each worker loads a piece of the data file

    pairs = data.map(lambda line: line.split())   # tell each worker to split each line of it's partition
    grouped = pairs.groupByKey()
    grouped = grouped.mapValues(lambda group: sorted(group))

    count = grouped.flatMapValues(lambda group: itertools.combinations(group, 2))
    count = count.mapValues(lambda pair: (pair[1], pair[0]) if int(pair[0]) > int(pair[1]) else pair)
    count = count.map(lambda pair: (pair[1], pair[0]))
    count = count.groupByKey()
    count = count.map(lambda pair: (pair[0], len(pair[1])))
    count = count.filter(lambda pair: pair[1] >= 3)

    output = count.collect()                      # bring the data back to the master node so we can print it out
    rows = {}
    for page_id, count in output:

        rows[str(page_id[0])]= rows.get(page_id[0],"") + str(page_id[1]) + " "
        rows[str(page_id[1])]= rows.get(page_id[1],"") + str(page_id[0]) + " "
        print ("page_id %s count %s" % (page_id, count))
    print(rows)

    sc.stop()
    print(rows)
    db = MySQLdb.connect(host = 'db', user='www', db ='cs4501', passwd='$3cureUS')
    cursor = db.cursor()
    cursor.execute("TRUNCATE TABLE models_recommendation")

    for group, recommendations in rows.items():
        row = {group,recommendations}
        cursor.execute("INSERT INTO models_recommendation (group_id, recommended_groups) VALUES (%s, %s)", (group,recommendations))

    db.commit()

    cursor.close()
    db.close()
