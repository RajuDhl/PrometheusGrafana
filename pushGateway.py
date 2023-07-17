"""
This code snippet demonstrates how to create and update a Gauge metric using the Prometheus Python client library.
"""
from prometheus_client import start_http_server, Gauge, CollectorRegistry, push_to_gateway
import time

# initialize start_time variable to record function starting time
start_time = time.time()


def test_push_to_gateway(value):
    """
    Args:
         gauge_metric: name of the gauge metric being created
         registry: name of the registry
    Returns:
       Returns a success message after successfully running for 100 seconds
    Raises:
          Server Creation Error with related error message
    """
    try:
        # CollectorRegistry class to manage the registry of metrics.
        registry = CollectorRegistry()

        # Create a Gauge metric
        gauge_metric = Gauge(
            'my_gauge_metric',
            'Test gauge metric',
            registry=registry)

        # Update the gauge metric value
        while True:
            gauge_metric.set(value)
            push_to_gateway('localhost:9091', job='test_job', registry=registry)
            time.sleep(5)  # Sleep for 5 second

            # exit the loop after 100 seconds
            if time.time() - start_time >= 100:
                break
        return "Bla Bla Bla"
    except Exception as e:
        print("Exception occurred =>", str(e))


print(test_push_to_gateway(100))
