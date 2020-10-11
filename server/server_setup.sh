#!/usr/bin/env bash

# Consider running these two commands separately
# Do a reboot before continuing.
apt update
apt upgrade -y

apt install zsh # Need to look up documentation on this shell "oh-my-zsh."
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# Install some OS dependencies:
sudo apt-get install -y -q build-essential git unzip zip nload tree #look up build-essential, nload, unzip, zip, nload, tree on SO
sudo apt-get install -y -q python3-pip python3-dev python3-venv
sudo apt-get install -y -q nginx
# for gzip support in uwsgi.  Why is this needed?
sudo apt-get install --no-install-recommends -y -q libpcre3-dev libz-dev

# Stop the hackers>  Lookup fail2ban.
sudo apt install fail2ban -y

ufw allow 22
ufw allow 80
ufw allow 443
ufw enable

# Basic git setup
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=720000'

# Be sure to put your info here:
git config --global user.email "aambrioso1@gmail.com"
git config --global user.name "aambrioso"

# Web app file structure
mkdir /apps
chmod 777 /apps # WHat does this do?
mkdir /apps/logs
mkdir /apps/logs/erika_site
mkdir /apps/logs/erika_site/app_log
cd /apps

# Create a virtual env for the app.
cd /apps
python3 -m venv venv # Then . venv/bin/activate to activate the virtual environment.
source /apps/venv/bin/activate # Or . venv/bin/activate to activate the virtual environment.
pip install --upgrade pip setuptools
pip install --upgrade httpie glances
pip install --upgrade uwsgi

#  To activate the apps virtual environment add source /apps/venv/bin/activate to .zshrc using nano (bashrc).
# clone the repo:
cd /apps
git clone https://github.com/aambrioso1/erika_site

# Setup the web app:
cd cd /apps/erika_site/
pip install -r requirements.txt

# Copy and enable the daemon
cp /apps/erika_site/server/erika_site.service /etc/systemd/system/erika_site.service

systemctl start erika_site
systemctl status erika_site
systemctl enable erika_site

# Setup the public facing server (NGINX)
apt install nginx

# CAREFUL HERE. If you are using default, maybe skip this
rm /etc/nginx/sites-enabled/default

cp /apps/erika_site/server/erika_site.nginx /etc/nginx/sites-enabled/erika_site.nginx
update-rc.d nginx enable
service nginx restart


# Optionally add SSL support via Let's Encrypt:
# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04

add-apt-repository ppa:certbot/certbot
apt install python-certbot-nginx
certbot --nginx -d erikaambrioso.com
