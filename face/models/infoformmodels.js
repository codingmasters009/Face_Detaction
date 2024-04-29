const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const formSchema = new Schema ({
    name:{
        type:String,
        require:true
    },
    adress:{
        type:String,
        require:true
    },
    cnic:{
        type:String,
        require:true
    },
    img:{
        type:String,
    }
});

module.exports=mongoose.model('Form',formSchema)