# Setting up things manually

For simplicity, set up a new folder so that you can have everything in one place. Creating sub-directory for each component might be helpful.

## prometheus server

Go to https://prometheus.io/download/ and download prometheus file for your OS.
Unzip the file into the new folder created.

Note: For Mac-OS, the OS type is Darwin

## Grafana
Although Grafana is available as installer file and standalone binary for each OS, it is recommended to download standalone binaries for more versatility.

Go to https://grafana.com/grafana/download and download the standalone binary for your OS. Extract the contents in the new folder created.


## Prometheus Client
```shell
pip3 install prometheus-client
```

