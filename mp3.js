const express = require('express');
const axios = require('axios');
const ytdl = require('ytdl-core');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

const SOUND_CLOUD_API_KEY = 'YOUR_SOUNDCLOUD_CLIENT_ID';

app.get('/search', async (req, res) => {
    const query = req.query.q;
    if (!query) {
        return res.status(400).send('Search query is required');
    }

    try {
        const response = await axios.get(
            `https://api-v2.soundcloud.com/search/tracks?q=${encodeURIComponent(query)}&client_id=${SOUND_CLOUD_API_KEY}`
        );

        if (response.data.collection.length === 0) {
            return res.status(404).send('No results found');
        }

        const track = response.data.collection[0]; 
        res.json({
            title: track.title,
            url: track.permalink_url,
        });
    } catch (error) {
        console.error('Error in search:', error);
        res.status(500).send('Error searching for track');
    }
});

app.get('/download', async (req, res) => {
    const trackUrl = req.query.url;
    res.send('Download functionality is not implemented in this example.');
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
