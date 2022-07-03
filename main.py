#!python3
# -*- coding: utf-8 -*-

from asyncio.subprocess import PIPE
from os import path
import os
import subprocess
import sys
from tkinter.messagebox import YES
from loguru import logger

# VM name
vm_name = "teste-zeppelin"

#----------------------------------------------------------------------
@logger.catch
def vagrant_up() -> bool:
    command = "vagrant up"

    try:
        logger.info("VAGRANT - Initializing virtual machine.")
        subprocess.run(command, check=True)
        return True
    except Exception as err:    
        logger.error(f"VAGRANT - Error initializing virtual machine: {err}.")
        return False

#----------------------------------------------------------------------
@logger.catch
def verify_wget(vagrant_cmd:str) -> bool:
    '''
    Verify if wget is installed.
    '''
    try:
        logger.info("Verifying if wget is installed...")
        ssh_cmd = "wget --version"
        ret = subprocess.run(f"{vagrant_cmd}'{ssh_cmd}'", stdout=PIPE)
        if ret.returncode != 0:
            logger.info("wget is not installed.")
            install_wget(vagrant_cmd)
    except Exception as err:    
        logger.error(f"Error verifying wget: {err}.")

#----------------------------------------------------------------------
@logger.catch
def install_wget(vagrant_cmd:str):
    '''
    Installs wget in the VM.
    '''
    try:
        logger.info(f"Installing wget in the virtual machine...")
        ssh_cmd = "sudo yum install -y wget"
        subprocess.run(f"{vagrant_cmd}'{ssh_cmd}'", check=True)
        logger.info(f"wget installed successfully.")
    except Exception as err:    
        logger.error(f"Error installing wget: {err}.")

#----------------------------------------------------------------------
@logger.catch
def update_yum(vagrant_cmd:str):
    '''
    Update yum.
    '''
    try:
        logger.info(f"Updating yum...")
        ssh_cmd = "sudo yum update -y"
        subprocess.run(f"{vagrant_cmd}'{ssh_cmd}'", check=True)
        logger.info(f"yum updated successfully.")
    except Exception as err:    
        logger.error(f"Error updating yum: {err}.")   

#----------------------------------------------------------------------
@logger.catch
def tar_extract(vagrant_cmd: str, tar_file:str, path_destiny:str) -> bool:
    logger.info(f"Extracting {tar_file}...")
    ssh_cmd = f"sudo tar xf {tar_file} -C {path_destiny}"
    ret = subprocess.run(f"{vagrant_cmd}'{ssh_cmd}'")
    return bool(ret.returncode)

#----------------------------------------------------------------------
@logger.catch
def wget_download(vagrant_cmd:str, url:str, path_destiny:str) -> bool:   
    # Checks if wget is installed, otherwise installs it.
    try:
        if not verify_wget:
            install_wget()
        ssh_cmd = f"wget {url} -P {path_destiny}"
        ret = subprocess.run(f"{vagrant_cmd}'{ssh_cmd}'", check=True)
    except Exception as err:
        logger.error(f"Error downloading the file using wget: {err}.")        

#----------------------------------------------------------------------
@logger.catch
def install_java(vagrant_cmd: str):
    '''
    Installs JDK in the VM.
    '''
    try:
        logger.info("Installing JDK in the virtual machine...")

        logger.info("Downloading JDK...")
        wget_download(vagrant_cmd, "https://download.oracle.com/java/18/latest/jdk-18_linux-x64_bin.rpm", ".")
       
        logger.info("Installing JDK...")
        ssh_cmd = "sudo rpm -ivh jdk-18_linux-x64_bin.rpm"
        ret = subprocess.run(f"{vagrant_cmd}'{ssh_cmd}'", check=True)
        
        logger.info(f"Including JDK's path in PATH variable...")
        ssh_cmd = f"export PATH=\"$PATH:/usr/java/latest/bin\""
        ret = subprocess.run(f"{vagrant_cmd}'{ssh_cmd}'", check=True)

        logger.info(f"Setting JAVA_HOME variable in bash_profile file...")
        ssh_cmd = f"export PATH=\"$PATH:/usr/java/latest\" >> ~/.bash_profile"
        ret = subprocess.run(f"{vagrant_cmd}'{ssh_cmd}'", check=True)

        logger.info(f"Setting JRE_HOME variable in bash_profile file...")
        ssh_cmd = f"echo \"export JRE_HOME=/usr/java/latest/bin\" >> ~/.bash_profile"
        ret = subprocess.run(f"{vagrant_cmd}'{ssh_cmd}'", check=True)

        logger.info(f"Executing bash_profile to set variables...")
        ssh_cmd = f"source ~/.bash_profile"
        ret = subprocess.run(f"{vagrant_cmd}'{ssh_cmd}'", check=True)
    except Exception as err:    
        logger.error(f"Error installing Java: {err}.")

#----------------------------------------------------------------------
@logger.catch
def install_zeppelin(vagrant_cmd: str):
    '''
    Installs Apache Zeppelin in the VM.
    '''
    try:
        logger.info("Downloading Apache Zeppelin...")
        wget_download(vagrant_cmd, "https://dlcdn.apache.org/zeppelin/zeppelin-0.10.1/zeppelin-0.10.1-bin-all.tgz", ".")
        
        logger.info("Extracting Apache Zeppelin...")
        tar_extract(vagrant_cmd, "zeppelin-*-bin-all.tgz", "/opt")

        # To be continued...

    except Exception as err:    
        logger.error(f"Error installing Apache Zeppelin: {err}.")


if __name__ == "__main__":

    # Get program path
    app_dir = path.dirname(path.realpath(__file__))

    # Vagrant path
    vagrant_path = path.join(app_dir, "vagrant")

    # Change workdir to vagrant path
    os.chdir(vagrant_path)

    vagrant_cmd = f"vagrant ssh -c "

    # Inicializa a máquina virtual
    if vagrant_up():

        # Updating yum
        update_yum()

        # Verifying if wget is installed
        if not verify_wget(vagrant_cmd):
            # Install wget
            install_wget()

        # Instala o Java
        install_java(vagrant_cmd)

        # Instala o Apache Zeppelin
        install_zeppelin(vagrant_cmd)
