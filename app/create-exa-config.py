import requests
from requests import HTTPError
from gzip import BadGzipFile
import yaml
from jinja2 import Environment, FileSystemLoader
import os
import re

def get_mrt_file():
    """ Method to download RIS RAW DATA from internet and save them into bgp-view/(rrcXX folder)/latest-bview.gz
    
    Return nothing

    """
    # MRT Regex
    mrt_directory_regex = '(r{2}c{1}[0-9]{2})'


    # Load bgp.yaml file
    with open('bgp.yaml', 'r') as stream:
        try:
            input_bgp = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            print(f'Cannot parse yaml file {err}')
        finally:
            # Use MRT value into a loop to download each mrt file from internet and saving them into bgp-view/rrc<id> directory
            for mrt in input_bgp['mrts']:
                mrt_directory = re.search(mrt_directory_regex, mrt).group(1)
                os.mkdir(f'bgp-view/{mrt_directory}')
                print(f"Downloading archive {mrt_directory}, please wait...")
                try:
                    mrt_data = requests.get(mrt)
                except HTTPError as err:
                    print(f'%ERROR - Cannot download file located at {mrt}. HTTP Error: {err}')
                finally:
                    print("OK")  

                print(f"Save MRT file {mrt_directory}, please wait...")
                try:
                    with open(f'bgp-view/{mrt_directory}/latest-bview.gz', "wb") as file:
                        file.write(mrt_data.content)
                except PermissionError:
                    print("%ERROR, cannot open file, permission denied")
                finally:
                    print(f'OK')

def create_exa_config():
    """Method to create exabgp configuration files. 

        input files : bgp.yaml, bgp-view files
        output files : conf/exabgp.conf, conf/bgp-table-<router name>.py
    """
    # Load bgp.yaml file
    with open('bgp.yaml', 'r') as stream:
        try:
            input_bgp = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            print(f'Cannot parse yaml file {err}')
        finally:
            # Loading exabgp.conf.j2 template file
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('exabgp.conf.j2')

            # Merging template and bgp.yaml file into exabgp.conf
            with open(f"conf/exabgp.conf", 'w') as conf:
                conf.write(template.render(input_bgp))

            # For Each neighbor, creating the bgp view using mrt key inside the neighbor configuration. The mrt key value must match mrts directory created with get_mrt_file()
            for neighbor in input_bgp['neighbors']:
                print(f"Creating routing table for neighbor {neighbor['name']}, please wait...")
                os.system(f"python mrtparse/examples/mrt2exabgp.py -4 {neighbor['inetnexthop']} -6 {neighbor['inet6nexthop']} -P bgp-view/{neighbor['mrt']}/latest-bview.gz > conf/bgp-table-{neighbor['name']}.py")
                print(f"Routing table creation done for {neighbor['name']}")
            else:
                print("Routing table creation done")
def main():
    get_mrt_file()
    create_exa_config()
if __name__ == "__main__":
    main()