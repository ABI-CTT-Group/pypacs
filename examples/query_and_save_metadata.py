"""
Query a remote Orthanc DICOM server using pypx (via pypacs wrapper).

Reads connection settings from configs/config_uoa471493.json and queries
the Orthanc server running at 130.216.253.184:4242.

Usage:
    cd my_workspace
    python query_and_save_metadata.py
"""

import json
import os
import sys

import pypacs


def load_config(conf_path):
    """Load PACS connection config from JSON file."""
    with open(conf_path) as f:
        return json.load(f)


def main():
    # ── Configuration ──────────────────────────────────────────────────
    conf_path = "path_to_config_file"
    cfg = load_config(conf_path)

    server_ip = cfg["server_ip"]
    server_port = cfg["server_port"]
    aec = cfg["aec"]
    aet = cfg.get("aet")

    save_dir = os.path.join(os.path.dirname(__file__), "out")
    save_filename = "metadata.json"
    os.makedirs(save_dir, exist_ok=True)

    # ── Step 1: Verify connectivity (DICOM C-ECHO) ────────────────────
    print(f"Checking connectivity to {server_ip}:{server_port} …")
    status = pypacs.verify_connectivity(server_ip, server_port)
    print(f"Connectivity status: {status}")
    if status != "success":
        print("ERROR: Cannot reach PACS server. Aborting.")
        sys.exit(1)

    # ── Step 2: Define query ───────────────────────────────────────────
    # Query all patients (use wildcard).
    # You can narrow the search by specifying DICOM tags, e.g.:
    #   PatientID, PatientName, Modality, StudyDate,
    #   StudyInstanceUID, SeriesInstanceUID, etc.
    # query_settings = {
    #     "PatientID": "*",        # wildcard: all patients
    #     "aet": aet               # injected calling AET
    # }
    query_settings = {
        "PatientID": "*",        # wildcard: all patients
        "aet": aet               # injected calling AET
    }

    # Examples of more specific queries:
    # query_settings = {
    #     "PatientID": "VL00001",
    #     "Modality": "MR",
    # }
    # query_settings = {
    #     "StudyInstanceUID": "1.3.6.1.4.1.14519.5.2.1.7009.2406.941409355639310066701665617488",
    # }
    # query_settings = {
    #     "SeriesInstanceUID": "1.3.6.1.4.1.14519.5.2.1.7009.2406.277304413291607535957606464849",
    # }

    # ── Step 3: Query (DICOM C-FIND) ──────────────────────────────────
    print(f"Querying PACS (aec={aec}, aet={aet}) with: {query_settings}")
    metadata = pypacs.get_metadata(server_ip, server_port, aec, query_settings)
    print(json.dumps(metadata, indent=2))

    if metadata.get("status") == "error":
        print("ERROR: C-FIND query failed. Please check your AET/AEC configuration and Orthanc logs.")
        sys.exit(1)

    # ── Step 4: Build report and save ─────────────────────────────────
    report = pypacs.create_custom_report(metadata)
    save_path = os.path.join(save_dir, save_filename)
    pypacs.save_metadata(report, save_path)
    print(f"\nReport saved to {save_path}")

    print("DONE")


if __name__ == "__main__":
    # ── Configuration ──────────────────────────────────────────────────
    # TODO. provide the config file for the PACS you want to connect. see resources/conf_template.json for a config template
    conf_path = "resources/conf_template.json"
    cfg = load_config(conf_path)

    server_ip = cfg["server_ip"]
    server_port = cfg["server_port"]
    aec = cfg["aec"]
    aet = cfg.get("aet")

    save_dir = os.path.join(os.path.dirname(__file__), "out")
    save_filename = "metadata.json"
    os.makedirs(save_dir, exist_ok=True)

    # ── Step 1: Verify connectivity (DICOM C-ECHO) ────────────────────
    print(f"Checking connectivity to {server_ip}:{server_port} …")
    status = pypacs.verify_connectivity(server_ip, server_port)
    print(f"Connectivity status: {status}")
    if status != "success":
        print("ERROR: Cannot reach PACS server. Aborting.")
        sys.exit(1)

    # ── Step 2: Define query ───────────────────────────────────────────
    # Query all patients (use wildcard).
    # You can narrow the search by specifying DICOM tags, e.g.:
    #   PatientID, PatientName, Modality, StudyDate,
    #   StudyInstanceUID, SeriesInstanceUID, etc.
    # query_settings = {
    #     "PatientID": "*",        # wildcard: all patients
    #     "aet": aet               # injected calling AET
    # }
    query_settings = {
        "PatientID": "VL00001",        # wildcard: all patients
        "aet": aet               # injected calling AET
    }

    # Examples of more specific queries:
    # query_settings = {
    #     "PatientID": "VL00001",
    #     "Modality": "MR",
    # }
    # query_settings = {
    #     "StudyInstanceUID": "1.3.6.1.4.1.14519.5.2.1.7009.2406.941409355639310066701665617488",
    # }
    # query_settings = {
    #     "SeriesInstanceUID": "1.3.6.1.4.1.14519.5.2.1.7009.2406.277304413291607535957606464849",
    # }

    # ── Step 3: Query (DICOM C-FIND) ──────────────────────────────────
    print(f"Querying PACS (aec={aec}, aet={aet}) with: {query_settings}")
    metadata = pypacs.get_metadata(server_ip, server_port, aec, query_settings)
    print(json.dumps(metadata, indent=2))

    if metadata.get("status") == "error":
        print("ERROR: C-FIND query failed. Please check your AET/AEC configuration and Orthanc logs.")
        sys.exit(1)

    # # # TODO. filter by extra query
    # extra_query = [
    #     # NumberOfSeriesRelatedInstances
    #     {
    #         'tag': 'NumberOfSeriesRelatedInstances',
    #         'operator': '>',
    #         'value': 100
    #     }
    # ]
    # metadata = pypacs.filter_by_extra_conditions(metadata, extra_query)

    # ── Step 4: Build report and save ─────────────────────────────────
    report = pypacs.create_custom_report(metadata)
    save_path = os.path.join(save_dir, save_filename)
    pypacs.save_metadata(report, save_path)
    print(f"\nReport saved to {save_path}")

    print("DONE")