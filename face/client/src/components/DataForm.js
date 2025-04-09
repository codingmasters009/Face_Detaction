import React, { useRef, useState } from "react";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

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
        }
    }

    return (
        <Box component="form" sx={{ flexGrow: 1 }} onSubmit={addInfo} style={styles.formContainer}>
            <Card sx={{ width: '100%', borderRadius: '12px', boxShadow: 3 }} style={styles.card}>
                <CardContent>
                    <Typography variant="h5" component="h2" style={styles.cardTitle}>Add User Info</Typography>
                    <Grid container spacing={2}>
                        <Grid item xs={8}>
                            <Box>
                                <TextField
                                    id="name"
                                    variant="outlined"
                                    fullWidth
                                    label="Name"
                                    onChange={(e) => setInfo({ ...info, name: e.target.value })}
                                    value={info.name}
                                    style={styles.textField}
                                />
                                <TextField
                                    id="address"
                                    variant="outlined"
                                    fullWidth
                                    label="Address"
                                    onChange={(e) => setInfo({ ...info, address: e.target.value })}
                                    value={info.address}
                                    style={styles.textField}
                                />
                                <TextField
                                    id="cnic"
                                    variant="outlined"
                                    fullWidth
                                    label="CNIC"
                                    onChange={(e) => setInfo({ ...info, cnic: e.target.value })}
                                    value={info.cnic}
                                    style={styles.textField}
                                />
                            </Box>
                        </Grid>
                        <Grid item xs={4}>
                            <div onClick={handleImage} style={styles.imageContainer}>
                                <img
                                    src={image || "./photo.jpg"}
                                    alt="Upload"
                                    style={styles.uploadImage}
                                />
                                <input
                                    type="file"
                                    ref={inputRef}
                                    style={{ display: 'none' }}
                                    onChange={handleImageChange}
                                />
                            </div>
                        </Grid>
                        <Grid item xs={12}>
                            <Button
                                type="submit"
                                variant="contained"
                                color="primary"
                                fullWidth
                                style={styles.submitButton}
                            >
                                Add Info
                            </Button>
                        </Grid>
                    </Grid>
                </CardContent>
            </Card>
        </Box>
    );
}

const styles = {
    formContainer: {
        display: 'flex',
        justifyContent: 'center',
        padding: '30px',
        backgroundColor: '#f7f7f7',
        minHeight: '70vh',
    },
    card: {
        padding: '20px',
        backgroundColor: '#ffffff',
        borderRadius: '15px',
        boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.1)',
        width: '80%',
        maxWidth: '900px',
    },
    cardTitle: {
        textAlign: 'center',
        marginBottom: '20px',
        color: '#333',
    },
    textField: {
        marginBottom: '15px',
        borderRadius: '8px',
        '& .MuiInputBase-root': {
            backgroundColor: '#f9f9f9',
        },
    },
    imageContainer: {
        cursor: 'pointer',
        textAlign: 'center',
        marginBottom: '15px',
        borderRadius: '10px',
        border: '2px dashed #007bff',
        padding: '10px',
        backgroundColor: '#f9f9f9',
    },
    uploadImage: {
        width: '100%',
        height: 'auto',
        borderRadius: '10px',
        objectFit: 'cover',
    },
    submitButton: {
        padding: '12px',
        fontSize: '16px',
        fontWeight: '600',
        backgroundColor: '#007bff',
        color: '#fff',
        borderRadius: '8px',
        '&:hover': {
            backgroundColor: '#0056b3',
        },
    },
};

export default DataForm;
