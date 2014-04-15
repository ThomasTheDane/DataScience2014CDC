var http = require("http");
var cheerio = require("cheerio");
var fs = require('fs');
var natural = require('natural'),
TfIdf = natural.TfIdf,
tfidf = new TfIdf();

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

function getWordsAndRankings(){
 download('http://news.google.com/news/section?topic=m', function(data){
   if(data){
     var stringToSave = "";
     var documentCount = 0;
     var wordsAndRankings = {};

     var $ = cheerio.load(data);
     $(".esc-lead-article-title .titletext").each(function(i, e) {
       var title = e.children[0].data.toLowerCase();
       for(var i = 0; i < 20; i++){
         title = title.replace("&#39;", "");
         title = title.replace("&quot;", '');
       }
       if(title != undefined){
       //   tfidf.addDocument(title);
       //   documentCount += 1;
     	stringToSave += title + " ";
       }
     });
     $(".esc-lead-snippet-wrapper").each(function(i,e){
       // console.log(e.children[0].data.toLowerCase());
       var subheadding = e.children[0].data.toLowerCase();
       // tfidf.addDocument(subheadding);
       // documentCount += 1;
       // stringToSave += e.children[0].data.toLowerCase() + " ";
     });
     console.log(stringToSave);
     tfidf.addDocument(stringToSave);
     tfidf.listTerms(0).forEach(function(item) {
       // console.log(item.term + ': ' + item.tfidf);
     });
   }
 });
}

function saveWordDumpFromGoogleNewsHealth(){
 download('http://news.google.com/news/section?topic=m', function(data){
   if(data){
     //generate string to save
     var d = new Date(); // Today's date 

     var dstr = (d.getMonth() + 1) + '-' + ('00' + d.getDate()).substr(-2);

     var stringToSave = (new Date()).getHours() + "h-" + (new Date).getMinutes() + "m " + ": {";

     var $ = cheerio.load(data);
     $(".esc-lead-article-title .titletext").each(function(i, e) {
       // console.log(e.children[0].data.toLowerCase());
       stringToSave += e.children[0].data.toLowerCase() + " ";
     });
     $(".esc-lead-snippet-wrapper").each(function(i,e){
       // console.log(e.children[0].data.toLowerCase());
       stringToSave += e.children[0].data.toLowerCase() + " ";
     });

     stringToSave += "}\n";
     //save the file
     fs.appendFile(__dirname + "\\wordDump" + dstr + ".txt", stringToSave, function(err) {
       if(err) {
         console.log(err);
       } else {
         console.log("The file was saved!");
       }
     });
     console.log("done");  
   }
 });
}

function saveTitleWordRankings(){
download('http://news.google.com/news/section?topic=m', function(data){
 if(data){
   var titles = [];
   var $ = cheerio.load(data);
   $(".esc-lead-article-title .titletext").each(function(i, e) {
       console.log(e.children[0].data.toLowerCase());
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

   var dstr = (d.getMonth() + 1) + '-' + ('00' + d.getDate()).substr(-2);

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

   fs.appendFile(__dirname + "\\wordDump" + dstr + ".txt", stringToSave, function(err) {
     if(err) {
       console.log(err);
     } else {
       console.log("The file was saved!");
     }
   });
   console.log("done");  
 }
});
}
//getWordsAndRankings();
saveTitleWordRankings();
// setInterval(, 1000 * 60 * 1);