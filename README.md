# Prometheus-2-CSV
Exports Prometheus queries to multiple csv files. 
Why multiple csv files? - Because prometheus can only export 11.000 datapoints at once, so for ever hour a single request is done and a single CSV file is written.

## Usage

1. Configure Prometheus-Url (or PromQL-compatible datasource, like Thanos) 
2. Configure queries in `prometheus_queries`
3. Configure the starting dates of every query as unix timestamps in `start_datetimes_unix`
4. Configure the ending dates of every query as unix timestamps in `end_datetimes_unix`
5. Configure the step size for every query in `steps`

Important: Unix timestamps, not millisecond timestamps, and that all configurable lists need to have the same amount of values inside.

Execute the script: 
```shell
python3 prometheus_2_csv.py output/
```

The output can be found under `output/`, and a zip-file `output.zip` is created (contains all csv files)