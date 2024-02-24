const User = require('../models/userSchema')


const register = async (req, res) => {
    const { username, name, password } = req.body;

    try {
        // Check if the username already exists
        const existingUser = await User.findOne({ username });

        if (existingUser) {
            return res.status(400).json({ error: 'Username already exists' });
        }

        // Hash the password
        const hashedPassword = await bcrypt.hash(password, 10);

        // If username is unique, create a new user with hashed password
        const newUser = await User.create({ username, name, password: hashedPassword });

        res.status(201).json({ msg: 'User registered successfully', user: newUser });
    } catch (error) {
        res.status(500).json({ error: 'Internal Server Error' });
    }
};


const login = async (req, res) => {
    const { username, password } = req.body;

    try {
        // Check if the user exists in the database
        const user = await reg.findOne({ username });

        if (!user) {
            return res.status(400).json({ error: 'Invalid credentials' });
        }

        // Compare the provided password with the hashed password stored in the database
        const isPasswordValid = await bcrypt.compare(password, user.password);

        if (!isPasswordValid) {
            return res.status(400).json({ error: 'Invalid credentials' });
        }

        // Generate a JWT token for authentication
        const token = jwt.sign({ userId: user._id }, 'your_secret_key', { expiresIn: '1h' });

        res.status(200).json({ token });
    } catch (error) {
        res.status(500).json({ error: 'Internal Server Error' });
    }
};


module.exports={register,login};