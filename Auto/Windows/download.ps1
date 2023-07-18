# PowerShell script
$prometheus = "https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.windows-amd64.zip"
$grafana = "https://dl.grafana.com/enterprise/release/grafana-enterprise-10.0.2.windows-amd64.zip"

$prometheus_file = "prometheus.zip"
$grafana_file = "grafana.zip"

# Change to the Desktop directory in the user's profile
Set-Location $env:USERPROFILE\Desktop

# Create the PrometheusGrafana2 directory
mkdir "PrometheusGrafana" -Force
Set-Location "PrometheusGrafana"

# Create prometheus and grafana directories
#mkdir "prometheus" -Force
#mkdir "grafana" -Force

# Change to the prometheus directory and download Prometheus
Write-Host "Downloading Prometheus..."
Invoke-WebRequest -Uri $prometheus -OutFile $prometheus_file

Write-Host "Unzipping Prometheus..."
Expand-Archive -Path $prometheus_file -DestinationPath .\temp -Force
Get-ChildItem .\temp\* | Move-Item -Destination .\prometheus -Force
Remove-Item .\temp -Force -Recurse

# Change back to the parent directory
Set-Location ..

# Change to the grafana directory and download Grafana
Write-Host "Downloading Grafana..."
Invoke-WebRequest -Uri $grafana -OutFile $grafana_file
Expand-Archive -Path $grafana_file -DestinationPath .\temp -Force
Get-ChildItem .\temp\* | Move-Item -Destination .\grafana -Force
Remove-Item .\temp -Force -Recurse

# Change back to the parent directory
Set-Location ..
