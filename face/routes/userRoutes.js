const express = require('express');
const userRouter = express.Router();

const{
    register,
    login
}=require('../controller/usercontroller')

userRouter.post('/reg',register)
userRouter.get('/log',login)

module.exports=userRouter
