cd /workspace
export TUNNEL_ORIGIN_CERT="/workspace/.cloudflare/cert.pem"
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && dpkg -i cloudflared-linux-amd64.deb
cloudflared tunnel create "diffie_tunnel_$RUNPOD_POD_ID"
python3 .cloudflare/generate_config_json.py
cloudflared tunnel route lb "diffie_tunnel_$RUNPOD_POD_ID" api.diffusitron.net "pool_$RUNPOD_POD_ID"
cd .cloudflare
tmux new-session -d -s cloudflare_tunnel 'cloudflared tunnel --config /workspace/.cloudflare/config.yml run'
cd /workspace
python3 .cloudflare/update_pool.py