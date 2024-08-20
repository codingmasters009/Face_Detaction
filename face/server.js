const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const userRouter = require('./routes/userRoutes');
const dataRouter = require('./routes/infoformRoutes');
const app = express();
const axios = require('axios'); // Import axios
// Middleware
app.use(bodyParser.json());
app.use(cors());

// DB config
const db = require('./config/keys').mongoURI;

// Routes
app.use('/api', userRouter);
app.use('/api', dataRouter);






// DB connection
mongoose
    .connect(db)
    .then(() => console.log('DB Connected....'))
    .catch(err => console.log(err));

// Server listening
const port = process.env.PORT || 3001;
app.listen(port, () => console.log(`Server is Running on Port ${port}`));
