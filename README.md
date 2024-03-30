# Radio Repeater Data Processing Script

This script is designed to read data from an XML file containing information about radio repeaters, process it, and export it to a CSV file. The CSV file format is compatible with the ICOM IC-705 radio.

## Features

1. Reads data from an XML file
3. Filters the list of repeaters based on the country, mode, and band.
6. Writes the data to the CSV file

## Usage

To use this script, run it with Python and provide the path to the XML file as a command-line argument. The script will create a CSV file in the same directory as the XML file.

```bash
python repeaters.py path/to/your/xml/file.xml --country pl --mode FM DSTAR FMLINK --band 70CM 2M
