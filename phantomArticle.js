var sys = require('system'),
    page = require('webpage').create(),
    domain, pii, url, f;

//    url = 'http://www.sciencedirect.com/science/article/pii/S0020751900001272';
if (sys.args.length < 2 ) {
    console.log('Usage: phantomArticle.js <SD Domain> <PII file Path>');
    phantom.exit(1);
} else {

    domain = sys.args[1];
    pii=sys.args[2];
    url='http://'+domain+'/science/article/pii/'+pii;
    //url = 'http://www.sciencedirect.com/science/article/pii/S0020751900001272';
    console.log(url);
    var s=Date.now();
    page.open(url, function (status) {
       if (status !== 'success') {
          console.log('Unable to access network');
       } else {
          var t=Date.now()-s;
          console.log('load time:'+t);
          console.log(page.evaluate(function () {return document.title;}));
       }
       phantom.exit();
   });
}

