import os
import glob
import yaml

# Get a list of all JSON files in the current directory
json_files = glob.glob('/home/ghost/Documents/.cloudflare/*.json')

# Check that we found exactly one JSON file
if len(json_files) != 1:
    print(f"Expected exactly one JSON file, but found {len(json_files)}")
    exit(1)

# Extract the filename from the path
json_file_name = os.path.basename(json_files[0])

# Get the environment variable RUNPOD_POD_ID
runpod_pod_id = os.getenv('RUNPOD_POD_ID')
if runpod_pod_id is None:
    print("Environment variable RUNPOD_POD_ID is not set")
    exit(1)

# Set up the content for the YAML file
yaml_content = {
    'tunnel': f'diffie_tunnel_{runpod_pod_id}',
    'credentials-file': json_file_name,
    'ingress': [
        {
            'hostname': 'api.diffusitron.net',
            'service': 'http://127.0.0.1:5000',
            'originRequest': {
                'httpHostHeader': 'api.diffusitron.net'
            }
        },
        {
            'service': 'http_status:404'
        }
    ]
}

# Write the YAML content to the config.yml file
with open('/home/ghost/Documents/.cloudflare/config.yml', 'w') as outfile:
    yaml.dump(yaml_content, outfile, default_flow_style=False)
