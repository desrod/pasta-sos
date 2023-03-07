#----
#Libs
#----

import argparse
from pathlib import Path
import os
import subprocess
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import re
import sys

#----
#Exceptions
#----

class Sosreport_Not_Found(Exception): pass
class Sosreport_Unreadable(Exception): pass
class Sosreport_Error(Exception): pass
class Unknown_Error(Exception): pass

#----
#main
#----

def sosreport_path_check(path):
    #checking that sosreport files are usable
    #see: https://docs.python.org/3/library/os.html#os.access

    sosreport = Path(path)

    if not sosreport.exists():
        raise Sosreport_Not_Found()

    if not os.access(sosreport, os.R_OK):
        raise Sosreport_Unreadable("Cannot read sosreport due to permission restriction.")

def run_hotsos(path):
    sosreport = Path(path)

    #running hotsos against the passed in path
    '''
    BUG

    When doing subprocess.run with the correct invocation:

    `subprocess.run(["hotsos", "--machine-readable", "--format yaml", str(sosreport)], shell=True, capture_output=True)`

    hotsos will run as if the final argument is '/' and attempt to analyze the local machine.

    Changing the argument to a single string suppresses this behaviour.
    '''

    res = subprocess.run([f"hotsos --machine-readable --format yaml {str(sosreport)}"], shell=True, capture_output=True)

    if res.returncode != 0:
        raise Sosreport_Error(f"Path may not lead to a correct sosreport: {sosreport}", res.stderr.decode())

    return res.stdout.decode()

def get_version_name_from_hotsos(out):
    #loading hotsos output
    data = load(out, Loader=Loader)
    words = re.split(r"\s", data['system']['os'].strip())
    return [i for i in filter( lambda x: x != 'ubuntu', words )][0]

def get_version_number_from_sosreport(path):
    sosreport = Path(path)

    #given a path to a sosreport, extract the version number from <sosreport path>/lsb-release
    p_lsb_release = sosreport / "lsb-release"

    with open(p_lsb_release) as f:
        version_string = f.read()

    words = re.split(r"\s", version_string.strip())

    #source: https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
    version_num = [i for i in filter( lambda x: bool(re.search(r'\d', x)), words )][0]

    #multipass only supports launching VMs using the major and minor version number
    #so only return the first two numbers
    #e.g., if lsb_release shows `22.04.1`, then use `22.04` to attempt to launch
    #https://en.wikipedia.org/wiki/Software_versioning

    return ".".join(version_num.split(".")[:2])

def run_multipass(version):
    '''
    BUG

    When launching subprocess.run with the correct invocation:

    `res = subprocess.run(["multipass", "launch", version], shell=True, capture_output=True)`

    multipass returns an error about incorrect invocation. removing the `shell=True` option resolves this; Unlike the previous error.
    '''

    return subprocess.run(["multipass", "launch", version], capture_output=True)

def check_done(res):
    if res.returncode == 0:
        launched_message = re.search(r"Launched\: (.+)", res.stdout.decode()).group()
        print( launched_message )

        sys.exit(0)

if __name__ == '__main__':
    #parsing CLI arguments
    parser = argparse.ArgumentParser(description='Given a sosreport from a system, create a pseudo-copy in a virtual machine.')
    parser.add_argument('sosreport', type=str, nargs=1, help='a path to a folder containing a sosreport.')
    args = parser.parse_args()

    sosreport_path = str(Path(args.sosreport[0]).absolute())

    sosreport_path_check(sosreport_path)

    hotsos_out = run_hotsos(sosreport_path)

    friendly_version_name = get_version_name_from_hotsos(hotsos_out)

    #first attempt to launch VM based on version information (friendly distro name; e.g., jammy) from hotsos
    res = run_multipass(friendly_version_name)

    check_done(res)

    #the friendly distro name from hotsos could not be used to launch a VM (e.g., the distro name was not found amongst multipass's known images)
    #second attempt to launch VM, this time pulling version number from the sosreport
    version_num = get_version_number_from_sosreport(path)
    res = run_multipass(version_num)

    check_done(res)

    #if the VM could not be launched, then error out
    raise Unknown_Error(f"Could not launch VM based on sosreport at: '{sosreport_path}'.")