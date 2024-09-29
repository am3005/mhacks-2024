import express from 'express';
import bodyParser from 'body-parser';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import axios from 'axios';
import { spawn } from 'child_process';  // Import child_process to run the Python script

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
    let uniqueClasses = []; // To store class names for prediction

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

            const apiResult = response.data;
            results.push(apiResult);

            // Extract classes and add to uniqueClasses array
            const predictions = apiResult.predictions || [];
            predictions.forEach(prediction => {
                if (prediction.class) {
                    uniqueClasses.push(prediction.class.trim()); // Add class to the array, including duplicates
                }
            });

        } catch (error) {
            console.error('Error processing image:', error.message);
            results.push({ error: 'Error processing image' });
        }
    }

    // Combine unique classes into a single string without separators
    const combinedClassString = uniqueClasses.join('').toUpperCase(); // Join without spaces or commas

    // Call the Python script for prediction using the combined class string
    const pythonProcess = spawn('C:\\Python312\\python.exe', ['LSTMmain.py', '--mode', 'predict', '--input_seq', combinedClassString]);

    let pythonResult = '';

    // Capture the output from the Python script
    pythonProcess.stdout.on('data', (data) => {
        pythonResult += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data.toString()}`);
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`Python script exited with code ${code}`);
            results.push({ error: `Python script failed with exit code ${code}` });
        } else {
            results.push({ prediction: pythonResult.trim() }); // Trim the result for cleaner output
        }

        // Return success response and provide a link to get results
        res.json({ message: 'Images processed successfully', results: results.length });
    });
});

// New endpoint to get results in JSON format
app.get('/get-results', (req, res) => {
    if (results.length === 0) {
        return res.status(404).json({ error: 'No results available' });
    }
    res.json(results);
});

// New endpoint to run prediction using combined classes
app.post('/run-predict', (req, res) => {
    const inputSeq = req.body.input_seq.toUpperCase();

    if (!inputSeq) {
        return res.status(400).json({ error: 'No input sequence provided' });
    }

    // Call the Python script for prediction using the input sequence
    const pythonProcess = spawn('C:\\Python312\\python.exe', ['LSTMmain.py', '--mode', 'predict', '--input_seq', inputSeq]);

    let pythonResult = '';

    // Capture the output from the Python script
    pythonProcess.stdout.on('data', (data) => {
        pythonResult += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data.toString()}`);
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`Python script exited with code ${code}`);
            return res.status(500).json({ error: `Python script failed with exit code ${code}` });
        }
        
        // Return the predicted output
        res.json({ predicted_output: pythonResult.trim() }); // Trim the result for cleaner output
    });
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
