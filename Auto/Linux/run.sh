cd ~/prometheus-Grafana

cd grafana
./bin/grafana-server > grafana.log 2>&1 &

cd ../prometheus
./prometheus > prometheus_server.log 2>&1 &