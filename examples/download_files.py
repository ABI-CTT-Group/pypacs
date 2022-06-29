"""
Retrieve data from the pacs of your choose (sender) and send to another pacs (receiver).

This script is an example of downloading the dicom images from the pacs on bioeng100 to the breast eResearch drive.
The images will go to "<eResearch>/sandbox/dicom_node/"

If you want to download the images to your local machine, see below:
    1. Make sure both the sender and receiver nodes are running before sending files.
       Below are the steps to set up a receiver node using storescp:
        1. (optional) you need have dcmtk package installed:
            - sudo apt-get update
            - sudo apt-get install -y dcmtk
        2. Create a folder as the dicom node
        3. Open a terminal from the dicom node folder
        4. Run:
            - sudo storescp -v <portNumber> -tos 3 -dhl -ss dcm -tn

    2. The receiver node/pacs needs to be configured properly in the sender pacs on the AE management page/configuration file.
       Below are the steps to add a receiver node to the DCM4CHEE PACS on bioeng100:
        1. On the PACS GUI, click the 'AE Management' tab on the navigation bar
        2. Click the 'new AET' bottom on the first right column
        3. Enter "AE Title", "Hostname"(the ip address of the receiver node) & "Port"(the port number of the receiver node)
        4. Click "echo" to check connectivity, then click "create".
"""

import json

import pypacs

if __name__ == '__main__':
    # TODO: provide the information of the PACS system you want to interact with.
    #       make sure the pacs is up and running before executing the script
    server_ip = ""
    server_port = ""
    aec = ""
    aet = ""

    # TODO. write your query here.
    # Currently, you have to provide StudyInstanceUID and SeriesInstanceUID.
    # Future improvement: allow user to send data from patient, study, series or image levels.
    query_settings = {
        'StudyInstanceUID': '1.3.12.2.1107.5.2.30.25138.30000006060122155281200000007',
        'SeriesInstanceUID': '1.3.12.2.1107.5.2.30.25138.30000006060120104693700002235'
    }

    pypacs.move_files(server_ip=server_ip, server_port=server_port, aec=aec, aet=aet, query_settings=query_settings)

    print("DONE")

