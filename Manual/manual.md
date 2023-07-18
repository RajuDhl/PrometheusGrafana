# Setting up things manually

For simplicity, set up a new folder so that you can have everything in one place. Creating sub-directory for each component might be helpful.

## prometheus server

Go to https://prometheus.io/download/ and download prometheus file for your OS.
Unzip the file into the new folder created.

Note: For Mac-OS, the OS type is Darwin

* PushGateway can be installed/run in the same way if required

## Grafana
Although Grafana is available as installer file and standalone binary for each OS, it is recommended to download standalone binaries for more versatility.

Go to https://grafana.com/grafana/download and download the standalone binary for your OS. Extract the contents in the new folder created.


## Prometheus Client
Prometheus client is installed as a python package
```shell
pip3 install prometheus-client
```

## Running Prometheus server
In the installation directory, open prometheus.yaml file and change the targets.
Alternatively, replace the content of file with the one provided with this documentation.
### Windows
Go to extracted folder and run prometheus.exe

### Mac-OS and Linux
IN the extracted directory, open terminal and run
```shell
./prometheus
```

Go to http://localhost:9090/ to verify

## Running Grafana server
### WIndows
In the extracted folder run bin/grafana-server.exe

### Mac-OS and Linux
```shell
./grafana-server
```

Go to http://localhost:3000/ to verify. For first run, the default username and password is `admin` and `admin`

## Visualizing data
To visualize data in grafana server, firstly data need to be available in prometheus client in the form of metrics. The data can then be pushed to prometheus server. For this prometheus server can be set to target the end point of prometheus client or exporter. 

