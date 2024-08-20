import React, { useRef, useState } from "react";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';

function DataForm() {
    const [info, setInfo] = useState({
        img: null, name: "", address: "", cnic: ""
    });
    const inputRef = useRef(null);
    const [image, setImage] = useState(null);

    const handleImage = () => {
        inputRef.current.click();
    }

    const handleImageChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            const imageUrl = URL.createObjectURL(file);
            setImage(imageUrl);
            setInfo({ ...info, img: file });
        }
    }

    const addInfo = async (e) => {
        e.preventDefault();
        const { name, address, cnic, img } = info;

        if (!img) {
            window.alert("Please upload an image.");
            return;
        }

        const formData = new FormData();
        formData.append('image', img);
        formData.append('name', name);
        formData.append('address', address);
        formData.append('cnic', cnic);

        try {
            const res = await fetch("http://localhost:3001/api/data", {
                method: "POST",
                body: formData
            });

            // Log the response for debugging
            console.log("Response Status:", res.status);
            console.log("Response Body:", await res.text());

            if (res.ok) {
                window.alert("Info Added Successfully");
                const data = await res.json();
                console.log("Added Success:", data);
                setInfo({ img: null, name: "", address: "", cnic: "" });
                setImage(null);
            } else {
                window.alert("Invalid Information");
            }
        } catch (error) {
            console.error('Error:', error);
          //  window.alert("Error submitting form");
        }
    }

    return (
        <Box component="form" sx={{ flexGrow: 1 }} onSubmit={addInfo}>
            <Grid container spacing={2}>
                <Grid item xs={8}>
                    <Box>
                        <TextField
                            id='name'
                            variant="standard"
                            fullWidth
                            label='Name'
                            onChange={(e) => setInfo({ ...info, name: e.target.value })}
                            value={info.name}
                        />
                        <TextField
                            id='address'
                            variant="standard"
                            fullWidth
                            label='Address'
                            onChange={(e) => setInfo({ ...info, address: e.target.value })}
                            value={info.address}
                        />
                        <TextField
                            id='cnic'
                            variant="standard"
                            fullWidth
                            label='CNIC'
                            onChange={(e) => setInfo({ ...info, cnic: e.target.value })}
                            value={info.cnic}
                        />
                    </Box>
                </Grid>
                <Grid item xs={4}>
                    <div onClick={handleImage} style={{ cursor: 'pointer', textAlign: 'center' }}>
                        <img src={image || "./photo.jpg"} alt="Upload" style={{ width: '100%', height: 'auto' }} />
                        <input
                            type="file"
                            ref={inputRef}
                            style={{ display: 'none' }}
                            onChange={handleImageChange}
                        />
                    </div>
                </Grid>
                <Grid item xs={12}>
                    <Button type="submit" variant="contained" color="primary" fullWidth>
                        Add Info
                    </Button>
                </Grid>
            </Grid>
        </Box>
    );
}

export default DataForm;
