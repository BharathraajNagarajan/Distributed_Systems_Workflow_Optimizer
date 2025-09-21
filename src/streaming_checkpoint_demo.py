import sys
import time
import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

def run(inputDir, checkpointDir, triggerSec):
    spark = (SparkSession.builder
             .appName("StreamingReliabilityDemo")
             .getOrCreate())

    spark.sparkContext.setLogLevel("WARN")

    # Define streaming source
    lines = (spark.readStream
             .format("text")
             .load(inputDir))

    words = lines.select(explode(split(lines.value, "\\s+")).alias("word"))

    wordCounts = words.groupBy("word").count()

    # Write output to console
    query = (wordCounts.writeStream
             .outputMode("complete")
             .format("console")
             .option("checkpointLocation", checkpointDir)
             .trigger(processingTime=f"{triggerSec} seconds")
             .start())

    # Wait 5s, then create test files automatically
    time.sleep(5)
    with open(f"{inputDir}/batch1.txt", "w") as f:
        f.write("hello spark streaming test\n")
    with open(f"{inputDir}/batch2.txt", "w") as f:
        f.write("spark streaming checkpoint recovery\n")

    print(">>> Test files created inside stream_in folder <<<")

    query.awaitTermination(30)  # run for 30 seconds then stop

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputDir", required=True)
    parser.add_argument("--checkpointDir", required=True)
    parser.add_argument("--triggerSec", type=int, default=5)
    args = parser.parse_args()

    run(args.inputDir, args.checkpointDir, args.triggerSec)
