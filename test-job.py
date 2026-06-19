import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, round


def main():
    # 1. Initialize SparkSession (The entry point for the job)
    spark = SparkSession.builder.appName("SampleETLJob").getOrCreate()

    # Set log level to see warnings and errors clearly
    spark.sparkContext.setLogLevel("WARN")

    try:
        print("Starting PySpark Job...")

        # 2. Extract: Read data (e.g., from a CSV or Parquet file)
        # Replacing with inline mock data for immediate testing
        data = [
            ("Alice", "Engineering", 75000),
            ("Bob", "Engineering", 80000),
            ("Charlie", "Marketing", 60000),
            ("David", "Marketing", 65000),
            ("Eve", "Sales", 70000),
        ]
        columns = ["employee_name", "department", "salary"]
        df = spark.createDataFrame(data, schema=columns)

        print("Raw Data:")
        df.show()

        # 3. Transform: Group data and find average salary per department
        transformed_df = (
            df.groupBy("department")
            .agg(round(avg("salary"), 2).alias("average_salary"))
            .filter(col("average_salary") >= 65000)
            .orderBy(col("average_salary").desc())
        )

        print("Transformed Data:")
        transformed_df.show()

        # 4. Load: Write the results out (e.g., Parquet format)
        # In production, use paths like "s3a://my-bucket/output/"
        output_path = "output/department_salaries"

        transformed_df.write.mode("overwrite").parquet(output_path)

        print(f"Job successfully completed. Output written to {output_path}")

    except Exception as e:
        print(f"Job failed with error: {str(e)}")
        sys.exit(1)

    finally:
        # 5. Stop the session to free cluster resources
        spark.stop()


if __name__ == "__main__":
    main()
