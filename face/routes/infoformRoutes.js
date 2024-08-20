const express = require('express')

const forRouter =express.Router();

const{
    newdata,
    getDataByImage
}= require('../controller/infoforrmcontroller')

forRouter.post('/data', newdata);
forRouter.get('/user/:img', getDataByImage); 

module.exports = forRouter

