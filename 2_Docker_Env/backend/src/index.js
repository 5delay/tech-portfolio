const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 4500;

app.use(express.json());
app.use(cors({
    origin: [
        'http://114.71.51.34:3800',
        'http://localhost:3800'
    ]
}));

app.get('/', (req, res) => {
    res.json({
        status: 'ok',
        message: 'Backend server is running!'
    });
});

app.get('/api', (req, res) => {
    res.status(200).json({
        status: 'healthy'
    });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
    console.log(`server running on ${PORT}`);
  });
  