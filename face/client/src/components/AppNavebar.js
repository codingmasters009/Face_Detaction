import React from 'react';
import { BrowserRouter, Route, Routes, Link } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import DataForm from './DataForm';
import IdentifyCriminal from './IdentifyCriminal';

function AppNavbar() {
    return (
        <BrowserRouter>
            <Box sx={{ flexGrow: 1 }}>
                <AppBar position="static">
                    <Toolbar variant="dense">
                        <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
                            <MenuIcon />
                        </IconButton>
                        <Typography variant="h6" sx={{ m: 2 }} color="inherit" component="div">
                            <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                                Add Criminal Info
                            </Link>
                        </Typography>
                        <Typography variant="h6" sx={{ m: 2 }} color="inherit" component="div">
                            <Link to="/identify" style={{ textDecoration: 'none', color: 'inherit' }}>
                                Identify Criminal
                            </Link>
                        </Typography>
                    </Toolbar>
                </AppBar>
                <Routes>
                    <Route exact path="/" element={<DataForm />} />
                    <Route path="/identify" element={<IdentifyCriminal />} />
                </Routes>
            </Box>
        </BrowserRouter>
    );
}

export default AppNavbar;
