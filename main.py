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
def verify_wget(vagrant_cmd: str) -> bool:
    '''
    Verify if wget is installed.
    '''
    try:
        logger.info("Verifying if wget is installed...")
        ssh_cmd = "wget --version"
        ret = subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'")
        return ret.returncode == 0
    except Exception as err:    
        logger.error(f"Error verifying wget: {err}.")
        return False

#----------------------------------------------------------------------
@logger.catch
def verify_java(vagrant_cmd: str) -> bool:
    '''
    Verify if Java is installed.
    '''
    try:
        logger.info("Verifying if Java is installed...")
        ssh_cmd = "java -version"
        ret = subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'")
        return ret.returncode == 0
    except Exception as err:    
        logger.error(f"Error verifying Java version: {err}.")
        return False

#----------------------------------------------------------------------
@logger.catch
def verify_zeppelin(vagrant_cmd: str) -> bool:
    '''
    Verify if Apache Zeppelin is installed as service.
    '''
    try:
        logger.info("Verifying if Apache Zeppelin is installed...")
        ssh_cmd = "sudo systemctl status zeppelin"
        ret = subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'")
        return ret.returncode == 0
    except Exception as err:    
        logger.error(f"Error verifying Apache Zeppelin service: {err}.")
        return False

#----------------------------------------------------------------------
@logger.catch
def install_wget(vagrant_cmd: str):
    '''
    Installs wget in the VM.
    '''
    try:
        logger.info(f"Installing wget in the virtual machine...")
        ssh_cmd = "sudo yum install -y wget"
        subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'", check=True)
        logger.info(f"wget installed successfully.")
    except Exception as err:    
        logger.error(f"Error installing wget: {err}.")

#----------------------------------------------------------------------
@logger.catch
def update_yum(vagrant_cmd: str):
    '''
    Update yum.
    '''
    try:
        logger.info(f"Updating yum...")
        ssh_cmd = "sudo yum update -y"
        subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'", check=True)
        logger.info(f"yum updated successfully.")
    except Exception as err:    
        logger.error(f"Error updating yum: {err}.")   

#----------------------------------------------------------------------
@logger.catch
def tar_extract(vagrant_cmd: str, tar_file: str, path_destiny: str) -> bool:
    logger.info(f"Extracting {tar_file}...")
    ssh_cmd = f"sudo tar xvf {tar_file} -C {path_destiny}"
    ret = subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'")
    return bool(ret.returncode)

#----------------------------------------------------------------------
@logger.catch
def wget_download(vagrant_cmd: str, url: str, path_destiny: str) -> bool:   
    # Checks if wget is installed, otherwise installs it.
    try:
        logger.info(f"Starting download of the url: {url}...")
        ssh_cmd = f"wget {url} -P {path_destiny}"
        ret = subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'", check=True)
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
        ret = subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'", check=True)
        
        logger.info(f"Including JDK's path in PATH variable...")
        ssh_cmd = f"export PATH=\"$PATH:/usr/java/latest/bin\""
        ret = subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'", check=True)

        logger.info(f"Setting JAVA_HOME variable in bash_profile file...")
        ssh_cmd = f"export PATH=\"$PATH:/usr/java/latest\" >> ~/.bash_profile"
        ret = subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'", check=True)

        logger.info(f"Setting JRE_HOME variable in bash_profile file...")
        ssh_cmd = f"echo \"export JRE_HOME=/usr/java/latest/bin\" >> ~/.bash_profile"
        ret = subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'", check=True)

        logger.info(f"Executing bash_profile to set variables...")
        ssh_cmd = f"source ~/.bash_profile"
        ret = subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'", check=True)
    except Exception as err:    
        logger.error(f"Error installing Java: {err}.")

#----------------------------------------------------------------------
@logger.catch
def install_zeppelin(vagrant_cmd: str, install_dir: str):
    '''
    Installs Apache Zeppelin in the VM.
    '''
    try:
        logger.info("Downloading Apache Zeppelin...")
        wget_download(vagrant_cmd, "https://dlcdn.apache.org/zeppelin/zeppelin-0.10.1/zeppelin-0.10.1-bin-all.tgz", ".")
        
        logger.info("Extracting Apache Zeppelin...")
        tar_extract(vagrant_cmd, "zeppelin-*-bin-all.tgz", "/opt")
       
        logger.info(f"Moving Apache Zeppelin binaries to final directory...")
        ssh_cmd = f"sudo mv /opt/zeppelin-*-bin-all {install_dir}"
        ret = subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'", check=True)
    except Exception as err:    
        logger.error(f"Error installing Apache Zeppelin: {err}.")

#----------------------------------------------------------------------
@logger.catch
def start_zeppelin(vagrant_cmd: str, service_name: str):
    '''
    Start Apache Zeppelin service.
    '''  
    try:
        logger.info(f"Starting Apache Zeppelin service...")
        ssh_cmd = f"sudo systemctl start {service_name}"
        ret = subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'", check=True)
    except Exception as err:
        logger.error(f"Error starting Apache Zeppelin service: {err}.")   
#----------------------------------------------------------------------
@logger.catch
def create_zeppelin_service(vagrant_cmd: str, install_dir: str, service_name: str, service_file_path: str):
    '''
    Create Apache Zeppelin service.
    '''    
    try:
        logger.info(f"Creating Apache Zeppelin service user...")
        ssh_cmd = f"sudo adduser -d {install_dir} -s /sbin/nologin {service_name}"
        subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'")

        logger.info(f"Providing ownership of the files to the Zeppelin user....")
        ssh_cmd = f"sudo chown -R {service_name}:{service_name} {install_dir}"
        subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'", check=True)

        cur_path = path.dirname(path.abspath(__file__))
        service_file_path = path.join(cur_path, service_file_path)
        with open(service_file_path) as buf:
            service_str = buf.read()
        
        service_str = service_str.replace("{install_dir}", install_dir)
        service_str = service_str.replace("{user}", service_name)
        service_str = service_str.replace("{group}", service_name)
        service_str = service_str.strip()
        
        logger.info(f"Creating Apache Zeppelin .service file by the file {service_name}.service...")
        ssh_cmd = f"sudo echo '{service_str}' > {service_name}.service"
        cmd = f"{vagrant_cmd} \"{ssh_cmd}\""
        subprocess.run(cmd, check=True)
        
        ssh_cmd = f"sudo mv {service_name}.service /etc/systemd/system/{service_name}.service"
        subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'", check=True)
        
        start_zeppelin(vagrant_cmd, service_name)

        logger.info(f"Enable Zeppelin service to automatically start at boot time...")
        ssh_cmd = f"sudo systemctl enable {service_name}"
        subprocess.run(f"{vagrant_cmd} '{ssh_cmd}'", check=True)
    except Exception as err:    
        logger.error(f"Error creating Apache Zeppelin service: {err}.")

if __name__ == "__main__":

    zeppelin_install_dir = "/opt/zeppelin"
    zeppelin_service_name = "zeppelin"
    zeppelin_service_file_path = path.join("vagrant", "zeppelin.service")

    # Get program path
    app_dir = path.dirname(path.realpath(__file__))

    # Vagrant path
    vagrant_path = path.join(app_dir, "vagrant")
    # Change workdir to vagrant path

    os.chdir(vagrant_path)
    vagrant_cmd = f"vagrant ssh -c"

    # Inicializa a máquina virtual
    vagrant_up()

    # Updating yum
    update_yum(vagrant_cmd)

    # Verify if wget is installed
    if not verify_wget(vagrant_cmd):
        # Install wget
        install_wget(vagrant_cmd)

    # Verify if Java is installed
    if not verify_java(vagrant_cmd):
        install_java(vagrant_cmd)

    # Verify if Apache Zeppelin is installed
    if not verify_zeppelin(vagrant_cmd):
        install_zeppelin(vagrant_cmd, zeppelin_install_dir)

    # Create Apache Zeppelin Service
    create_zeppelin_service(vagrant_cmd, zeppelin_install_dir, zeppelin_service_name, zeppelin_service_file_path)
