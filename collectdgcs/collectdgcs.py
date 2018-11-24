import os
import sys
import time
import socket
import datetime as dt

from google.cloud import storage



def parseStorageLogFile(logFile):
    """
    Parses the given storage log file and returns the average bucket size
    over the 24 hours covered by the file.
    """

    contentLines = logFile.download_as_string().decode('utf-8').splitlines()
    byteHourUsed = int(contentLines[1].split(',')[1].strip('"'))

    return int(byteHourUsed / 24)



def fetchAndPrintStorageLogs(logsBucketName, interval):
    """
    Fetches the log files located in the bucket whose name is passed
    as argument, parses the last storage information from these files,
    prints that information in the format interpreted by CollectD's
    Exec plugin, and removes the log files.
    """

    # Google Cloud Storage access proxies.

    client = storage.Client()
    logsBucket = client.get_bucket(logsBucketName)

    # Stores for the storage logs dates and values.

    bucketSizes = {}
    lastLogDates = {}

    # Running through all the files in the logs bucket.

    for logFile in logsBucket.list_blobs():

        # Infering information about the current file from its name.

        parts = logFile.name.split('_')

        bucketName = parts[0]
        logType = parts[1]
        logDate = dt.datetime(*[int(i) for i in parts[2:-2]])
        logId = parts[-2]
        logVersion = parts[-1]

        # Parse the file if it contains storage information and is the latest one for its bucket.

        if logType == 'storage' and (bucketName not in bucketSizes or logDate > lastLogDates[bucketName]):

            lastLogDates[bucketName] = logDate
            bucketSizes[bucketName] = parseStorageLogFile(logFile)

        # Removing the current file since it is not needed anymore.

        logFile.delete()

    # Fetching the hostname to build statistics' identifiers.

    host = os.environ.get('COLLECTD_HOSTNAME', socket.gethostname())

    # Printing the result in CollectD's Exec plugin format, and flushing stdout to avoid delays.

    for bucketName, size in bucketSizes.items():

        date = int(lastLogDates[bucketName].timestamp())

        identifier = '{}/gcs_storage-{}/bytes'.format(host, bucketName.replace('-', '_'))

        print('PUTVAL {} interval={} {}:{}'.format(identifier, interval, date, size), flush=True)



def main():
    """
    Tries to parse the logs bucket name and the fetching interval in the program
    arguments, and passes them to function fetchAndPrintStorageLogs() if they were
    found, or prints a usage indication message otherwise.
    """

    if len(sys.argv) != 3:

        print('Usage : collectdgcs bucket-name-where-logs-are-stored interval', flush=True)

    else:

        interval = int(sys.argv[2])
        logsBucketName = sys.argv[1]

        while True:

            fetchAndPrintStorageLogs(logsBucketName, interval)
            time.sleep(interval)



if __name__ == '__main__':
    main()
