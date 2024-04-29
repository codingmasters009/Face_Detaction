const express = require('express')

const forRouter =express.Router();

const{
    newdata
}= require('../controller/infoforrmcontroller')

forRouter.post('/data', newdata);

module.exports = forRouter