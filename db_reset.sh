#!/bin/bash
read -p "Are you sure you want to reset the flaskapp db? <y/N> " prompt
if [[ $prompt == "y" || $prompt == "Y" || $prompt == "yes" || $prompt == "Yes" ]]
then
    sudo mysql < "DROP DATABASE IF EXISTS flaskapp;"
    sudo mysql < db_setup.sql
    sudo mysql < "INSERT INTO users (email, username, password, is_admin) values ('mfanx2@gmail.com', 'mfanx2', '088409e872857b396b89ab899245c7a4', 1);"
    sudo mysql < "INSERT INTO users (email, username, password, is_admin) values ('test_admin@selenium.test', 'test_admin', 'a08099eb3efa177a74bee07ee30552a1', 1)"
    echo "flaskapp db reset"
else
    echo "flaskapp db not reset"
    exit 0
fi