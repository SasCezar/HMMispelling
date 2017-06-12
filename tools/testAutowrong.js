// JavaScript source code
const autowrong = require('autowrong');
const options = {adjacent: 0.05, double: 0.00, order: 0.00}
var fs = require("fs");
var text = fs.readFileSync("./myText.txt").toString('utf-8');
var textByLine = text.split("\r\n");
console.log(textByLine)
var maxIndex = textByLine.length
console.log(maxIndex)
for(i = 0; i < maxIndex; i++){
	var perturb = textByLine[i].split("\t")
	console.log(perturb[0])
	console.log(perturb[1])
	fs.appendFileSync("./myTextWrite.txt", perturb[0] + "\t" + autowrong(perturb[1], options) + "\r\n") 
}
