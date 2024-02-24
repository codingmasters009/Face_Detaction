const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const regRouter = require('./routes/userRoutes')
const app = express();

app.use(bodyParser.json());

// db config
const db = require('./config/keys').mongoURI;

//Routes
app.use('/api/reg',regRouter);

// db connection
mongoose
    .connect(db)
    .then(() => console.log('DB Connected....'))
    .catch(err =>console.log(err));

    const port = process.env.PORT || 3000;
    app.listen(port, () => console.log('Server is Running on Port 3000'));