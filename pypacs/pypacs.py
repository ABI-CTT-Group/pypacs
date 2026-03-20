import os
import pypx
import json
from collections import OrderedDict


def verify_connectivity(server_ip, server_port):
    """
    Verify connectivity of the target PACS server

    :param server_ip: IP address of the target PACS
    :type server_ip: string
    :param server_port: port number of the target PACS
    :type server_port: string

    :return: connectivity status
    :rtype: string
    """
    pacs_settings = {
        'executable': '/usr/bin/echoscu',
        'serverIP': str(server_ip),
        'serverPort': str(server_port)
    }
    output = pypx.echo(pacs_settings)
    print(output)
    return output['status']


def get_metadata(server_ip, server_port, aec, query_settings):

    """
    get metadata beased on query settings

    :param server_ip: IP address of the target PACS
    :type server_ip: string
    :param server_port: port number of the target PACS
    :type server_port: string
    :param aec: the called AE title
    :type aec: string
    :param query_settings: query
    :type query_settings: dict

    :return: metadata
    :rtype: dict
    """
    pacs_settings = {
        'executable': '/usr/bin/findscu',
        'serverIP': str(server_ip),
        'serverPort': str(server_port),
        'aec': aec
    }

    output_settings = {
        'printReport': 'json',
        'colorize': 'dark'
    }

    opt = {**pacs_settings, **query_settings, **output_settings}
    metadata = pypx.find(opt)

    return metadata


def save_metadata(metadata, save_path):
    """
    Write metadata to file

    :param metadata: metadata
    :type metadata: dict
    :param save_path: path to the target file
    :type save_path: string

    :return:
    :rtype:
    """
    dir_path = os.path.dirname(save_path)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    with open(save_path, "w") as write_file:
        json.dump(metadata, write_file, indent=4)


def move_files(server_ip, server_port, aec, aet, query_settings):
    """
    Download files

    :param server_ip: IP address of the target PACS
    :type server_ip: string
    :param server_port: port number of the target PACS
    :type server_port: string
    :param aec: the called AE title
    :type aec: string
    :param aet: the calling AE title
    :type aet: string
    :param query_settings: query
    :type query_settings: dict

    :return:
    :rtype:
    """
    pacs_settings = {
        'executable': '/usr/bin/movescu',
        'serverIP': str(server_ip),
        'serverPort': str(server_port),
        'aec': str(aec),
        'aet': str(aet)
    }

    opt = {**pacs_settings, **query_settings}
    output = pypx.move(opt)
    print(output)


def get_total_num_of_slices(metadata):
    """
    Calculate the total number of slices

    :param metadata: metadata
    :type metadata: dict
    :return: number of files
    :rtype: int
    """
    num_of_slices = 0
    studies = metadata['data']
    for study in studies:
        series = study['series']
        for s in series:
            num_of_slices = num_of_slices + int(s['NumberOfSeriesRelatedInstances']['value'])
    return num_of_slices


def filter_by_extra_conditions(metadata, extra_query):
    """
    Filter the query results by extra conditions

    :param metadata: metadata/query result
    :type metadata: dict
    :param extra_query: filter
    :type extra_query: dict

    :return:
    :rtype:
    """
    studies = metadata['data']

    for item in extra_query:
        tag = item.get('tag')
        operator = item.get('operator')
        value = item.get('value')

        if tag == "NumberOfSeriesRelatedInstances":
            for study_idx, study in enumerate(studies):
                if "series" in study:
                    if operator == ">":
                        series = [s for s in study["series"] if int(s[tag]["value"]) > value]
                    elif operator == ">=":
                        series = [s for s in study["series"] if int(s[tag]["value"]) >= value]
                    elif operator == "==":
                        series = [s for s in study["series"] if int(s[tag]["value"]) == value]
                    elif operator == "<":
                        series = [s for s in study["series"] if int(s[tag]["value"]) < value]
                    elif operator == "<=":
                        series = [s for s in study["series"] if int(s[tag]["value"]) <= value]
                    elif operator == "!=":
                        series = [s for s in study["series"] if int(s[tag]["value"]) != value]
                    else:
                        series = study["series"]
                    study["series"] = series
                    studies[study_idx] = study
            # delete studies if length of series == 0
            studies = [study for study in studies if len(study["series"]) > 0]
            metadata['data'] = studies
    return metadata


def create_custom_report(metadata, fields=None, custom_fields=None):
    """
    Create custom report for the metadata

    :param metadata: metadata/query result
    :type metadata: dict
    :param fields: fields for different query levels (patient, study or series)
    :type fields: dict
    :param custom_fields: a list of custom fields which do not provided by the metadata directly might need to be calculated or queried separately.
    :type custom_fields: list
    :return:
    :rtype:
    """
    # TODO. the fields in the report are customisable by providing/modifying the variable "fields"
    if fields is None:
        fields = {
            "patient":
                ["PatientName", "PatientID", "PatientBirthDate", "PatientAge", "PatientSex"],
            "study":
                ["StudyInstanceUID", "StudyDate", "ModalitiesInStudy", "StudyDescription"],
            "series":
                ["SeriesDate", "Modality", "SeriesDescription", "SeriesInstanceUID", "NumberOfSeriesRelatedInstances"]
        }

    report = OrderedDict()

    studies = metadata['data']
    for study in studies:
        # get patient id
        patient_id = study["PatientID"]["value"]
        if not (patient_id in report):
            report[patient_id] = OrderedDict()
            report[patient_id]["study"] = OrderedDict()

        # get study id
        study_id = study["StudyInstanceUID"]["value"]
        if not (patient_id in report[patient_id]["study"]):
            report[patient_id]["study"][study_id] = OrderedDict()

        for key in study:
            # get patient info
            if key in fields["patient"]:
                report[patient_id][key] = study[key]["value"]
            # get study info
            if key in fields["study"]:
                report[patient_id]["study"][study_id][key] = study[key]["value"]

        if "series" in study:
            report[patient_id]["study"][study_id]["series"] = OrderedDict()
            for series in study["series"]:
                # get series id
                series_id = series["SeriesInstanceUID"]["value"]
                if not (series_id in report[patient_id]["study"][study_id]["series"]):
                    report[patient_id]["study"][study_id]["series"][series_id] = OrderedDict()

                for key_in_series in series:
                    # get series info
                    if key_in_series in fields["series"]:
                        report[patient_id]["study"][study_id]["series"][series_id][key_in_series] = \
                            series[key_in_series]["value"]

    # reorder
    for patient_id in report:
        report[patient_id].move_to_end("study")

    return report
