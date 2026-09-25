const express = require('express');
const cors = require('cors');
const axios = require('axios')
const app = express();

app.use(cors());
app.use(express.json());

const PORT = 5000;
const AI_SERVICE_URL = "http://localhost:8000";


app.get("/api/hello", async (req,res) =>{
   try {
    const response = await axios.get(`${AI_SERVICE_URL}/hello`);

    res.json({
        message: response.data.message,
    });
   } catch (error) {
    console.log("AI Service Error",error.message);
    
    res.json({
        message: "Failed To communicate With AI service",
    })
   }
});

app.listen(PORT,()=>{
    console.log(`node.js server running on https://localhost:${PORT}`);
});

