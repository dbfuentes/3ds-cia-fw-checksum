#! /usr/bin/env python
# -*- coding: UTF-8 -*-

# Import modules
import hashlib
import sys
import os
from os import curdir

# ================== START EDIT HERE ==================

# Directory with the md5 files (*.md5)
HASH_DIR = "hashes"

# Input directory with the CIAs files (fimrware files)
INPUT_DIR = "updates"

# ================== STOP EDIT HERE  ==================

# Internal Variables
VERSION = "0.1.0"
QUIET_MODE = False

# raw_input fix for python 3.x
if sys.version[0] == "3":
    raw_input = input

# ===========================================
# Class and funcionts


def user_input(mensage, error_mensage):
    """Ask for user input and chech if the input is a number."""
    fist_selection = True
    number = False
    while number is False:
        try:
            if fist_selection:
                x = int(raw_input(mensage))
            else:
                x = int(raw_input(error_mensage))
            # try convert: x(input) --> int number
            selection = int(x)
            number = True
        except:
            number = False
            fist_selection = False
    return selection


def input_option(maxnumber, mensage, error_mensage):
    """Chech if the selection number (user input) is a valid option."""
    selection = int(user_input(mensage, error_mensage))
    correct = False
    while correct is False:
        if selection <= maxnumber and selection > 0:
            correct = True
        else:
            correct = False
            selection = user_input(error_mensage, error_mensage)
    return selection


def get_md5(filename, mode="b"):
    """Calculate md5 hash for a file without full-load in memory."""
    # Try open the file in binary mode(rb) or text mode(r)
    try:
        if mode == "b":
            infile = open(filename, "rb")
        else:
            infile = open(filename, "r")
    except:
        infile.close()
        error_code = 5
        return error_code
    # Calculate and return md5 hash
    suma = hashlib.md5()
    while True:
        data = infile.read(1024)
        if not data:
            break
        suma.update(data)
    infile.close()
    return suma.hexdigest()


def get_expected_hashes(hashfile, listfiles, quiet=False):
    """Read a .md5 file and return a 2 dictionaries (hashes and read mode)."""
    results = {"status": 0}
    read_mode = {}
    # The "status" and "mensages" values save all error/warnirng. Codes values:
    #  0 = Ok (No Errors / Warnirngs)
    #  1 = (Error-01) the INPUT_DIR is empty or does not exist
    #  2 = (Error-02) .md5 File Not found (not exist) in the HASH_DIR
    #  3 = (Error-03) Can't open the .md5 File (corrupt file?)
    # 11 = (Warnirng-01) No valid format in some lines (Expected md5sum format)
    if os.path.exists(hashfile) is False:
        # Try open the *.md5 file (contains a list of all hash, filename pairs)
        err = ("Error-02: .md5 File Not found:\n" + str(hashfile))
        results["status"] = 2
        results["mensage"] = str(err)
    else:
        try:
            if quiet is False:
                print("Open file: " + str(hashfile))
            infile = open(hashfile, "r")
        except:
            infile.close()
            err = ("Error-03: Can't open the .md5 File: " + str(hashfile))
            results["status"] = 3
            results["mensage"] = str(err)
    if results["status"] == 2 or results["status"] == 3:
        # Return a error code/mensage in a dictionary
        return results, read_mode
    else:
        # Read the file, line by line (Expected md5sum format or similar):
        # One line for each FILE with: checksum hash (128-bit value, which is
        # 32 characters in a hex encode or 22 in base64), a space, a character
        # indicating input mode ('*' for binary, ' ' for text) and a filename.
        line_counter = 0
        invalid_lines = []
        for line in infile:
            line_counter = line_counter + 1
            hash_end = line.find(" ")
            if hash_end != -1:
                hash_string = line[0:hash_end]
                hash_mode = line[(hash_end+1):(hash_end+2)]
                hash_filename = line[(hash_end+2):-1]
                if hash_mode == "*" or hash_mode == " ":
                    if len(hash_string) == 32:
                        results[hash_filename] = hash_string
                        read_mode[hash_filename] = hash_mode
                    else:
                        # no valid format (hash != 32, space = ok, mode = ok)
                        invalid_lines.append(line_counter)
                else:
                    # no valid format (space = ok, mode = not valid)
                    invalid_lines.append(line_counter)
            else:
                # no valid format (space no found)
                invalid_lines.append(line_counter)
        infile.close()
        # Warnirng: No valid format in some lines
        if len(invalid_lines) != 0:
            err = "Warnirng-01: No valid format (Expected md5sum format)"
            err = err + "in lines number (line ignored): " + str(invalid_lines)
            results["status"] = 11
            results["mensage"] = str(err)
        return results, read_mode


def run_script():
    """Main script."""
    breakline = "=" * 55
    print("CIA Updater Pack - Checksum Script\nVersion: " + str(VERSION))
    # chech the 3DS model
    print(breakline)
    print("A. What is your console model?")
    print("1 = Old 3DS / 3DS XL\n2 = 2DS\n3 = New 3DS / New 3DS XL\n")
    model = None
    mensage = "Your selection [1-3]: "
    error_mensage = "Invalid selection [values: 1-3], retry: "
    option = input_option(3, mensage, error_mensage)
    while model is None:
        if option == 1 or option == 2:
            model = "o3DS"
        elif option == 3:
            model = "n3DS"
        else:
            model = None
            option = input_option(3, error_mensage, error_mensage)
    # chech the firmware version
    print(breakline)
    print("B. What is the version of the CIA Pack?")
    print("1 = 9.2.0-20E\n2 = 9.2.0-20U\n3 = 9.2.0-20J\n--------------")
    print("4 = 9.0.0-20E\n5 = 9.0.0-20U\n6 = 9.0.0-20J\n--------------")
    print("7 = 2.1.0-4E \n8 = 2.1.0-4U \n9 = 2.1.0-4J\n")
    fw = None
    mensage = "Your selection [1-9]: "
    error_mensage = "Invalid selection [values: 1-9], retry: "
    option = input_option(9, mensage, error_mensage)
    while fw is None:
        if option == 1:
            fw = "9.2.0-20E"
        elif option == 2:
            fw = "9.2.0-20U"
        elif option == 3:
            fw = "9.2.0-20J"
        elif option == 4:
            fw = "9.0.0-20E"
        elif option == 5:
            fw = "9.0.0-20U"
        elif option == 6:
            fw = "9.0.0-20J"
        # fw 2.1 exist only in old3DS
        elif option == 7:
            model = "o3DS"
            fw = "2.1.0-4E"
        elif option == 8:
            model = "o3DS"
            fw = "2.1.0-4U"
        elif option == 9:
            model = "o3DS"
            fw = "2.1.0-4J"
        else:
            fw = None
            option = input_option(9, error_mensage, error_mensage)
    # Path to *.md5 file
    filename = str(model) + "-" + str(fw) + ".md5"
    hashfile = os.path.join(curdir, HASH_DIR, filename)
    print(breakline)
    # =======================
    # Step 1: Checking hashes
    print("Step 1: Checking hashes for: " + model + "-" + str(fw) + "\n")
    try:
        dir_file = os.listdir(os.path.join(curdir, INPUT_DIR))
    except:
        dir_file = []
    if not dir_file:
        err = "Error-01: The direcory: " + str(os.path.join(curdir, INPUT_DIR))
        err = err + "  is empty or does not exist."
        hashes = {"status": 1}
        hashes["mensage"] = str(err)
    else:
        if QUIET_MODE is False:
            hashes, mode = get_expected_hashes(hashfile, dir_file, quiet=False)
        else:
            hashes, mode = get_expected_hashes(hashfile, dir_file, quiet=True)
    # Display errors
    if hashes["status"] == 1:
        # the INPUT_DIR is empty or does not exist
        print(str(hashes["mensage"]) + "\n")
    elif hashes["status"] == 2:
        print(str(hashes["mensage"]))
        print("The script can't continue as a .md5 file is missing.")
        print("Please make sure you have all the files related to")
        print("this script on this folder.\n")
    elif hashes["status"] == 3:
        print(str(hashes["mensage"]))
        print("The script can't open the .md5 file.\n")
    else:
        if hashes["status"] == 11:
            print(str(hashes["mensage"]) + "\n")
        # Checking hashes
        if QUIET_MODE is False:
            print("Checking hashes for:")
        results = {"status": 0}
        elements = hashes.keys()
        for cia in elements:
            if cia == "mensage" or cia == "status":
                pass
            else:
                route = os.path.join(curdir, INPUT_DIR, cia)
                if os.path.exists(route):
                    # Route found
                    if mode[cia] == "*":
                        result = get_md5(route, mode="b")
                    elif mode[cia] == " ":
                        result = get_md5(route, mode="r")
                    # compare expected hash vs file hash
                    if hashes[cia] == result:
                        results[str(cia)] = "ok"
                    else:
                        results["status"] = 1
                        results[str(cia)] = "Checksum does NOT match"
                    # remove the file in the list of files in the INPUT_DIR
                    dir_file.remove(cia)
                else:
                    # Route Not found
                    results["status"] = 2
                    results[str(cia)] = "Not found"
                if QUIET_MODE is False:
                    print("File: " + str(cia) + " - " + results[cia])
        # =======================
        # Step 2: Show Results
        print("\n" + breakline)
        print("Step 2: Results\n")
        if results["status"] == 0:
            if not dir_file:
                print("Your CIA pack is good :-)")
            else:
                print("Your CIA pack is good.")
                print("But contains the following extra files:")
                for element in dir_file:
                    print(element)
        else:
            print("Your CIA pack is NOT GOOD!")
            print((" " * 17) + "---------")
            if results["status"] == 1:
                print("The sum of the following files does not match:")
                not_match = results.items()
                for x, y in not_match:
                    if y == "Checksum does NOT match":
                        print(str(x))
            if results["status"] == 2:
                print("Some file(s) is missing:")
                not_match = results.items()
                for x, y in not_match:
                    if y == "Not found":
                        print(str(x))
            if dir_file:
                print("\nAnd contains the following extra files:")
                for element in dir_file:
                    print(element)

# Main script
if __name__ == "__main__":
    run_script()
