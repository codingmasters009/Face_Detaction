const path = require('path');
const multer = require('multer');
const Form = require('../models/infoformmodels');

// Set up storage for uploaded images
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadPath = path.join(__dirname, '../client/src/images');
        console.log('Upload path:', uploadPath);
        cb(null, uploadPath);
    },
    filename: (req, file, cb) => {
        const filename = Date.now() + path.extname(file.originalname);
        console.log('Generated filename:', filename);
        cb(null, filename);
    }
});

const upload = multer({ 
    storage: storage,
    limits: { fileSize: 1024 * 1024 * 5 } // Limit file size to 5MB
}).single('image');

const newdata = async (req, res) => {
    upload(req, res, async (err) => {
        if (err) {
            console.error('Multer error:', err);
            return res.status(500).json({ error: 'Image upload failed', details: err.message });
        }

        console.log('File uploaded:', req.file); // Log the uploaded file

        const { name, address, cnic } = req.body;
        const img = req.file.filename; // Use the filename directly from req.file

        try {
            const newUser = await Form.create({ name, address, cnic, img });
            console.log('New user created:', newUser);
            res.status(201).json({ msg: 'Data entered successfully', user: newUser });
        } catch (error) {
            console.error('Database error:', error);
            res.status(500).json({ error: 'Internal Server Error', details: error.message });
        }
    });
};
const getDataByImage = async (req, res) => {  
    const { img } = req.params; // Assuming img is passed as a route parameter  

    try {  
        const user = await Form.findOne({ img });  
        if (!user) {  
            return res.status(404).json({ error: 'User not found' });  
        }  
        res.status(200).json(user);  
    } catch (error) {  
        console.error('Database error:', error);  
        res.status(500).json({ error: 'Internal Server Error', details: error.message });  
    }  
};  

module.exports = { newdata, getDataByImage };  


