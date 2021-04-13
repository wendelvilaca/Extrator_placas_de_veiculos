
/*server.js*/
const http = require('http');
const hostname = 'retornaplaca.azurewebsites.net';
const port = 80;



const server = http.createServer(function (req, res) {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/json');
    res.charset = 'ISO-8859-1';
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
                console.log(err);
                res.end(err.Error);
            });
        //res.end("a");
    }

});
server.listen(port, hostname, function () {
    console.log('Server running at http://' + hostname + ':' + port + '/');
});