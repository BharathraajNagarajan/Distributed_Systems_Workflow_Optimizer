import argparse
from pyspark.sql import SparkSession, functions as F, types as T

def run(edges_path, source, output_path, max_iters, partitions):
    spark = SparkSession.builder.appName("DijkstraSpark").getOrCreate()
    spark.conf.set("spark.sql.shuffle.partitions", str(partitions))

    edges_schema = T.StructType([
        T.StructField("src", T.StringType(), False),
        T.StructField("dst", T.StringType(), False),
        T.StructField("w", T.DoubleType(), False),
    ])
    edges = spark.read.option("header", True).schema(edges_schema).csv(edges_path).repartition(partitions).cache()

    vertices = edges.select("src").union(edges.select("dst")).distinct().withColumnRenamed("src", "id")
    inf = float("inf")
    dist = vertices.withColumn("dist", F.when(F.col("id")==F.lit(source), F.lit(0.0)).otherwise(F.lit(inf)))
    dist.persist()

    for _ in range(max_iters):
        msgs = edges.join(dist.withColumnRenamed("id","src_id").withColumnRenamed("dist","src_dist"),
                          edges.src==F.col("src_id")).select(F.col("dst").alias("id"),
                                                             (F.col("src_dist")+F.col("w")).alias("cand"))
        agg = msgs.groupBy("id").agg(F.min("cand").alias("cand"))
        joined = dist.join(agg, "id", "left").select("id", F.when(F.col("cand").isNull(), F.col("dist")).otherwise(F.least(F.col("dist"), F.col("cand"))).alias("new_dist"), F.col("dist").alias("old_dist"))
        changed = joined.filter(F.col("new_dist") != F.col("old_dist")).limit(1).count() > 0
        dist = joined.select(F.col("id"), F.col("new_dist").alias("dist"))
        dist.persist()
        if not changed:
            break

    dist.write.mode("overwrite").parquet(output_path)
    spark.stop()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--edges", required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--maxIters", type=int, default=50)
    p.add_argument("--partitions", type=int, default=200)
    args = p.parse_args()
    run(args.edges, args.source, args.output, args.maxIters, args.partitions)
