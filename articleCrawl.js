// Render Multiple piis to file

var RenderpiisToFile, arrayOfpiis, system;

system = require("system");

//////////////////////////////////
// Render given piis
// @param array of piis to render
// @param callbackPerpii Function called after finishing each pii, including the last pii
// @param callbackFinal Function called after finishing everything

RenderpiisToFile = function(piis, callbackPerpii, callbackFinal) {
    var getFilename, next, page, retrieve, piiIndex, webpage;
    piiIndex = 0;
    webpage = require("webpage");
    page = null;
    getFilename = function() {
        return "rendermulti-" + piiIndex + ".png";
    };
    next = function(status, pii, file) {
        page.close();
        callbackPerpii(status, pii, file);
        // nextSt = Date.now();
        // console.log('nextSt: '+nextSt);
        return retrieve();
    };
    retrieve = function() {
        var pii;
        if (piis.length > 0) {
            pii = piis.shift();
            piiIndex++;
            page = webpage.create();
            page.viewportSize = {
                width: 1200,
                height: 600
            };
            page.settings.userAgent = "Phantom.js bot";
            url2visit="http://"+hostname+"/science/article/pii/" + pii;
            // console.log(url2visit);
            return page.open(url2visit, function(status) {
                var file;
                file = getFilename();
                if (status === "success") {
                    return window.setTimeout((function() {
                        //////////////////////////
                        // Uncomment below to validate same session across page views
                        // var sessID=page.evaluate(function(){
                      	// 	return SDM.si.sds;
                      	// });
                        // console.log(sessID);

                        getMetrics(page);
                        ///////////////////////////////
                        // Uncomment to render pages for visual inpsection
                        // page.render(file);
                        return next(status, pii, file);
                    }), 200);
                } else {
                    return next(status, pii, file);
                }
            });
        } else {
            return callbackFinal();
        }
    };
    return retrieve();
};

///////////////////////////////////////////////
// Handle Commandline input
arrayOfpiis = [];

if (system.args.length > 2) {
    // arrayOfpiis = Array.prototype.slice.call(system.args, 1);
    hostname = system.args[1];
    // console.log(hostname);
    system.args.forEach(function(arg,i){
      if (i>1){arrayOfpiis.push(arg);}
    });
    // console.log(arrayOfpiis);
} else {
    console.log("Usage: phantomjs render_multi_pii.js pii1 pii2 pii3...");
    // arrayOfpiis = ["www.google.com", "www.bbc.co.uk", "www.phantomjs.org"];
    arrayOfpiis = ["S0022314X03000155","S0045794904003025", "S0092867411001279"];
    hostname="cdc318-www.sciencedirect.com";

}

////////////////////////////////////////////
// Collect & report on page timing
function getMetrics(page) {
	var wpt=page.evaluate(function(){
		return window.performance.timing;
	});

	var ns=wpt.navigationStart;
	var ttfb=wpt.responseStart-ns;
	var sr=wpt.domContentLoadedEventEnd-ns;
	console.log('TTFB:'+ttfb+' startRender:'+sr);
}



////////////////////////////////////////////
// Execute the script
RenderpiisToFile(arrayOfpiis, (function(status, pii, file) {
    if (status !== "success") {
        return console.log("Unable to render '" + pii + "'");
    } //else {
    //     return console.log("Rendered '" + pii + "' at '" + file + "'");
    // }
}), function() {
    return phantom.exit();
});

