#!/bin/bash

printf "This Script will guide you through making a new webapp1 flask server\nNOTE: It is important that you only run this script once\n\n"
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
    printf "\nStopping any running webapp1 docker container\n"
    ssh mfanx2@$ip_address sudo docker stop webapp1
    printf "\nListing all docker containers\n"
    ssh mfanx2@$ip_address sudo docker ps -a
    printf "\nPruning docker images and containers\n"
    ssh mfanx2@$ip_address sudo docker image prune -f
    ssh mfanx2@$ip_address sudo docker system prune -f
    printf "\nSuccessfully executed script new_server_wizard.sh\n"
    exit 0
else
    printf "\nAborted script new_server_wizard.sh\n"
    exit 1
fi