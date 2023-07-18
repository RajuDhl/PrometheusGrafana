Prometheus and grafana are also available as docker images

### Running Prometheus
```shell
docker run \
    -p 9090:9090 \
    -v /path/to/prometheus.yml:/etc/prometheus \ #replace path to config with path to prometheus.yaml file provided with the code
    prom/prometheus
```

### Running Grafana
```shell
docker run -d --name=grafana -p 3000:3000 grafana/grafana-enterprise
```