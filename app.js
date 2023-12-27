const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();

app.use(cors());
app.use(bodyParser.json({ limit: '10mb' }));
app.use(bodyParser.urlencoded({ limit: '10mb', extended: true }));

app.get('/', (req, res) => {
    res.send('Servidor Node.js funcionando correctamente');
});

app.post('/reconocimiento_facial', (req, res) => {
    console.log('Recibida solicitud POST /reconocimiento_facial');
    console.log('Llamando al script de Python...');

    const imagenB64 = req.body.imagen.split(',')[1];
    const imagenBuffer = Buffer.from(imagenB64, 'base64');
    
    fs.writeFileSync('debugImage.png', imagenBuffer);

    const tempFilePath = path.join(__dirname, 'tempImage.png');
    fs.writeFileSync(tempFilePath, imagenBuffer);

    const pythonProcess = spawn('python', ['Final_Proj_FR_ID.py', tempFilePath]);

    let errorMessage = '';

    pythonProcess.stdout.on('data', (data) => {
        console.log('Python script output:', data.toString());
        res.send(data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error en el script de Python: ${data}`);
        errorMessage += data.toString();
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python script terminado con código ${code}`);
        fs.unlinkSync(tempFilePath); // Eliminar el archivo temporal
        if (errorMessage) {
            res.status(500).send("Error en el script de Python: " + errorMessage);
        }
    });
});

app.listen(5000, () => {
    console.log('Servidor corriendo en http://localhost:5000');
});
