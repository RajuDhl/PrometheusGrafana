Set-Location $env:USERPROFILE\Desktop\PrometheusGrafana

$prometheus = "prometheus\prometheus.exe"
$grafana = "grafana\bin\grafana-server.exe"

Set-Location prometheus

Start-Process .\prometheus.exe

Set-Location ..\grafana\bin


Start-Process .\grafana-server.exe

#Start-Process -FilePath $prometheus -Wait
#Start-Process -FilePath $grafana



