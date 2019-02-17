import os
import sys
import hashlib
import filecmp
import pandas as pd
import logging

from pyspark import SparkContext, SparkConf

os.environ["SPARK_HOME"] = "/usr/local/lib/python3.5/dist-packages/pyspark"
os.environ["PYSPARK_PYTHON"]="/usr/bin/python3.5"

appName = "PyDuplicatesScaner"

conf = SparkConf()\
    .setAppName(appName)\
    .setMaster('local[3]')
sc = SparkContext(conf=conf)

class CheckDir():
    def __init__(self,path):
        self.path = path
        self.filelist = []
        self.df = pd.DataFrame(self.collect(),
                               columns=["Name", "Path",
                                        "Size", "Content"])

    def collect(self):
        def hash(path):
            if os.path.isfile(path):
                try:
                    with open(path, 'rb') as file:
                        hash = hashlib.sha1(file.read())
                        res = hash.hexdigest()
                        logging.info("success %s" % path)
                        return res
                except PermissionError:
                    logging.error("permission error: %s" % path)
                    return
                except TypeError:
                    logging.error("type error: %s" % path)
                    return
                except:
                    logging.error("Unexpected error: % %s" % \
                                  sys.exc_info()[0])
                    return


        getthrow = lambda args:\
            [(fname, os.path.join(args[0],fname))\
             for fname in args[2]]

        def getInfo(t:tuple):
            logging.info("try {0}".format(t[1]))
            size = os.path.getsize(t[1])
            content = hash(t[1])
            return (t[0], t[1], size, content)


        return sc.parallelize(os.walk(self.path))\
            .flatMap(getthrow) \
            .map(getInfo) \
            .filter(lambda t: len(t) == 4) \
            .collect()

if __name__ == "__main__":
    dir = CheckDir(os.path.curdir)

    print(dir.df.head(10))

