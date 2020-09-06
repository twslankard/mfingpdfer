#!/usr/bin/env python3
import sys
import csv
import urllib.request
import urllib.parse
import time
import os
import shutil
import tempfile
import hashlib
import argparse

from PyPDF2 import PdfFileMerger

def download_files(rows):
    # make temp dir
    m = hashlib.md5() 
    m.update(''.join([row[1] for row in rows]).encode())
    temp_path = os.path.join('.', 'downloaded_files', m.hexdigest())
    try:
        os.makedirs(temp_path)
    except FileExistsError:
        pass

    # download each file
    for row in rows:
        text, url = row
        parsed_url = urllib.parse.urlparse(url)
        file_name = os.path.basename(parsed_url.path)

        destination = os.path.join(temp_path, file_name)
        row.append(destination)
        print('Downloading {} -> {}'.format(url, destination))
        with urllib.request.urlopen(url) as response, open(destination, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    print("Done downloading.")
    return rows

def create_pdfs(rows, output_filename):
    merger = PdfFileMerger()
    for row in rows:
       merger.append(row[2]) 
    merger.write(output_filename)
    merger.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', metavar='[CSV file]')
    parser.add_argument('output_pdf', metavar='[output PDF]')
    args = parser.parse_args()
    with open(args.csv_file) as fp:
        reader = csv.reader(fp)
        rows = [row for row in reader][1:]

    downloaded_rows = download_files(rows)
    create_pdfs(rows, args.output_pdf)
