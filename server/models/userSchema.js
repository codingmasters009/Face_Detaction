const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const regSchema = new Schema({

    username:{
        type:String,
        require:true,
        unique:true
    },
    name:{
        type:String,
        require:true
    },
    password:{
        type:String,
        require:true
    }
});
module.exports=mongoose.model('reg',regSchema)
