gpid=$(lsof -t -i :3000)
ppid=$(lsof -t -i :9090)

new_gpid=${gpid: -5}
new_ppid=${ppid: -5}

echo "$new_gpid"
echo "$new_ppid"

sudo kill "$new_gpid"
sudo kill "$new_ppid"
