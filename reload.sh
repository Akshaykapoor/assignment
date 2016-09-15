#!/bin/sh

# Command to reload default nginx config residing at the default location.
#/usr/local/bin/nginx -s reload --> removing this as this was for doing it on mac os x

# for nginx on ubnutu it will have the inti file, so we use the following,
sudo service nginx reload
