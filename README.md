# Nikky Server

This app is written in Laravel 7 made to work as a command and control for various services which can be deployed on Linux based machines.

## Pre-requsities
- Install Php 7.2
- Install MySQL Database and create credentials (Ovbiously)
Here's a guide on it https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04

## Getting started
    
    git clone https://github.com/joshiabir/nikky.git
    cd ./nikky
    
    # Edit the .env file for MySQL credentials
    php artisan migrate
    php artisan serve --port=8080

    # This will start a server on port 8080
    


