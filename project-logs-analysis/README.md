# Udacity Project - Logs Analysis

This is first project of the [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004). In this project we'll build an **internal reporting tool** that will use information from the database to print out reports. 

## Installing 

In order to run the programm, we'll need a virtual machine(VM) that runs on top of your own machine. We're using the Vagrant software to configure and manage the VM. Here are the tools you'll need to install to get it running:

**Install VirtualBox:**

VirtualBox is the software that actually runs the virtual machine. You can download it from virtualbox.org, [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)

**Install Vagrant:**

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from [vagrantup.com](https://www.vagrantup.com/downloads.html)

**Download the VM configuration:**

You can download and unzip this file: [FSND-Virtual-Machine](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip). Alternately, you can use Github to fork and clone the repository: https://github.com/udacity/fullstack-nanodegree-vm.

## Getting started

**Running the virtual machine**

From your terminal, inside the **vagrant** subdirectory, run the command `vagrant up`. When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!

**Download the data**

Next, download the data [here](https://github.com/jaytoy/udacity-fullstack-nanodegree/tree/master/project-logs-analysis/Downloads). You will need to unzip this file after downloading it. The file inside is called **newsdata.sql**. Put this file into the **vagrant** directory, which is shared with your virtual machine.

To load the data, **cd** into the **vagrant** directory and use the following command: 

```
psql -d news -f newsdata.sql
```

## Running the program
Open the terminal. Then, run the following commands:

```
python logs_analysis.py
```