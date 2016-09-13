import log
import time
import socket
import subprocess
from random import randint

'''
We use these global variables to maintain the state of the different backend servers being load balanced
LAST_UNUSED_PORT is used to keep track of the last server process which was started, so as to be able to delete
the last spawned node instance if the requests per minute is less than 100

'''

BACKEND_SERVER_COUNT = 0
LAST_PROCESS_PORT = []
APP_NAME = 'helloworld_app'

logger = log.enable_logging('autoscale')

def get_requests():
    random_int = randint(90,110)
    return random_int

def PickUnusedPort():
    '''
    Gets the next availabe port number to start the node process
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    addr, port = s.getsockname()
    s.close()
    global LAST_PROCESS_PORT
    LAST_PROCESS_PORT.append(port)
    return port

def start_app(port):
    '''
    Start the node app which has been earlier
    '''
    command = 'node {0}/main.js --port {1}'.format(APP_NAME, port)
    # We use Popen here, so that it is a non-blocking call. At times it may
    # take some time for the process to be up and running. In the interim we can
    # update our nginx config and reload to reflect the same
    try:
      p = subprocess.Popen(command, shell = True, stdin = None, stdout = None, stderr = None)
    except OSError as e:
      logger.info('OS Error {0}'.format(e))
    except ValueError as e:
      logger.info('Value Error {0}'.format(e))
      logger.info('Could not start proces: {0}'.format(e))
    logger.info('Node process has been started on localhost and port: {0}'.format(port))

def reload_nginx_config():
    '''
    We are using reload.sh file to reload nginx config.
    There were issues when trying to reload on OS X with subprocess call
    '''
    command = '/usr/local/bin/nginx -s reload'
    p = subprocess.call(['./reload.sh'])
    if not p:
        logger.info('Nginx has been reloaded successfully...')
    else:
        logger.debug('Nginx config could not be reloaded')

def update_nginx_config(port=None, count=None):
    command = 'node javascript/update-nginx.js --ip={0} --count={1}'.format(port, count)
    logger.debug('Updating nginx config with the following command: {0}'.format(command))
    p = subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None)
    if port:
        global BACKEND_SERVER_COUNT
        BACKEND_SERVER_COUNT += 1
        logger.info('Total server count after addition is: {0}'.format(BACKEND_SERVER_COUNT))
    else:
        BACKEND_SERVER_COUNT -= 1
        logger.debug('Total server count after deletion is: {0}'.format(BACKEND_SERVER_COUNT))
    reload_nginx_config()

def kill_node_process(port):
    '''
    We stop the node server by sending it a sigkill signal
    It can be killed gracefully, by adding a signal handler in the
    javascript code.
    So that some preventinve actions can be taken when
    killing the process or some process can be notified of the removal of the service
    ps -ef | grep -v grep | grep "<port number>" | awk -F ' ' '{print $2}'
    '''
    command = "ps -ef | grep -v grep | grep \"%s\" | awk -F ' ' '{print $2}'" % port
    pid = subprocess.check_output(command, shell=True)
    logger.debug('PID to stop node server is: {0}'.format(pid))
    stop_cmd = 'kill -9 {0}'.format(pid)
    p = subprocess.check_output(stop_cmd, shell=True)
    logger.debug('Node server binding on port {0} has been stopped'.format(port))

while True:
    logger.info('Sart time for the 1-minute sampling: %s' % time.ctime())
    logger.info('Sleeping for 60 seconds to get simulate requests per minute sampling')
    time.sleep(60)
    if get_requests() >= 100:
        # Since the simulated value is greater than 100
        # we need to add a new node.js server instance
        # on the next available port number
        port = PickUnusedPort()
        logger.debug('Port number selected for instantinating node server is: {0}'.format(port))
        # Start a new node app and add this to a new
        # config to nginx also
        start_app(port)
        update_nginx_config(port=port)
        print 'Nginx config should be updated now'
    else:
        if BACKEND_SERVER_COUNT >= 1:
            update_nginx_config(count=BACKEND_SERVER_COUNT)
            # gracefully kill the node process using LAST_PROCESS_PORT
            logger.info('Last added node server needs to be removed as RPM is less than threshold')
            # We kill the process with SIGKILL, as explained the method description above
            kill_node_process(LAST_PROCESS_PORT.pop())
        else:
            logger.info('Only 1 instance of node server is running. We should not remove that')
            pass


    logger.info('End time for the 1-minute sampling: %s' % time.ctime())
