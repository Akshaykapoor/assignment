/*
This is the config used when we do the initial setup phase.
When the first instance is instanciated, changes to the nginx config
to relfect the name of the upstream servers is done in this file
*/

var nginx_conf_file = '/usr/local/etc/nginx/nginx.conf'
var NginxConfFile = require('nginx-conf').NginxConfFile;

// Since we know the first node instance starts on 8080, we add this value to the variable
// Ideallly all this is prefeable when done through Configuration Management tools
var default_addr = '127.0.0.1:8080' //

// Using the deault config location of nginx file
NginxConfFile.create(nginx_conf_file, function(err, conf) {
  if (err) {
    console.log(err);
    return;
  }

var yargs = require('yargs').argv;
var app_name = yargs.app;
console.log(app_name);

var proxy_pass = 'http://' + app_name;
conf.nginx.http._add('server');
conf.nginx.http.server[1]._add('listen', '0.0.0.0:80');
conf.nginx.http.server[1]._add('server_name', app_name);
conf.nginx.http.server[1]._add('location', '/');
conf.nginx.http.server[1].location._add('proxy_pass', proxy_pass);
conf.nginx.http._remove('server')

// Now to add upstream so that all servers are treated as backend for load_balancing
conf.nginx.http._add('upstream', app_name)
conf.nginx.http.upstream._add('server', default_addr)
});
