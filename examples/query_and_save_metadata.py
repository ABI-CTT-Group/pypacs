import json
import os

import pypacs

if __name__ == '__main__':
    # TODO: provide the config file for the PACS you want to connect. see resources/conf_template.json for a config template
    conf_path = "path_to_config_file"

    save_dir = 'out/'
    save_filename = 'metadata.json'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    with open(conf_path) as config_file:
        cfg = json.load(config_file)
    server_ip = cfg.get('server_ip')
    server_port = cfg.get('server_port')
    aec = cfg.get('aec')

    # TODO. write your query here
    # You can query by most of the DICOM tags. E.g. PatientID, Modality, StudyInstanceUID, etc.
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
