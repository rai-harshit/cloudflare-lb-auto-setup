import requests
import json
import os
import glob

def attach_monitor_to_pool(account_identifier, account_email, api_key, pool_id, monitor_id, tunnel_name, tunnel_endpoint):
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_identifier}/load_balancers/pools/{pool_id}"

    headers = {
    'Content-Type': 'application/json',
    'X-Auth-Email': account_email,
    'X-Auth-Key': api_key 
    }

    data = {
        'monitor': monitor_id,
        'origins': [
            {
                "address": tunnel_endpoint,
                "enabled": True,
                "header": {
                    "Host": [
                        "api.diffusitron.net"
                    ]
                },
                "name": tunnel_name,
                "weight": 1
            }
        ] 
    }
    print(data)
    response = requests.request("PATCH", url, headers=headers, data=json.dumps(data))

    print(response.text)

def get_pool_id_from_name(account_identifier, account_email, api_key, pool_name):

    url = f"https://api.cloudflare.com/client/v4/accounts/{account_identifier}/load_balancers/pools"

    headers = {
    'Content-Type': 'application/json',
    'X-Auth-Email': account_email,
    'X-Auth-Key': api_key,
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    for pool in data['result']:
        if pool['name'] == pool_name:
            # print(f"The ID of the pool named '{pool_name}' is {pool['id']}")
            return pool['id']
    else:
        print(f"No pool found with the name '{pool_name}'")

def get_monitors(account_identifier, account_email, api_key, monitor_name):
    url = f'https://api.cloudflare.com/client/v4/accounts/{account_identifier}/load_balancers/monitors'
    headers = {
    'Content-Type': 'application/json',
    'X-Auth-Email': account_email,
    'X-Auth-Key': api_key,
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    for monitor in data['result']:
        if monitor['description'] == monitor_name:
            # print(f"The ID of the monitor named '{monitor_name}' is {monitor['id']}")
            return monitor['id']
    else:
        print(f"No pool found with the name '{monitor_name}'")

if __name__ == "__main__":
    account_identifier = os.environ['CLOUDFLARE_ACCOUNT_ID']
    account_email = os.environ['CLOUDFLARE_ACCOUNT_EMAIL']
    api_key = os.environ['CLOUDFLARE_API_KEY']
    monitor_name = 'mon-1'
    pool_name = "pool_" + os.environ['RUNPOD_POD_ID']
    tunnel_name = "diffie_tunnel_" + os.environ['RUNPOD_POD_ID']
    json_files = glob.glob('/workspace/.cloudflare/*.json')
    tunnel_endpoint = os.path.basename(json_files[0]).split(".")[0] + ".cfargotunnel.com"
    pool_id = get_pool_id_from_name(account_identifier, account_email, api_key, pool_name)
    print(pool_id)
    monitor_id = get_monitors(account_identifier, account_email, api_key, monitor_name)
    print(monitor_id)
    attach_monitor_to_pool(account_identifier, account_email, api_key, pool_id, monitor_id, tunnel_name, tunnel_endpoint)
