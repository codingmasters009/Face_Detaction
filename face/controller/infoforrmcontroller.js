const Form = require('../models/infoformmodels');


const newdata = async (req, res) => {
    const {name, adress, cnic, img } = req.body;

    try {
        

        // If username is unique, create a new user with hashed password
        const newUser = await Form.create({name, adress, cnic, img });

        res.status(201).json({ msg: 'Data Enter successfully', user: newUser });
    } catch (error) {
        res.status(500).json({ error: 'Internal Server Error' });
    }
};
module.exports= {newdata}