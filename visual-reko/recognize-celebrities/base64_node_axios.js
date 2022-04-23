'use strict';

const fs = require('fs');
const axios = require("axios");

let buff = fs.readFileSync('RapidAPI/tutorial/data/image.jpg');
let base64data = buff.toString('base64');


const options = {
  method: 'POST',
  url: 'https://vrt-visual-recognition-tool.p.rapidapi.com/celebrities',
  headers: {
    'content-type': 'application/json',
    'X-RapidAPI-Host': 'vrt-visual-recognition-tool.p.rapidapi.com',
    'X-RapidAPI-Key': 'YOUR KEY'
  },
  data: `{"ImageUrl":"data:image/jpg;base64,${base64data}"}`
};

axios.request(options).then(function (response) {
	console.log(response.data);
}).catch(function (error) {
	console.error(error);
});