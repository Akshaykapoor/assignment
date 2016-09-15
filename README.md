#Assignment

####Disclaimer: All of this has been battle tested on OS X 10.10.4 under a specific environment.
##(UPDATE): This has now been ported to run on ubuntu (Vagrantfile to the rescue !)

**This project includes the following file:**

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

9. Vagrantfile - Used for baking your environment

10. setup.sh - Used by vagrant to setup the environment.


##Steps to do:

This assumes you have vagrant installed and can spin up VMs and vagrant box to
instantiate the same.
I've used Virtualbox and ubuntu 12.04

1. vagrant box add precise64 https://files.hashicorp.com/precise64.box
2. git clone https://github.com/Akshaykapoor/assignment.git
3. cd assignment/vagrant
4. vagrant up
5. vagrant ssh
6. cd assignment --> So that you can execute the assignment
7. sudo python configure_nginx.py (to run nginx on port 80)
8. sudo python initial_setup.py (clones the node app and adds it to LB)
      At this point you should be able to confirm both (node and nginx) are working by
      either going to the browser on http://localhost if your guest and host ports are mapped
      or running the commands below from command line

      `curl http://localhost (nginx load balancing the node app)`
      
      `curl http://localhost:8080 (node server listening on )`
      
9. sudo python autoscale.py
      This will run in an infinite loop simulating number of requests
      per minute. 
      At this pint you can do `tailf setup.log` to see what is happening

The above is run as root user, because nginx needs to be run on port 80.
There can be multiple ways to avoid running as root,
  - we can use iptables to forward all traffic on 80 to some less privilege port

##For the questions:

  - Start new nginx server on port 80
	   - The best approach for doing such things is by using a configuration
       management tool like Saltstack, Chef etc (depending upon the deployment)
     - Done in configure_nginx.py
  - create node.js environment (Most of the environment setup is done in the shell script for Vagrant)
	   - Again better of to be done with Saltstack/Chef. We do install a python package
       specific for one of the task from the code itself.
     - Done in initial_setup.py
  - pull git repo and start server
     - Also done in initial_setup.py (This is because this is an 1 time task)

  - Add server to LB when requests /minute > 100
  - Remove backend from LB and stop the last service when requests < 100
      - The above 2 tasks are managed in autoscale.py (which simulates a request
        per minute mechanism and run in while loop unless interrupted)
        Maintaining node information in cluster (for scaling) is usually done by a cluster manager.
        For the scope of this project, we implement a way to simulate the same.


**This assignment does the following,**

1. Create an initial config which does the following: (Update: Added a vagrant file which handles
   all dependencies for setting up the environment)

    a. Setup the system environment with packages dependencies for running the assignment,
       clone the specified git repo

    b. Run the node.js app from the cloned repo

2. Once, the app is up and running, we simulate the number of requests per minute

    a. RPM (Request per minute) is simulated by generating a random integer between 90 and 110

        1. Another approach of getting the total number of requests is by using ngx_http_stub_status_module (vanialla nginx
           installations using any package manager such as yum, apt-get are not installed with this module) within nginx.
           To install this module, nginx has to be  compiled from source with the required flags.
           Using this approach, we can take samples from the status module every minute and get the difference
           from the last minute until now.

        2. We could also parse the access.log file to get the number of requests per minute, but this seems quite
           expensive to be built on top, unless done natively by the server.
           
        3. Or can have that information be feeded to this code from some monitoring solution

    b. If RPM is > 100, we spin up a node.js application and add it's config to nginx and reload nginx

    c. If RPM < 100 and the total number of instances is > 1, we remove the instance from the load balancer
       and the server process is also stopped.

##FAQ:

Q - How do you keep track of the last node server started ?
A - We do this with the help of a list variable (LAST_PROCESS_PORT), which is a global list
    updated with the port number whenever a new server is added. Better approaches of having this information available
    are also possible by having a datastore which could be persistent and shared across many modules.
    Can also be done by writing to a file.
