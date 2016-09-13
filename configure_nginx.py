'''
This is the initail csript to configure nginx.

Ideally we could have used templating (such as jinja, Maco etc)to change the config file
For the scope of this assignment. We will use an nginx config supplied
and residing at the same dir as this file.

Copy this file to the correct default locaiton of nginx on Mac OS X


This script assumes that nginx is installed on your machine
and it can be started via system calls such as systemd, service, launchctl etc
This is demonstrated on a mac OS X. Vanilla installations for mac, doesn't include the
.plist file which is used to call the service at startup

Having a .pllist file is out of scope of this assignment. (As mostly this is usually handled very well by Configuration management tools)

We use the default installation nginx file location. '/usr/local/etc/nginx/nginx.conf'

Tested on (Mac OS X 10.10.4)

author = Akshay Kapoor
'''
import subprocess
import time
import sys
import os
import log
from shutil import copyfile

logger = log.enable_logging('nginx')

def start_nginx():
    sourcefilepath = os.path.abspath('nginx.conf')
    destinationfilepath = '/usr/local/etc/nginx/nginx.conf'
    copyfile(sourcefilepath, destinationfilepath)
    command = 'nginx -c {0}'.format(destinationfilepath)
    logger.info('Command used for starting is: {0}'.format(command))
    # we use subprocess.call, because we make this a blocking call,
    # so as to wait for the result of the exceution
    try:
      p = subprocess.call([command], shell=True)
    except CalledProcesError as e:
      logger.info('Subprocess failed with %s' % e)
    if p:
        logger.info('Nginx failed to start with exit ')
    else:
        logger.info('Nginx is now listening on 127.0.0.1:80....')

def main():
    '''
    Main method for nginx config
    '''
    start_nginx()
    sys.exit(0)


if __name__ == '__main__':
    main()
