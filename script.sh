
# sudo docker exec -it spark-master bash -c "
# apt-get update &&
# apt-get install python3-dev libmysqlclient-dev -y &&
# apt-get install python-pip -y &&
# pip install mysqlclient &&
# apt-get install python-mysqldb
# exit"
#
# sudo docker exec -it spark-worker bash -c "
# apt-get update &&
# apt-get install python3-dev libmysqlclient-dev -y &&
# apt-get install python-pip -y &&
# pip install mysqlclient &&
# apt-get install python-mysqldb
# exit"

#!/data/data.py
sudo docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /data/data.py
