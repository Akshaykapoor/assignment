import os
import pip
import log
import time
import sys
import subprocess

'''
This code achieves the following, under the assumption that the following hold true
a. system has python 2.7 installed
b. system has pip installed
c. system has node.js installed v4.5.0
	1. To install on mac, you can use the following wiki, https://coolestguidesontheplanet.com/installing-node-js-on-osx-10-10-yosemite/
        2. Install npm package yargs

1. Installs pip packages
2. Clones the git repo for the node app
3. Starts the server
4. Updates the nginx config and reloads it

'''

APP_NAME = 'helloworld_app'
LOGGER = log.enable_logging('root')


def install(package):
	'''
	If the installation of packages is a big list. It is
	recommended to use a requirements.txt and add all package dependency to that file
	All this should be taken care of by the Chef, Saltstack etc
	'''
	LOGGER.info('Package installed: {0}'.format(package))
	pip.main(['install', package])

def create_git_repo():
    '''
    Clones the git project in a dir named helloworld_app
    '''
    from git import Repo
    directory = APP_NAME
    if not os.path.exists(directory):
        os.makedirs(directory)
    git_url = 'https://github.com/chetandhembre/hello-world-node.git'
    Repo.clone_from(git_url,directory)
    LOGGER.info('Fetching git clone done....')

def reload_nginx_config():
    command = '/usr/local/bin/nginx -s reload'
    p = subprocess.call(['./reload.sh'])
    if not p:
        LOGGER.info('Nginx has been reloaded successfully...')
    else:
        LOGGER.debug('Nginx config could not be reloaded')

def register_in_nginx():
    command = 'node javascript/initial_nginx.js --app={0}'.format(APP_NAME)
    p = subprocess.check_output(command, shell=True)
    LOGGER.debug('Command usd for starting app is {0}'.format(command))
    reload_nginx_config()

def initial_start_app():
    '''
    Start the node app which has been cloned earlier
    '''
    command = 'node helloworld_app/main.js'
    LOGGER.info('Starting the node app')
    p = subprocess.Popen(command, shell = True, stdin = None, stdout = None, stderr = None)
    LOGGER.info('App is starting in background. Reload nginx config to see changes')
    register_in_nginx()

def main():
    LOGGER.info('Starting the initial setup phase')
    LOGGER.info('Installing packages...')
    install('gitpython')
    create_git_repo()
    initial_start_app()
    sys.exit(0)

if __name__ == '__main__':
    main()
