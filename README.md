Assignment

Disclaimer:

All of this has been battle tested on OS X 10.10.4 under a specific environemt. 

This project includes the following file:

1. initial_setup.py - Does initial setup of setting up environment
                      installing packages and running nginx
2. configure_nginx.py - Starts nginx server on the default port

3. nginx.conf - Config file used for starting nginx on port 80
                (This task is essentially managed by Chef/Saltstack)
                But in the scope of this assignment, we just supply an initial config

4. log.py - Global logger module to enable logging

5. autoscale.py - Handles the autoscaling and stopping of server process

6. initial-nginx.js - After starting nginx, we do your initial phase, we use this file

7. update-nginx.js - This is used when we are in the process of scaling up or down
                     (Allows to change nginx config dynamically)

8. reload.sh - Used to reload the nginx config

------------------------------------------------------------------------------------------------------------

Steps to do:

Make sure to run all of the above as root user. 
This is because nginx needs to be run on port 80.
There are multiple ways to achieve this,
  - we can use iptables to forward all traffic on 80 to some less privilege port

1. Have all the pre-req installed
     - pip
     - node.js v4.5.0
     - npm
     - npm install yargs
     - npm install nginx-conf

2. Run configure_nginx.py (to run nginx on port 80)

3. Run python initial_setup.py to clone from git and run node server, and add to LB

4. Run python autoscale.py (Run in a while loop to simulate number of requests and scaling up and down)

------------------------------------------------------------------------------------------------------------

For the questions:

  - Start new nginx server on port 80
	   - The best approach for doing such things is by using a configuration
       management tool like Saltstack, Chef etc (depending upon the deployment)
     - Done in configure_nginx.py
  - create node.js environment
	   - This involves making sure app packages are installed for node.js and
       node.js itself is installed. Again better of to be done with Saltstack/Chef
     - Done in initial_setup.py
  - pull git repo and start server
     - Also done in initial_setup.py (This is because this is an 1 time task)

  - Add server to LB when requests /minute > 100
  - Remove backend from LB and stop the last service when requests < 100
      - The above 2 tasks are managed in autoscale.py (which simulates a request
        per minute mechanism and run in while loop unless interrupted)

------------------------------------------------------------------------------------------------------------

This assignment does the following,

1. Create an initial config which does the following:

    a. Install required pip packages for installation (Installing npm and node.js
        is assumed to be installed by Chef/Saltstack or any other tool)
        
        1. Install nginx (and change the config if required to include upstream)
        
    b. Configure the system to install packages, clone the specified git repo
    
    c. Run the node.js app from the cloned repo

2. Once, the app is up and running, we simulate the number of requests per minute

    a. RPM (Request per minute) is simulated by generating a random integer between 90 and 110
    
        1. Another approach of getting the total number of requests is by using status modules (vanialla nginx
           installations using any package manager such as yum, apt-get are not installed with this module) within nginx.
           To install this module, nginx has to be  compiled from source with the required flags.
           Using this approach, we can take samples from the status module every minute and get the difference
           from the last minute until now.
           
        2. We could also parse the access.log file to get the number of requests per minute, but this seems quite
           expensive to be built on top, unless done natively by the server.
           
    b. If RPM is > 100, we spin up a node.js application and add it's config to nginx and reload nginx
    
    c. If RPM < 100 and the total number of instances is > 1, we remove the instance from the load balancer
       and the server process is also stopped.

------------------------------------------------------------------------------------------------------------
FAQ:

Q - How do you keep track of the last node server started ?
A - We do this with the help of a variable (LAST_PROCESS_PORT), which is a global variable
    updated whenever a new server is added. Better approaches of having this information available
    are also possible by having a datastore which could be persistent and shared across many modules.
    Can also be done by writing to a file


#########################################################################################

In the interest of time and scope of this assignment, a vagrant box is not supplied
so as to simulate everything.
#########################################################################################
