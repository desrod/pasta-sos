# pasta-sos
Create a virtual machine from an sosreport, for troubleshooting.

## Version
v0.1.0

## Description
A common task when troubleshooting client systems is to replicate a system for testing. This is done to issolate a bug or to attempt fixes without harming client infrastructure. A common tool to do this is `sosreport` (see: https://github.com/sosreport/sos). `sosreport` gathers detailed information about a client's system into a single package which then can be handed off to support for the purposes of information gathering or replication. Replication is often done manually, given the information in a sosreport. This project attempts to automate the process of replication.

## Overview
This project, in its alpha state, is a thin wrapper around the tools `hotsos` and `multipass`. These tools are used (respectively) to gather summary information from a sosreport and to create a virtual machine configured similarly to the details found in a sosreport.

This project is intended for the replication of Ubuntu installations. As such, at this time, when `pasta-sos` is ran it will create a virtual machine installed with Ubuntu whose version matches the information in the sosreport.

Feedback on usage is appreciated, and recommendations on features and improvements are encouraged; see the discussion forum: https://github.com/pjmattingly/pasta-sos/discussions/categories/ideas.

At the moment there is no packaging assocaited with this project, and so the installation instructions seek to mimic a development environment.

This tool is in an alpha state and will likely break. Please use the [Issues](https://github.com/pjmattingly/pasta-sos/issues) tab for reporting.

## Install

1) Install `hotsos`; See: https://github.com/canonical/hotsos#install
2) Install `multipass`; See: https://github.com/canonical/multipass#install-multipass
3) Install `python` (developed with 3.10); see: https://www.python.org/downloads/
4) Install `pipenv`; see: https://packaging.python.org/en/latest/tutorials/managing-dependencies/#installing-pipenv
6) Clone the repository `git clone https://github.com/pjmattingly/pasta-sos`; see: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
5) Install dependencies `pipenv install`; see: https://pipenv-fork.readthedocs.io/en/latest/basics.html
6) Run `pasta-sos <path/to/sosreport folder>`

## Cleanup

`pasta-sos` will create virtual machines with `multipass`. At this time there is no functionality for removing these virtual machines automatically. `pasta-sos` will report the names of the virtual machines it creates with output to STDOUT; Similar to: `Launched: <name of VM>`. Use the command `multipass delete <name of VM>` to remove the virtual machines it creates; You may also need to use `multipass purge` to remove deleted virtual machines from your system.
  
## Future

I believe the first order of business should be snapshot support. This should allow for easy rollbacks after making changes to the virtual machine. At this time `multipass` does not support snapshots; Though it is a promised feature for a future release: https://github.com/canonical/multipass/issues/208<sup>1</sup>. `multipass` was chosen for this initial version due to its simplicity of use. In the future, another virtual machine creation tool will be used in the place of `multipass` for future releases (e.g., libvirt, etc.).
  
Second, support for `cloud-init`. `cloud-init` is a means for "cloud instance initialisation" (https://cloudinit.readthedocs.io/en/latest/). As such, specifying packages to be added to the virtual machine produced by `pasta-sos` with `cloud-init` seems to be a reasonable approach for further duplicating the state of client systems.

Third, cloning installed packages. That is, `sosreport` gathers information about installed packages on a client machine. Thus, a means of installing (approximately) identical packages to a `pasta-sos` virtual machine would be helpful in troubleshooting difficult to reproduce issues.<sup>2</sup>

Other future ideas: support for creating containers in addition to (or instead of?) virtual machines. Automatic cleanup of created virtual machines. Virtual machine names that include case numbers. Backups. Tools for inducing rare real-world scenarios with the virtual machines (for example, packet loss, out of memory, out of storage space, etc.). Support for a variety of "shells" that mimic the behaviour of other virtual machine management tools (e.g., lib-virt, virt-manager, uvt-kvm), to allow for ease of integration with existing solution that use different tooling; for example: `pasta-sos shell uvt-kvm`, which then causes pasta-sos to act like `uvt-kvm`. Support for the creation of networks of virtual machines to mimic complex deployments on the client-side (perhaps with k8s?). Duplication of running service configurations, given configuration files and binaries from a client machine. Cloning hardware configurations; For example, a client machine may have two network interfaces, and a variety of storage devices, a pasta-sos virtual machine should mimic this configuration.

----

<sup>1</sup>There is technically a means of [creating snapshots manually](https://github.com/canonical/multipass/issues/208#issuecomment-910422845), given the underlying virtual machine driver. But this is likely to create edge-cases and bugs, and so moving to a different approach seems to be the best course of action. 

<sup>2</sup>As pointed out by [`desrod`](https://github.com/desrod), this is startingly complex topic. A key factor in this, is that client machines may have packages that are no longer available. As such, the question becomes: how to either (1) find such packages in available archives or (2) mimic these older packages such that they can be used in a virtual machine for reproduction? Current lines of inquiry include: `equivs` (https://manpages.debian.org/testing/equivs/equivs-build.1.en.html, https://wiki.debian.org/Packaging/HackingDependencies), `lpmadison` (https://github.com/desrod/lpmadison), `apt-clone` (https://manpages.ubuntu.com/manpages/jammy/man8/apt-clone.8.html), and `Minimal Ubuntu` (https://wiki.ubuntu.com/Minimal). As well as searching for the means of "mocking" or "stubbing" such packages.
