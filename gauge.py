"""
This code snippet demonstrates how to create and update a Gauge metric using the Prometheus Python client library.
"""
from prometheus_client import start_http_server, Gauge
import time

# initialize start_time variable to record function starting time
start_time = time.time()


def test_gauge(value):
    """
    Start an HTTP server on port 8000 and set a gauge value of 100 to be sent on the server
    Args:
         gauge_metric: name of the gauge metric being created
    Returns:
       Returns a success message after successfully running for 100 seconds
    Raises:
          Server Creation Error with related error message
    """
    try:
        # Create a Gauge metric
        gauge_metric = Gauge(
            'my_gauge_metric',
            'Test gauge metric',
            ['label_name1', 'label_name2']
        )

        # Start an HTTP server on port 8001
        start_http_server(8001)

        # Update the gauge metric value
        while True:
            # gauge_metric.set(value)  # Update the value
            gauge_metric.labels(label_name1='value1', label_name2='value2').set(40)
            time.sleep(1000)  # Sleep for 1 second

            # exit the loop after 100 seconds
            if time.time() - start_time >= 100:
                break

            return "Successfully created prometheus server on port 8000"

    except Exception as e:
        print(str(e))


print(test_gauge(1))
