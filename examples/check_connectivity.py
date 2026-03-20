import json

import pypacs

if __name__ == '__main__':
    # TODO: provide the config file for the PACS you want to connect. see resources/conf_template.json for a config template
    conf_path = "path_to_config_file"

    with open(conf_path) as config_file:
        cfg = json.load(config_file)
    server_ip = cfg.get('server_ip')
    server_port = cfg.get('server_port')

    # check connectivity
    status = pypacs.verify_connectivity(server_ip, server_port)
    print("Connectivity status: ", status)

    print("DONE")
