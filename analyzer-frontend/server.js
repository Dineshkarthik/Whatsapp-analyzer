// var express    =    require('express');
// var app        =    express();


// require('./router/main')(app);
// app.set('views',__dirname + '/views');
// app.set('view engine', 'ejs');
// app.engine('html', require('ejs').renderFile);

// var server     =    app.listen(3000,function(){
// console.log("Express is running on port 3000");
// });



var express =   require("express");
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var session = require('express-session')
var multer  =   require('multer');
var request = require('request');

var app = express();
var routes = require('./routes/index');
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');
// uncomment after placing your favicon in /public
//app.use(favicon(__dirname + '/public/favicon.ico'));
app.use(logger('dev'));
app.use(session(
  {
    secret: 'iwillusehokagokaaspasswordbecauseican',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: true }
  }
));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

var storage =   multer.diskStorage({
  destination: function (req, file, callback) {
    callback(null, '../analyser/data');
  },
  filename: function (req, file, callback) {
    var filename = file.fieldname + '-' + Date.now()+ '.txt'
    callback(null, filename);
  }
});
var upload = multer({ storage : storage, limits: {fileSize: 2000000, files:1}}).single('chatHistory');

app.use('/', routes);

app.post('/about', upload, function(req, res, err) {
  res.end("File is uploaded");
  request("http://localhost", function (err, response, body) {
    console.log(body);
  })
});

app.listen(3000,function(){
    console.log("Working on port 3000");
});