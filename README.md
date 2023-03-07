# pasta-sos
Create a virtual machine from an sosreport, for troubleshooting.

## Version
v0.1.0

## Description
A common task when troubleshooting client systems is to replicate a system for testing. This is done to issolate a bug or to attempt fixes without harming client infrastructure. A common tool to do this is `sosreport` (see: https://github.com/sosreport/sos). `sosreport` gathers detailed information about a client's system into a single package which then can be handed off to support for the purposes of information gathering or replication. Replication is often done manually, given the information in a sosreport. This project attempts to automate the process of replication.

## Overview
This project, in its alpha state, is a thin wrapper around the tools `hotsos` and `multipass`. These tools are used (respectively) to gather summary information from a sosreport and to create a virtual machine configured similarly to the details found in a sosreport. Feedback on usage is appreciated, and recommendation for ideas for additional features are encouraged. At the moment there is no packaging assocaited with this project, and so the installation instructions seek to mimic a development environment. This tool is in an alpha state and will likely break. Please use the [Issues](https://github.com/pjmattingly/pasta-sos/issues) tab for reporting.

## Install

1) Install `hotsos`; See: https://github.com/canonical/hotsos#install
2) Install `multipass`; See: https://github.com/canonical/multipass#install-multipass
3) Install `python` (developed with 3.10); see: https://www.python.org/downloads/
4) Install `pipenv`; see: https://packaging.python.org/en/latest/tutorials/managing-dependencies/#installing-pipenv
6) Clone the repository `git clone https://github.com/pjmattingly/pasta-sos`; see: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
5) Install dependencies `pipenv install`; see: https://pipenv-fork.readthedocs.io/en/latest/basics.html
6) Run `pasta-sos <path/to/sosreport folder>

## Cleanup

`pasta-sos` will create virtual machines with multipass. At this time there is no functionality for removing these virtual machines automatically. `pasta-sos` will report the names of the virtual machines it creates with output to STDOUT; Similar to: `Launched: <name of VM>`. Use the command `multipass delete <name of VM>` to remove the virtual machines it creates; You may also have to use `multipass purge` to remove deleted virtual machines from your system.
