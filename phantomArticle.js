var fs = require('fs'),
    sys = require('system'),
    page = require('webpage').create(),
    domain, pii, url, f;

pii=['S0020751900001272','S0306453007001205','S0022314X03000155'];

//    url = 'http://www.sciencedirect.com/science/article/pii/S0020751900001272';
if (sys.args.length < 2 ) {
    console.log('Usage: phantomArticle.js <SD Domain> <PII file Path>');
    phantom.exit(1);
} else {

    domain = sys.args[1];
    //for (var i=0; i<pii.length; i++){
        var s=Date.now();
        url='http://'+domain+'/science/article/pii/'+pii[0];
        //url = 'http://www.sciencedirect.com/science/article/pii/S0020751900001272';
        console.log(url);
        page.open(url, function (status) {
            if (status !== 'success') {
                 console.log('Unable to access network');
            } else {
               var t=Date.now()-s;
	       console.log('load time:'+t);
            }
            phantom.exit();
        });
    //}
}
