
/*server.js*/
const http = require('http');
const hostname = '127.0.0.1';
var utf8 = require('utf8');
const port = 3000;
const express = require('express')

const server = http.createServer();

/*
setTimeout(function () {

    //process.exit(1);
    // console.log("closing");
}, 60000);
*/
server.on('request', (req, res) => {
    res.statusCode = 200;
    //   res.setHeader('Content-Type', 'text/json');
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    // res.charset = 'ISO-8859-1';
    var sinespApi = require("sinesp-api")
    sinespApi.configure();
    var id = req.url.substring(1);
    console.log(req.url);
    if (id != "favicon.ico") {

        let vehicle = sinespApi.search(id);

        vehicle.then(
            function (val) {
                // res.end(val.situacao + " - " + val.modelo);
                res.write(JSON.stringify(val));
                res.end();
                console.log(val);

            }).catch(function (err) {
                res.write(err.toString());
                res.end();
                res.end();
               // throw ("error");
                //next(res);
                //process.exit(1);
            });
        //res.end("a");
    }
});
server.on('end', () => {
    console.log("END");
    
});

server.listen(port, hostname, function () {
    console.log('Server running at http://' + hostname + ':' + port + '/');
});