from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("My First Spark Job") \
    .getOrCreate()

data = [
    ("Great product",),
    ("Battery is terrible",),
    ("Fast delivery",)
]

df = spark.createDataFrame(data, ["review"])

df.show()

spark.stop()