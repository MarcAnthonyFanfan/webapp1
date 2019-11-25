#!/bin/bash

function quit {
    # printf "\nAborted script new_server_wizard.sh\n"
    dialog --title "New Server Wizard" --msgbox "Aborted script new_server_wizard.sh" 5 40
    exit 1
}
function cancel_if_selected {
    case $? in
        1)
            quit
        ;;
    esac
}

dialog --title "New Server Wizard" --yesno "This Script will guide you through making a new webapp1 flask server.\n\nAre you sure you want to continue?" 8 40
case $? in
    0)
        ip_address=$(dialog --title "New Server Wizard" --inputbox "Enter the IP address of the new server " 8 50 3>&1 1>&2 2>&3); cancel_if_selected
        username=$(dialog --title "New Server Wizard" --inputbox "Enter your username for $ip_address " 8 50 3>&1 1>&2 2>&3); cancel_if_selected
        password=$(dialog --title "New Server Wizard" --insecure --passwordbox "Enter your password for $username@$ip_address" 8 50 3>&1 1>&2 2>&3); cancel_if_selected
        # confirmation=$(dialog --title "New Server Wizard" --insecure --passwordbox "Confirm your password for $username@$ip_address" 8 50 3>&1 1>&2 2>&3); cancel_if_selected
        # if [ "$password" == "$confirmation" ]; then
        #     :
        # else
        #     printf "\nPassword and confirmation do not match\n"
        #     quit
        # fi
        dialog --title "New Server Wizard" --infobox "Enabling passwordless sudo\n(this will require your password again)" 5 50; sleep 2
        (sshpass -p $password ssh -t $username@$ip_address "echo '%sudo ALL=(ALL:ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo")
        (sshpass -p $password ssh $username@$ip_address mkdir -p ~/.ssh) >/dev/null 2>&1
        dialog --title "New Server Wizard" --infobox "Creating .ssh dir if does not exist already" 5 50; sleep 2
        (cat ~/.ssh/id_rsa.pub | sshpass -p $password ssh $username@$ip_address 'cat >> .ssh/authorized_keys') >/dev/null 2>&1
        dialog --title "New Server Wizard" --infobox "Enabling ssh login without password" 5 50; sleep 2
        (ssh $username@$ip_address mkdir -p ~/certs) >/dev/null 2>&1
        dialog --title "New Server Wizard" --infobox "Creating certs dir if does not exist already" 5 50; sleep 2
        (scp ~/certs/*.pem $username@$ip_address:~/certs/) >/dev/null 2>&1
        dialog --title "New Server Wizard" --infobox "Copying certificate files to ~/certs/" 5 50; sleep 2
        (ansible-playbook --extra-vars "target=$ip_address ansible_user=$username ansible_python_interpreter=/usr/bin/python3 ansible_sudo_pass=$password" -i $ip_address, deploy.yml; sleep 2)  | dialog --title "New Server Wizard" --progressbox "Running Ansible Playbook" 20 76
        echo $password | (ssh -t $username@$ip_address "echo y | ./db_reset.sh") >/dev/null 2>&1
        dialog --title "New Server Wizard" --infobox "Initializing Database" 5 50; sleep 2
        dialog --title "New Server Wizard" --msgbox "Finished script new_server_wizard.sh" 5 40
        exit 0
    ;;
    1)
        quit
    ;;
esac

#printf "This Script will guide you through making a new webapp1 flask server\n\n"
#read -p "Are you sure you want to continue? <y/N> " prompt

# if [[ $? > 0 ]]
# then
#     echo
#     read -p "Enter the IP address of the new server: " ip_address
#     printf "\nCreating .ssh dir if does not exist already (requires password)\n"
#     ssh $username@$ip_address mkdir -p ~/.ssh
#     printf "\nEnabling ssh login without password (requires password again)\n"
#     cat ~/.ssh/id_rsa.pub | ssh $username@$ip_address 'cat >> .ssh/authorized_keys'
#     printf "\nEnabling passwordless sudo  (requires password one last time)\n"
#     ssh -t $username@$ip_address "echo '%sudo ALL=(ALL:ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo"
#     printf "\nCreating certs dir if does not exist already\n"
#     ssh $username@$ip_address mkdir -p ~/certs
#     printf "\nCopying certificate files to ~/certs/\n"
#     scp ~/certs/*.pem $username@$ip_address:~/certs/
#     printf "\nListing all docker containers\n"
#     ssh $username@$ip_address sudo docker ps -a
#     printf "\nRunning Ansible Playbook\n"
#     ansible-playbook --extra-vars "target=$ip_address ansible_user=$username ansible_python_interpreter=/usr/bin/python3" -i $ip_address, deploy.yml
#     printf "\nListing all docker containers again\n"
#     ssh $username@$ip_address sudo docker ps -a
#     printf "\nInitializing Database\n"
#     ssh $username@$ip_address "echo y | ./db_reset.sh"
#     printf "\nFinished script new_server_wizard.sh\n"
#     exit 0
# else
#     printf "\nAborted script new_server_wizard.sh\n"
#     exit 1
# fi