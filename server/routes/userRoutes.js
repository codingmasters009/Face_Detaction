const express = require('express');
const regRouter = express.Router();

const{
    register,
    login
}=require('../controller/userController')

regRouter.post('/',register)


module.exports=regRouter
