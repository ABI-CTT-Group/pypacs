import json
import os

import pypacs

if __name__ == '__main__':
    # TODO: provide the information of the PACS system you want to interact with.
    #       make sure the pacs is up and running before executing the script
    server_ip = ""
    server_port = ""
    aec = ""

    save_dir = 'out/'
    save_filename = 'metadata.json'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # TODO. write your query here
    #       You can query by most of the DICOM tags. E.g. PatientID, Modality, StudyInstanceUID, etc.
    query_settings = {
        'PatientID': 'VL00001',
        'Modality': 'MR'
    }
    # query_settings = {
    #     'PatientID': 'VL*'
    # }

    # get metadata
    metadata = pypacs.get_metadata(server_ip, server_port, aec, query_settings)

    report = pypacs.create_custom_report(metadata)
    # save custom report
    save_path = os.path.join(save_dir, save_filename)
    pypacs.save_metadata(report, save_path)

    print("DONE")
