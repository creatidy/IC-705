# Radio Repeater Data Processing Script

This script is designed to read data from an XML file containing information about radio repeaters, process it, and export it to a CSV file. The CSV file format is compatible with the ICOM IC-705 radio.

## Features

1. Reads data from an XML file - source: https://przemienniki.net/
3. Filters the list of repeaters based on the country, mode, and band.
6. Writes the data to the CSV file

## Usage

To use this script, run it with Python and provide the path to the XML file as a command-line argument. The script will create a CSV file in the same directory as the XML file.

Optionally you can provide the following arguments:
--country: The country code to filter the repeaters by (e.g., pl)
--mode: The mode to filter the repeaters by (e.g., FM, DSTAR, FMLINK)
--band: The band to filter the repeaters by (e.g., 70CM, 2M)

You can provide multiple values for the mode and band arguments by separating them with spaces.

More about params you can find on the site: https://przemienniki.net/

```bash
python repeaters.py path/to/your/xml/file.xml --country pl --mode FM DSTAR FMLINK --band 70CM 2M
