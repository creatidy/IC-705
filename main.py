import xml.etree.ElementTree as ET
import csv
from typing import Any
import regex as re
from decimal import Decimal
from unidecode import unidecode


# The script reads the data from the XML file and exports it to the CSV file

# The XML file contains information about the repeaters. 
# The source of the XML file is http://przemienniki.net/
xml_file_path = '../data/rxf.xml'

# The CSV file format is compatible with the ICOM IC-705.
# Upload the file to the radio using SD Card.
repeaters_file_path = '../data/repeaters.csv'

# Filters for the repeaters
country = ['pl']
mode = ['FM', "DSTAR", "FMLINK"]
band = ['70CM', '2M']


def main():
    try:
        tree = ET.parse(xml_file_path)
        rxf = tree.getroot()
    except Exception as e:
        print(f"An error occurred while reading the XML file: {e}")
        return

    dictionary = rxf.find('dictionary')
    if dictionary is None:
        raise Exception('Dictionary is missing in the XML file')

    # Create a dictionary of items
    items = {}
    for item in dictionary.findall('item'):
        if item.find('type') is None:
            raise Exception('Type is missing in the item')
        type = item.find('type').text
        name = item.find('name').text
        value = item.find('value').text 
        description = item.find('description').text
        items[name] = {
            'type': type,
            'value': value,
            'description': description
        }

    # Create a list of repeaters
    repeaters = rxf.find('repeaters')
    if repeaters is None:
        raise Exception('Repeaters are missing in the XML file')

    repeaters_list: list[dict[str, Any]] = []
    for repeater in repeaters.findall('repeater'):
        status = repeater.find('status').text  # type: ignore
        if status not in ['WORKING']:
            continue
        latitude = repeater.find('location/latitude').text if repeater.find('location/latitude') is not None else None  # type: ignore
        if latitude is None:
            continue
        longitude = repeater.find('location/longitude').text if repeater.find('location/longitude') is not None else None  # type: ignore
        if longitude is None:
            continue
        qra = repeater.find('qra').text  # type: ignore
        id = repeater.find('id').text  # type: ignore
        hash = repeater.find('hash').text  # type: ignore
        created = repeater.find('created').text  # type: ignore
        updated = repeater.find('updated').text  # type: ignore
        statusInt = repeater.find('statusInt').text  # type: ignore
        licenseExpiryDate = repeater.find('licenseExpiryDate').text if repeater.find('licenseExpiryDate') is not None else None  # type: ignore
        modeInt = repeater.find('modeInt').text  # type: ignore
        mode = repeater.find('mode').text  # type: ignore
        bandInt = repeater.find('bandInt').text  # type: ignore
        band = repeater.find('band').text  # type: ignore
        qrg_rx = repeater.find('qrg[@type="rx"]').text  # type: ignore
        qrg_tx = repeater.find('qrg[@type="tx"]').text  # type: ignore
        country = repeater.find('country').text  # type: ignore
        qth = repeater.find('qth').text  # type: ignore
        locator = repeater.find('location/locator').text  # type: ignore
        altitudeOverSea = repeater.find('location/altitudeOverSea').text if repeater.find('location/altitudeOverSea') is not None else None  # type: ignore
        altitudeOverGround = repeater.find('location/altitudeOverGround').text if repeater.find('location/altitudeOverGround') is not None else None  # type: ignore
        activationInt = repeater.find('activationInt').text  # type: ignore
        activation = repeater.find('activation').text  # type: ignore
        ctcss_rx = repeater.find('ctcss[@type="rx"]').text if repeater.find('ctcss[@type="rx"]') is not None else None  # type: ignore
        ctcss_tx = repeater.find('ctcss[@type="tx"]').text if repeater.find('ctcss[@type="tx"]') is not None else None  # type: ignore
        trxPower = repeater.find('trxPower').text if repeater.find('trxPower') is not None else None  # type: ignore
        operator = repeater.find('operator').text if repeater.find('operator') is not None else None  # type: ignore
        remarks = repeater.find('remarks').text if repeater.find('remarks') is not None else None  # type: ignore
        link = repeater.find('link').text  # type: ignore
        source = repeater.find('source').text  # type: ignore
        feedback = repeater.find('feedback').text  # type: ignore
        repeaters_list.append({
            'qra': qra,
            'id': id,
            'hash': hash,
            'created': created,
            'updated': updated,
            'statusInt': statusInt,
            'status': status,
            'licenseExpiryDate': licenseExpiryDate,
            'modeInt': modeInt,
            'mode': mode,
            'band': band,
            'qrg_rx': qrg_rx,
            'qrg_tx': qrg_tx,
            'country': country,
            'qth': qth,
            'locator': locator,
            'latitude': latitude,
            'longitude': longitude,
            'altitudeOverSea': altitudeOverSea,
            'altitudeOverGround': altitudeOverGround,
            'activationInt': activationInt,
            'activation': activation,
            'ctcss_rx': ctcss_rx,
            'ctcss_tx': ctcss_tx,
            'trxPower': trxPower,
            'operator': operator,
            'remarks': remarks,
            'link': link,
            'source': source,
            'feedback': feedback
        })

    # Filter repeaters by the country
    repeaters_list = [repeater for repeater in repeaters_list if repeater['country'] in country]

    # Filter repeaters by the mode
    repeaters_list = [repeater for repeater in repeaters_list if repeater['mode'] in mode]

    # Filter repeaters by the band
    repeaters_list = [repeater for repeater in repeaters_list if repeater['band'] in band]

    repeaters_list = sorted(repeaters_list, key=lambda x: x['qra'])

    # Export repeaters to the CSV file

    # Example file format:
    # Group No,Group Name,Name,Sub Name,Repeater Call Sign,Gateway Call Sign,Frequency,Dup,Offset,Mode,TONE,Repeater Tone,RPT1USE,Position,Latitude,Longitude,UTC Offset
    # 0,Poland,Moszna-Parcela,Poland,SR5WC  B,SR5WC  G,438.600000,DUP-,7.600000,DV,OFF,88.5Hz,YES,Approximate,52.180000,20.750000,+1:00
    # 0,Poland,W-wa Mokotow,Poland,SR5RR,,439.275000,DUP-,7.600000,FM,TONE,127.3Hz,NO,Exact,52.178667,21.050667,+1:00

    # Prepare a data for the CSV file
    export_data: list[dict[str, Any]] = []
    for repeater in repeaters_list:
        item = {
            'Group No': re.search(r'(\d+)', repeater['qra']).group(1) if re.search(r'(\d+)', repeater['qra']) is not None else '',  # type: ignore
            'Group Name': re.search(r'(SR\d+)', repeater['qra']).group(1) if re.search(r'(SR\d+)', repeater['qra']) is not None else '',  # type: ignore
            'Name': unidecode(repeater['qth'].split(',')[0])[:16] if repeater['qth'] is not None else '',
            'Sub Name': 'Poland',
            'Repeater Call Sign': repeater['qra'],
            'Gateway Call Sign': repeater['qra'].ljust(7, ' ') + 'G' if repeater['mode'] == 'DSTAR' else '',
            'Frequency': repeater['qrg_tx'],
            'Dup': 'DUP-' if float(repeater['qrg_rx']) < float(repeater['qrg_tx']) else 'DUP+',
            'Offset': Decimal(abs(float(repeater['qrg_rx']) - float(repeater['qrg_tx']))).quantize(Decimal('1.000000')),
            'Mode': 'DV' if repeater['mode'] == 'DSTAR' else 'FM',
            'TONE': 'OFF' if repeater['ctcss_rx'] is None else 'TONE',
            'Repeater Tone': f"{repeater['ctcss_rx']}Hz" if repeater['ctcss_rx'] is not None else '88.5Hz' if repeater['mode'] == 'DSTAR' else '',
            'RPT1USE': 'YES',
            'Position': 'Exact' if repeater['altitudeOverSea'] is not None else 'Approximate',
            'Latitude': repeater['latitude'],
            'Longitude': repeater['longitude'],
            'UTC Offset': '+1:00'
        }

        export_data.append(item)

    # Export data to the CSV file
    with open(repeaters_file_path, 'w', newline='') as csvfile:
        fieldnames = export_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in export_data:
            writer.writerow(item)
        
    print(f"Data has been exported to the CSV file: {repeaters_file_path}")

if __name__ == '__main__':
    main()
