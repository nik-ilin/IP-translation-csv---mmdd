# IP-translation-csv---mmdd
INSTRUCTION FOR PROCESSING AND CONVERTING GEOIP DATA
====================================================

1. Preparing the Files
-----------------------
Ensure that the files "GeoLite2-Country-Blocks-IPv4.csv" and "GeoLite2-Country-Locations-ru.csv" 
are located in the same directory.

2. Running Preprocessing
------------------------
Open the terminal and navigate to the directory containing the files:
    cd /path/to/geoip

Run the preprocessing script:
    python3 process_geoip.py

After execution, a new file "GeoLite2-Country-FINAL.csv" will be generated.

3. Clearing the Terminal and Moving to the Converter Directory
--------------------------------------------------------------
Clear the terminal using the "clear" command or simply restart it.

Then navigate to the converter directory:
    cd /path/to/csv2mmdb

Make sure the binary file "csv2mmdb" has already been compiled using Go.

4. Converting to .mmdb Format
-----------------------------
Run the following command TWICE:

    ./csv2mmdb \
      -input /full/path/to/GeoLite2-Country-FINAL.csv \
      -config /full/path/to/config.yml \
      -output /full/path/to/GeoLite2-Country.mmdb

NOTE:
- Each file path must be specified fully (absolute path).
- The first run may generate an invalid .mmdb file of 0 bytes.
- The second run should complete successfully.
