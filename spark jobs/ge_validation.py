def validate_data():
    from pyspark.sql import SparkSession
    import great_expectations as gx
    from great_expectations.dataset import SparkDFDataset
    from great_expectations.render.renderer import ValidationResultsPageRenderer
    from great_expectations.render.view import DefaultJinjaPageView
    import os

    # 🚀 تشغيل Spark
    spark = SparkSession.builder.appName("Validation").getOrCreate()

    # 📥 قراءة البيانات من HDFS
    df = spark.read.option("header", True).csv("hdfs://namenode:8020/wuzzuf_output/Wuzzuf_data_transformed")

    # ✅ Great Expectations التحقق باستخدام
    ge_df = SparkDFDataset(df)
    ge_df._initialize_expectations(expectation_suite_name="scraping_suite")
    ge_df.expect_column_values_to_not_be_null("id")
    ge_df.expect_column_values_to_be_unique("id")
    ge_df.expect_column_values_to_not_be_null("job_title")
    ge_df.expect_column_values_to_not_be_null("company_name")
    results = ge_df.validate()

    # 📝 كتابة التقرير في نفس المسار اللي معمول له mount
    #report_path = "/opt/airflow/validation_report/validation_report.html"
    report_path = "/opt/bitnami/spark/validation_report/validation_report.html"


    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    document_model = ValidationResultsPageRenderer().render(results)
    html_report = DefaultJinjaPageView().render(document_model)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_report)
