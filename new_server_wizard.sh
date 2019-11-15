#!/bin/bash

printf "This Script will guide you through making a new webapp1 flask server\n\n"
read -p "Are you sure you want to continue? <y/N> " prompt
if [[ $prompt == "y" || $prompt == "Y" || $prompt == "yes" || $prompt == "Yes" ]]
then
    echo
    read -p "Enter the IP address of the new server: " ip_address
    printf "\nCreating .ssh dir if does not exist already (requires password)\n"
    ssh mfanx2@$ip_address mkdir -p ~/.ssh
    printf "\nEnabling ssh login without password (requires password again)\n"
    cat ~/.ssh/id_rsa.pub | ssh mfanx2@$ip_address 'cat >> .ssh/authorized_keys'
    printf "\nEnabling passwordless sudo  (requires password one last time)\n"
    ssh -t mfanx2@$ip_address "echo '%sudo ALL=(ALL:ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo"
    printf "\nCreating certs dir if does not exist already\n"
    ssh mfanx2@$ip_address mkdir -p ~/certs
    printf "\nCopying certificate files to ~/certs/\n"
    scp ~/certs/*.pem mfanx2@$ip_address:~/certs/
    printf "\nListing all docker containers\n"
    ssh mfanx2@$ip_address sudo docker ps -a
    printf "\nRunning Ansible Playbook\n"
    ansible-playbook --extra-vars "target=$ip_address ansible_user=mfanx2 ansible_python_interpreter=/usr/bin/python3" -i $ip_address, deploy.yml
    printf "\nListing all docker containers again\n"
    ssh mfanx2@$ip_address sudo docker ps -a
    printf "\nInitializing Database\n"
    ssh mfanx2@$ip_address "echo y | ./db_reset.sh"
    printf "\nSuccessfully executed script new_server_wizard.sh\n"
    exit 0
else
    printf "\nAborted script new_server_wizard.sh\n"
    exit 1
fi