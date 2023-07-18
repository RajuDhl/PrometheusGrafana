#!/bin/bash

# Script: download.sh
# Description: This script installs required components based on OS in linux and mac distributions
# Author: Raju Dahal
# Date: 2023-07-18

# Index for variable names:
# pl -> Prometheus for Linux
# pm -> Prometheus for Mac
# gl -> Grafana for Linux
# gm -> Grafana for Mac
# pf -> File name for downloaded prometheus file
# gf -> File name for downloaded grafana file

# pr -> required prometheus file based on OS
# gr -> required grafana file based on OS

pl="https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz"
pm="https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.darwin-amd64.tar.gz"

gl="https://dl.grafana.com/enterprise/release/grafana-enterprise-10.0.2.linux-amd64.tar.gz"
gm="https://dl.grafana.com/enterprise/release/grafana-enterprise-10.0.2.darwin-amd64.tar.gz"

pf="prometheus.tar.gz"
gf="grafana.tar.gz"

OS=$(uname -s)
if [ "$OS" == "Linux" ]; then
  echo "Linuz"
  pr=$pl
  gr=$gl
else
  pr=$pm
  gr=$gm
fi

cd ~
mkdir -p prometheus-Grafana
cd prometheus-Grafana
mkdir -p prometheus
mkdir -p grafana

wget -O "$pf" "$pr"
wget -O "$gf" "$gr"


tar -xvf $gf --strip-components=1 -C grafana
tar -xvf $pf --strip-components=1 -C prometheus




