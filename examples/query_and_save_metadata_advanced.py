import json
import os

from pypacs.pypacs import get_metadata, create_custom_report, save_metadata, filter_by_extra_conditions

if __name__ == '__main__':
    save_dir = 'out/'
    save_filename = 'metadata.json'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # TODO: get the config file of the pacs you want to access
    conf_path = "../resources/conf_dcm4chee_bioeng100.json"

    with open(conf_path) as config_file:
        cfg = json.load(config_file)
    server_ip = cfg.get('server_ip')
    server_port = cfg.get('server_port')
    aec = cfg.get('aec')

    # TODO. write your query here.
    query_settings = {
        'PatientID': 'VL00001',
        'Modality': 'MR'
    }

    # get metadata
    metadata = get_metadata(server_ip, server_port, aec, query_settings)

    # # TODO. filter by extra query
    extra_query = [
        # NumberOfSeriesRelatedInstances
        {
            'tag': 'NumberOfSeriesRelatedInstances',
            'operator': '>',
            'value': 100
        }
    ]

    metadata = filter_by_extra_conditions(metadata, extra_query)

    report = create_custom_report(metadata)

    # save custom report
    save_path = os.path.join(save_dir, save_filename)
    save_metadata(report, save_path)

    print("DONE")