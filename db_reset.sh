#!/bin/bash
read -p "Are you sure you want to reset the flaskapp db? <y/N> " prompt
if [[ $prompt == "y" || $prompt == "Y" || $prompt == "yes" || $prompt == "Yes" ]]
then
    sudo mysql < "DROP DATABASE IF EXISTS flaskapp;"
    sudo mysql < db_setup.sql
    echo "flaskapp db reset"
else
    echo "flaskapp db not reset"
    exit 0
fi