var express = require('express');
var router = express.Router();
var path = require('path')
var baseDir = path.dirname(require.main.filename);

/* GET home page. */
router.get('/', function (req,res) {
    // res.sendFile(baseDir + "/views/index.html");
    req.session.valid = 12;
    res.redirect('/dash');
    // res.render('dash', { title: "Whatsapp Analyser" });
});

router.get('/dash', function (req, res) {
    console.log(req.session.valid);
    // res.send("Dash");
    res.render('dash', { title: "Whatsapp Analyser" });
});

module.exports = router;