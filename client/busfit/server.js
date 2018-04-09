var express = require('express');  
var app = express();  
var server = require('http').createServer(app);  
var io = require('socket.io')(server);

var gsock = io.on('connection', function(client) {  
    console.log('Client connected...');
    client.on('data', function(data) {
        console.log(data);

    });
});

var sendToClient = function(data){
	if (gsock && gsock.connected){
		console.log('Sending to client...');
		gsock.emit('data', data)
	}
};

app.get('/api/:farOrNot', function(req, res, next) {  
    var body = req.body || req.params || req.query;
    console.log(body);
    sendToClient({tooClose: body.farOrNot == 1 ? true : false});
    res.json({success: true});
});

app.get('/api/:counter/:drill', function(req, res, next) {  
    var body = req.body || req.params || req.query;
    console.log(body);
    sendToClient({counter: Number(body.counter), drill: body.drill});
    res.json({success: true});
});

server.listen(3001);

