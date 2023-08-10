"""
Module minbundle.py - bundled standard codebase.
Copyright (c) 2023 Chris Joakim, MIT License
Timestamp: 2023-08-01 15:43

Usage:  from pysrc.minbundle import Bytes, Counter, Env, FS, Storage, System
"""

import csv
import json
import os
import platform
import socket
import sys
import time
import traceback

import psutil

from numbers import Number
from typing import Iterator

from azure.storage.blob import BlobServiceClient

# ==============================================================================

class Bytes():
    """
    This class is used to calculate KB, MB, GB, TB, PB, and EB values
    from a given number of bytes.  Also provides as_xxx() translation methods.
    """

    @classmethod
    def kilobyte(cls) -> int:
        """ Return the number of bytes in a kilobyte. """
        return 1024

    @classmethod
    def kilobytes(cls, kilobytes: Number) -> Number:
        """ Return the number of bytes in the given KB value. """
        return Bytes.kilobyte() * abs(float(kilobytes))

    @classmethod
    def megabyte(cls) -> int:
        """ Return the number of bytes in a megabyte."""
        return pow(1024, 2)

    @classmethod
    def megabytes(cls, megabytes: Number) -> Number:
        """ Return the number of bytes in the given MB value. """
        return Bytes.megabyte() * abs(float(megabytes))

    @classmethod
    def gigabyte(cls) -> int:
        """ Return the number of bytes in a gigabyte. """
        return pow(1024, 3)

    @classmethod
    def gigabytes(cls, gigabytes: Number) -> Number:
        """ Return the number of bytes in the given GB value. """
        return Bytes.gigabyte() * abs(float(gigabytes))

    @classmethod
    def terabyte(cls) -> int:
        """ Return the number of bytes in a terabyte. """
        return pow(1024, 4)

    @classmethod
    def terabytes(cls, terabytes: Number) -> Number:
        """ Return the number of bytes in the given TB value. """
        return Bytes.terabyte() * abs(float(terabytes))

    @classmethod
    def petabyte(cls) -> int:
        """ Return the number of bytes in a petabyte."""
        return pow(1024, 5)

    @classmethod
    def petabytes(cls, petabytes: Number) -> Number:
        """ Return the number of bytes in the given PB value. """
        return Bytes.petabyte() * abs(float(petabytes))

    @classmethod
    def exabyte(cls) -> int:
        """ Return the number of bytes in an exabyte. """
        return pow(1024, 6)

    @classmethod
    def exabytes(cls, exabytes: Number) -> Number:
        """ Return the number of bytes in the given EB value. """
        return Bytes.exabyte() * abs(float(exabytes))

    @classmethod
    def as_kilobytes(cls, num_bytes: Number) -> Number:
        """ Return the number of KB for the given number of bytes. """
        return float(abs(num_bytes)) / float(cls.kilobyte())

    @classmethod
    def as_megabytes(cls, num_bytes: Number) -> Number:
        """ Return the number of MB for the given number of bytes. """
        return float(abs(num_bytes)) / float(cls.megabyte())

    @classmethod
    def as_gigabytes(cls, num_bytes: Number) -> Number:
        """ Return the number of GB for the given number of bytes. """
        return float(abs(num_bytes)) / float(cls.gigabyte())

    @classmethod
    def as_terabytes(cls, num_bytes: Number) -> Number:
        """ Return the number of TB for the given number of bytes. """
        return float(abs(num_bytes)) / float(cls.terabyte())

    @classmethod
    def as_petabytes(cls, num_bytes: Number) -> Number:
        """ Return the number of PB for the given number of bytes. """
        return float(abs(num_bytes)) / float(cls.petabyte())
    @classmethod
    def as_exabytes(cls, num_bytes: Number) -> Number:
        """ Return the number of EB for the given number of bytes. """
        return float(abs(num_bytes)) / float(cls.exabyte())
# ==============================================================================

class Counter():
    """
    This class implements a simple int counter with an underlying dict object.
    """
    def __init__(self):
        self.data = {}

    def increment(self, key: str) -> None:
        """ Increment the given key by 1. """
        keys = self.data.keys()
        if key in keys:
            self.data[key] = self.data[key] + 1
        else:
            self.data[key] = 1

    def decrement(self, key: str) -> None:
        """ Decrement the given key by 1. """
        keys = self.data.keys()
        if key in keys:
            self.data[key] = self.data[key] - 1
        else:
            self.data[key] = -1

    def get_value(self, key: str) -> int:
        """ Get the int value of the given key. """
        keys = self.data.keys()
        if key in keys:
            return self.data[key]
        return 0

    def get_data(self) -> dict:
        """ Return the underlying dict object. """
        return self.data
# ==============================================================================

class Env():
    """
    This class is used to read the host environment, such as username and
    environment variables.  It also has methods for command-line flag
    argument processing.
    """

    @classmethod
    def var(cls, name: str, default=None) -> str | None:
        """ Return the value of the given environment variable name, or None. """
        if name in os.environ:
            return os.environ[name]
        return default

    @classmethod
    def username(cls) -> str | None:
        """ Return the USERNAME (Windows) or USER (macOS/Linux) value. """
        usr = cls.var('USERNAME')
        if usr is None:
            usr = cls.var('USER')
        return usr

    @classmethod
    def epoch(cls) -> float:
        """ Return the current epoch time, as time.time() """
        return time.time()

    @classmethod
    def verbose(cls) -> bool:
        """ Return a boolean indicating if --verbose or -v is in the command-line. """
        flags = [ '--verbose', '-v' ]
        for arg in sys.argv:
            for flag in flags:
                if arg == flag:
                    return True
        return False

    @classmethod
    def boolean_arg(cls, flag: str) -> bool:
        """ Return a boolean indicating if the given arg is in the command-line. """
        for arg in sys.argv:
            if arg == flag:
                return True
        return False
# ==============================================================================

class FS():
    """
    This class is used to do IO operations vs the local File System.
    """
    @classmethod
    def as_unix_filename(cls, filename: str) -> str:
        """ Return the given filename with unix slashes. """
        if filename.upper().startswith("C:"):
            return filename[2:].replace("\\", "/")
        return filename

    @classmethod
    def read(cls, infile: str) -> str | None:
        """ Read the given file, return the file contents str or None. """
        if os.path.isfile(infile):
            with open(file=infile, encoding='utf-8', mode='rt') as file:
                return file.read()
        return None

    @classmethod
    def readr(cls, infile: str) -> str | None:
        """ Read the given file with mode 'r', return the file contents str or None. """
        if os.path.isfile(infile):
            with open(file=infile, encoding='utf-8', mode='r') as file:
                return file.read()
        return None

    @classmethod
    def read_binary(cls, infile: str) -> str | None:
        """ Read the given binary file with mode 'rb', return the bytes or None. """
        if os.path.isfile(infile):
            with open(file=infile, mode='rb') as file:
                return file.read()
        return None

    @classmethod
    def read_lines(cls, infile: str) -> list[str] | None:
        """ Read the given file, return an array of lines(strings) or None """
        if os.path.isfile(infile):
            lines = []
            with open(file=infile, encoding='utf-8', mode='rt') as file:
                for line in file:
                    lines.append(line)
            return lines
        return None

    @classmethod
    def read_single_line(cls, infile: str) -> str | None:
        """ Read the given file, return the first line or None """
        lines = cls.read_lines(infile)
        if lines is not None:
            if len(lines) > 0:
                return lines[0].strip()
        return None

    @classmethod
    def read_encoded_lines(cls, infile: str, encoding='cp1252') -> list[str] | None:
        """
        Read the given file, with the given encoding.
        Return an array of lines(strings) or None.
        """
        if os.path.isfile(infile):
            lines = []
            with open(file=infile, encoding=encoding, mode='rt') as file:
                for line in file:
                    lines.append(line)
            return lines
        return None

    @classmethod
    def read_win_cp1252(cls, infile: str) -> str | None:
        """
        Read the given file with Windows encoding cp1252.
        Return an array of lines(strings) or None.
        """
        if os.path.isfile(infile):
            with open(file=os.path.join(infile), encoding='cp1252', mode='r') as file:
                return file.read()
        return None

    @classmethod
    def read_csv_as_dicts(cls, infile: str, delim=',', dialect='excel') -> list[str] | None:
        """
        Read the given csv filename, return an array of dicts or None.
        """
        if os.path.isfile(infile):
            rows = []
            with open(file=infile, encoding='utf-8', mode='rt') as csvfile:
                rdr = csv.DictReader(csvfile, dialect=dialect, delimiter=delim)
                for row in rdr:
                    rows.append(row)
            return rows
        return None

    @classmethod
    def read_csv_as_rows(cls, infile: str, delim=',', skip=0) -> list[str] | None:
        """
        Read the given csv filename, return an array of csv rows or None.
        """
        if os.path.isfile(infile):
            rows = []
            with open(file=infile, encoding='utf-8', mode='rt') as csvfile:
                rdr = csv.reader(csvfile, delimiter=delim)
                for idx, row in enumerate(rdr):
                    if idx >= skip:
                        rows.append(row)
            return rows
        return None

    @classmethod
    def read_json(cls, infile: str, encoding='utf-8') -> dict | list | None:
        """ Read the given JSON file, return either a list, a dict, or None. """
        if os.path.isfile(infile):
            with open(file=infile, encoding=encoding, mode='rt') as file:
                return json.loads(file.read())
        return None

    @classmethod
    def write_json(cls, obj: object, outfile: str, pretty=True, verbose=True) -> None:
        """ Write the given object to the given file as JSON. """
        if obj is not None:
            jstr = None
            if pretty is True:
                jstr = json.dumps(obj, sort_keys=False, indent=2)
            else:
                jstr = json.dumps(obj)

            with open(file=outfile, encoding='utf-8', mode='w') as file:
                file.write(jstr)
                if verbose is True:
                    print(f'file written: {outfile}')

    @classmethod
    def write_lines(cls, lines: list[str], outfile: str, verbose=True) -> None:
        """ Write the given str lines to the given file. """
        if lines is not None:
            with open(file=outfile, encoding='utf-8', mode='w') as file:
                for line in lines:
                    file.write(line + "\n") # os.linesep)  # \n works on Windows
                if verbose is True:
                    print(f'file written: {outfile}')

    @classmethod
    def text_file_iterator(cls, infile: str) -> Iterator[str] | None:
        """ Return a line generator that can be iterated with iterate() """
        if os.path.isfile(infile):
            with open(file=infile, encoding='utf-8', mode='rt') as file:
                for line in file:
                    yield line.strip()

    @classmethod
    def write(cls, outfile: str, string_value: str, verbose=True) -> None:
        """ Write the given string to the given file. """
        if outfile is not None:
            if string_value is not None:
                with open(file=outfile, encoding='utf-8', mode='w') as file:
                    file.write(string_value)
                    if verbose is True:
                        print(f'file written: {outfile}')

    @classmethod
    def list_directories_in_dir(cls, basedir: str) -> list[str] | None:
        """ Return a list of directories in the given directory, or None. """
        if os.path.isdir(basedir):
            files = []
            for file in os.listdir(basedir):
                dir_or_file = os.path.join(basedir, file)
                if os.path.isdir(dir_or_file):
                    files.append(file)
            return files
        return None

    @classmethod
    def list_files_in_dir(cls, basedir: str) -> list[str] | None:
        """ Return a list of files in the given directory, or None. """
        if os.path.isdir(basedir):
            files = []
            for file in os.listdir(basedir):
                dir_or_file = os.path.join(basedir, file)
                if os.path.isdir(dir_or_file):
                    pass
                else:
                    files.append(file)
            return files
        return None

    @classmethod
    def walk(cls, directory: str) -> list[dict] | None:
        """ Return a list of dicts for each file in the given directory, or None. """
        if os.path.isdir(directory):
            files = []
            for dir_name, _, base_names in os.walk(directory):
                for base_name in base_names:
                    full_name = f"{dir_name}/{base_name}"
                    entry = {}
                    entry['base'] = base_name
                    entry['dir'] = dir_name
                    entry['full'] = full_name
                    entry['abspath'] = os.path.abspath(full_name)
                    files.append(entry)
            return files
        return None

    @classmethod
    def read_csvfile_into_rows(cls, infile: str, delim=',') -> list | None:
        """ Read the given csv filename, return an array of csv rows or None. """
        if os.path.isfile(infile):
            rows = []  # return a list of csv rows
            with open(file=infile, encoding='utf-8', mode='rt') as csvfile:
                reader = csv.reader(csvfile, delimiter=delim)
                for row in reader:
                    rows.append(row)
            return rows
        return None

    @classmethod
    def read_csvfile_into_objects(cls, infile: str, delim=',') -> list[object] | None:
        """ Read the given csv filename, return an array of objects or None. """
        if os.path.isfile(infile):
            objects = []
            with open(file=infile, encoding='utf-8', mode='rt') as csvfile:
                reader = csv.reader(csvfile, delimiter=delim)
                headers = None
                for idx, row in enumerate(reader):
                    if idx == 0:
                        headers = row
                    else:
                        if len(row) == len(headers):
                            obj = {}
                            for field_idx, field_name in enumerate(headers):
                                key = field_name.strip().lower()
                                obj[key] = row[field_idx].strip()
                            objects.append(obj)
            return objects
        return None
# ==============================================================================

class Storage():
    """
    This class is used to access an Azure Storage account.
    """
    def __init__(self, opts):
        acct_name = opts['acct']
        acct_key  = opts['key']
        acct_url  = f'https://{acct_name}.blob.core.windows.net/'
        self.blob_service_client = BlobServiceClient(
            account_url=acct_url, credential=acct_key)

    def account_info(self):
        """ Return the account information. """
        return self.blob_service_client.get_account_information()

    def list_containers(self):
        """ Return the list of container names in the account. """
        clist = []
        try:
            containers = self.blob_service_client.list_containers(include_metadata=True)
            for container in containers:
                clist.append(container)
            return clist
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())
            return None

    def create_container(self, cname):
        """ Create a container in the account. """
        try:
            container_client = self.blob_service_client.get_container_client(cname)
            container_client.create_container()
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())

    def delete_container(self, cname):
        """ Delete a container in the account. """
        try:
            container_client = self.blob_service_client.get_container_client(cname)
            container_client.delete_container()
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())

    def list_container(self, cname):
        """ Return the list of blobs in the container. """
        try:
            container_client = self.blob_service_client.get_container_client(cname)
            return container_client.list_blobs()
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())
            return None

    def upload_blob_from_file(self, local_file_path, cname, blob_name, overwrite=True):
        """ Upload a blob from a local file. """
        try:
            blob_client = self.blob_service_client.get_blob_client(container=cname, blob=blob_name)
            with open(local_file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=overwrite)
            return True
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())
            return False

    def upload_blob_from_string(self, string_data, cname, blob_name, overwrite=True):
        """ Upload a blob from a string. """
        try:
            blob_client = self.blob_service_client.get_blob_client(container=cname, blob=blob_name)
            blob_client.upload_blob(string_data, overwrite=overwrite)
            return True
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())
            return False

    def download_blob(self, cname, blob_name, local_file_path):
        """ Download a blob to a local file. """
        try:
            blob_client = self.blob_service_client.get_blob_client(container=cname, blob=blob_name)
            with open(local_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())

    def download_blob_to_string(self, cname: str, blob_name: str) -> str:
        """ Download a blob to a string. """
        blob_client = self.blob_service_client.get_blob_client(container=cname, blob=blob_name)
        downloader = blob_client.download_blob(max_concurrency=1, encoding='UTF-8')
        return downloader.readall()
# ==============================================================================

class System():
    """
    This class is an interface to system information such as memory usage.
    """

    @classmethod
    def command_line_args(cls) -> list[str]:
        """ Return sys.argv """
        return sys.argv

    @classmethod
    def platform(cls) -> str:
        """ Return the platform.system() string. """
        return platform.system()

    @classmethod
    def is_windows(cls) -> bool:
        """ Return True if the platform is Windows, else False. """
        return 'win' in cls.platform().lower()

    @classmethod
    def is_mac(cls) -> bool:
        """ Return True if the platform is Apple macOS, else False. """
        return 'darwin' in cls.platform().lower()

    @classmethod
    def pid(cls) -> int:
        """ Return the current process id int. """
        return os.getpid()

    @classmethod
    def process_name(cls) -> str:
        """ Return the current process name. """
        return psutil.Process().name()

    @classmethod
    def user(cls) -> str:
        """ Return the current user name; os.getlogin(). """
        return os.getlogin()

    @classmethod
    def hostname(cls) -> str:
        """ Return the current hostname; socket.gethostname(). """
        try:
            return socket.gethostname()
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())
            return 'unknown'

    @classmethod
    def cwd(cls) -> str:
        """ Return the current working directory; Process.cwd(). """
        return psutil.Process().cwd()

    @classmethod
    def pwd(cls) -> str:
        """ Return the current working directory; os.getcwd() """
        return os.getcwd()

    @classmethod
    def platform_info(cls) -> str:
        """ Return a string with the platform info including processor. """
        return f'{platform.platform()} : {platform.processor()}'

    @classmethod
    def cpu_count(cls) -> int:
        """ Return the number of CPUs on the system. """
        return psutil.cpu_count(logical=False)

    @classmethod
    def memory_info(cls):
        """ Return the memory info for the current process. """
        return psutil.Process().memory_info()

    @classmethod
    def virtual_memory(cls):
        """ Return the virtual memory info for the current process. """
        return psutil.virtual_memory()

    @classmethod
    def epoch(cls) -> float:
        """ Return the current epoch time in seconds, as a float """
        return time.time()

    @classmethod
    def sleep(cls, seconds=1.0) -> None:
        """ Sleep for the given number of float seconds. """
        time.sleep(seconds)
