import React, { useRef, useState } from "react";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import uuid from 'uuid'

function DataForm() {
    state ={
        items:[
            {id: uuid(), name:'Abdullah', address:'Model Town', cnic:'32102'}
        ]
    }
    const inputRef = useRef(null);
    const [image, setImage] = useState(null);

    const handleImage = () => {
        inputRef.current.click();
    }

    const handleImageChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                setImage(e.target.result);
            };
            reader.readAsDataURL(file);
        }
    }

    return (
        <Box component="form" sx={{ flexGrow: 1 }}>
            <Grid container spacing={2}>
                <Grid item xs={8}>
                    <Box>
                        <TextField id="name" label="Name" variant="filled" fullWidth margin="normal" />
                        <TextField id="address" label="Address" variant="filled" fullWidth margin="normal" />
                        <TextField id="cnic" label="CNIC" variant="filled" fullWidth margin="normal" />
                    </Box>
                </Grid>
                <Grid item xs={4}>
                    <div onClick={handleImage} style={{ cursor: 'pointer', textAlign: 'center' }}>
                        <img src={image || "./photo.jpg"} alt="Upload" style={{ width: '100%', height: 'auto' }} />
                        <input type="file" ref={inputRef} style={{ display: 'none' }} onChange={handleImageChange} />
                    </div>
                </Grid>
            </Grid>
        </Box>
    );
}

export default DataForm;
