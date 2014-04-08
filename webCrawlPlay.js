var http = require("http");
var cheerio = require("cheerio");
var fs = require('fs');
// Utility function that downloads a URL and invokes
// callback with the data.
function download(url, callback) {
  http.get(url, function(res) {
    var data = "";
    res.on('data', function (chunk) {
      data += chunk;
    });
    res.on("end", function() {
      callback(data);
    });
  }).on("error", function() {
    callback(null);
  });
}

setInterval(function(){
	download('http://news.google.com/news/section?pz=1&cf=all&ned=us&topic=m&siidp=3e8f7860246ea3de1d3708afb6375bedf8c5&ict=ln', function(data){
	  if(data){
	    var titles = [];
	    var $ = cheerio.load(data);
	    $(".esc-lead-article-title .titletext").each(function(i, e) {
	      titles.push(e.children[0].data.toLowerCase());
	    });
	    
	    var wordsInTitles = {};
	    titles.forEach(function(title){
	      title.split(" ").forEach(function(word){
	        if(wordsInTitles[word]){
	          wordsInTitles[word]++;
	        }else{
	          wordsInTitles[word] = 1;
	        }
	      });
	    });

	    var tuples = [];
	    obj = wordsInTitles;
	    for (var key in obj) tuples.push([key, obj[key]]);

	    tuples.sort(function(a, b) {
	        a = a[1];
	        b = b[1];

	        return a < b ? -1 : (a > b ? 1 : 0);
	    });

	    //generate string to save
	    var d = new Date(); // Today's date 

	    var dstr = (d.getMonth() + 1) + '/' + ('00' + d.getDate()).substr(-2);

	    var stringToSave = dstr + " " + (new Date()).getHours() + "h-" + (new Date).getMinutes() + "m " + ": {";

	    for (var i = tuples.length-1; i >= 0; i--) {
	        var key = tuples[i][0];
	        var value = tuples[i][1];
	        console.log(key + " " + value);

	        // do something with key and value
	        if(i != 0){
	          stringToSave += key +":" + value + ',';
	        }else{
	          stringToSave += key +":" + value + '}\n';
	        }
	    }

	    fs.appendFile("C:\\Users\\tnattestad\\Google Drive\\data science\\cdc\\DataScience2014CDC\\testFile.txt", stringToSave, function(err) {
	      if(err) {
	        console.log(err);
	      } else {
	        console.log("The file was saved!");
	      }
	    });
	    console.log("done");  
	  }
	});
}, 1000 * 60 * 10);
