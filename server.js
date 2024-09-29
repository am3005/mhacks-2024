import express from 'express';
import bodyParser from 'body-parser';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import axios from 'axios';

// Manually define __dirname for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static('public'));
app.use(bodyParser.json({ limit: '10mb' }));

// Store results globally (or you can use a database)
let results = [];

// Handle image uploads
app.post('/upload', async (req, res) => {
    const images = req.body.images;

    if (!images || !Array.isArray(images)) {
        return res.status(400).json({ error: 'No images provided' });
    }

    const uploadDir = path.join(__dirname, 'public', 'uploads');
    if (!fs.existsSync(uploadDir)) {
        fs.mkdirSync(uploadDir);
    }

    results = []; // Clear previous results
    for (const [index, image] of images.entries()) {
        const base64Data = image.replace(/^data:image\/png;base64,/, '');
        const filePath = path.join(uploadDir, `image_${index}.png`);
        fs.writeFileSync(filePath, base64Data, 'base64');

        try {
            const imageData = fs.readFileSync(filePath, { encoding: 'base64' });

            const response = await axios({
                method: 'POST',
                url: 'https://detect.roboflow.com/asl-project-wcka3/3', // Adjust the model path
                params: {
                    api_key: 'IcGWxHMLBlniIr6s24b2' // Replace with your actual API key
                },
                data: imageData,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });

            results.push(response.data);
        } catch (error) {
            console.error('Error processing image:', error.message);
            results.push({ error: 'Error processing image' });
        }
    }

    // Return success response and provide a link to get results
    res.json({ message: 'Images processed successfully', results: results.length });
});

// New endpoint to get results in JSON format
app.get('/get-results', (req, res) => {
    if (results.length === 0) {
        return res.status(404).json({ error: 'No results available' });
    }
    res.json(results);
});

// Serve the results HTML file
app.get('/results', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'results.html'), (err) => {
        if (err) {
            res.status(err.status).end();
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
