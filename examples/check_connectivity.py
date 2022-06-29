import json

import pypacs

if __name__ == '__main__':
    # TODO: provide the information of the PACS system you want to interact with.
    #       make sure the pacs is up and running before executing the script
    server_ip = ""
    server_port = ""

    # check connectivity
    status = pypacs.verify_connectivity(server_ip, server_port)
    print("Connectivity status: ", status)
