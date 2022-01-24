import datetime
import shutil
import sys
from prometheus_pandas import query

# CONFIGURE HERE
PROMETHEUS_URL = "http://localhost:9090"

prometheus_queries = [
    "...",
    "..."
]

start_datetimes_unix = [1642845942, 1642845942]
end_datetimes_unix = [1642866627, 1642866627]
steps = ["15s", "15s"] # or 1m 


def load_prometheus_data(output_folder: str):


    """ Loads data from a PromQL-compatible datasource

    :param output_folder: The path to the output folder

    """

    p = query.Prometheus(PROMETHEUS_URL)

    # Request the data from Prometheus instance
    counter = 0
    for q in prometheus_queries:

        # split into hourly samples
        start_date = datetime.datetime.fromtimestamp(start_datetimes_unix[counter])
        end_date = datetime.datetime.fromtimestamp(end_datetimes_unix[counter])
        duration = end_date - start_date
        d_in_s = duration.total_seconds()
        hours_and_rest = divmod(d_in_s, 3600)
        hours = int(hours_and_rest[0])
        if hours_and_rest[1] != 0:
            hours += 1

        # Request the data from prometheus
        tf_start = start_date
        for i in range(hours):
            tf_end = tf_start + datetime.timedelta(hours=1)
            if tf_end > end_date:
                tf_end = end_date
            ts = p.query_range(query=q, start=tf_start, end=tf_end,
                               step=steps[counter])
            tf_start = tf_end
            file_name = output_folder + "ts_" + str(counter) + "_hour_" + str(i) + ".csv"
            ts.to_csv(file_name)
        counter += 1
    return


def to_zip_archive(output_folder):
    shutil.make_archive("output", 'zip', output_folder)


# Example Run: "python3 prometheus_2_csv.py output/"
if __name__ == "__main__":
    if len(sys.argv) == 2:
        load_prometheus_data(sys.argv[1])
        to_zip_archive(sys.argv[1])
