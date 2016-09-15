var NginxConfFile = require('nginx-conf').NginxConfFile;
var nginx_conf_file = '/etc/nginx/nginx.conf'
// Using the deault config location of nginx file
NginxConfFile.create(nginx_conf_file, function(err, conf) {
  if (err) {
    console.log(err);
    return;
  }

var yargs = require('yargs').argv;

/*
console.log(yargs.ip);
console.log(yargs)
console.log(yargs.count);
*/

// Depeing on the value supplied we either update or delete the server
// address from the config
if (yargs.ip == 'None') {
    // This mean a count has been passed, get this value and store in var
    var count = yargs.count
    conf.nginx.http.upstream._remove('server', count);
}
else {
    var localhost = '127.0.0.1:'
    var server_addr = localhost + yargs.ip
    conf.nginx.http.upstream._add('server', server_addr);
}
});
