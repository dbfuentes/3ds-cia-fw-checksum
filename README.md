# 3ds-cia-fw-checksum
This script checks the md5 hashes of all CIAs in a update pack for a 3DS, for the purpose of detecting errors/corrupted files.

## Requirement

- [Python 2.7 or Python 3.x](https://www.python.org/downloads/) 

## Instructions

Put your CIAs in the **updates** folder, run the script **checker.py** and follow its instructions.

The script tell you if the CIA files are good to be used for update or not.

## Currently supported CIA packs:

- **n3DS:** 9.2.0-20E, 9.2.0-20U, 9.2.0-20J, 9.0.0-20E, 9.0.0-20U, 9.0.0-20J

- **o3DS / 2DS:** 9.2.0-20E, 9.2.0-20U, 9.2.0-20J, 9.0.0-20E, 9.0.0-20U, 9.0.0-20J, 2.1.0-4E, 2.1.0-4U, 2.1.0-4J
