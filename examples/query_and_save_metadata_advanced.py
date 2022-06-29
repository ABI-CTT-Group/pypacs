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

    # TODO. write your query & query filter here.
    query_settings = {
        'PatientID': 'VL00001',
        'Modality': 'MR'
    }
    # # TODO. filter by extra query
    extra_query = [
        # NumberOfSeriesRelatedInstances
        {
            'tag': 'NumberOfSeriesRelatedInstances',
            'operator': '>',
            'value': 100
        }
    ]

    # get metadatass
    metadata = pypacs.get_metadata(server_ip, server_port, aec, query_settings)
    metadata = pypacs.filter_by_extra_conditions(metadata, extra_query)

    report = pypacs.create_custom_report(metadata)

    # save custom report
    save_path = os.path.join(save_dir, save_filename)
    pypacs.save_metadata(report, save_path)

    print("DONE")
