import axios from 'axios';
import * as dotenv from 'dotenv';

dotenv.config();

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';

if (!GEMINI_API_KEY) {
    console.error('GEMINI_API_KEY not found in environment variables. Please set it in your .env file.');
    process.exit(1);
}

async function getGeminiResponse(prompt: string): Promise<string> {
    try {
        const payload = {
            contents: [{ parts: [{ text: prompt }] }]
        };
        const params = { key: GEMINI_API_KEY };
        const response = await axios.post(GEMINI_API_URL, payload, { params });
        return response.data?.candidates?.[0]?.content?.parts?.[0]?.text || 'No response from Gemini API.';
    } catch (error: any) {
        console.error('Error accessing Gemini API:', error?.response?.data || error.message);
        return 'Sorry, I could not process your request.';
    }
}

async function main() {
    const prompt = process.argv.slice(2).join(' ');
    if (!prompt) {
        console.error('Please provide a prompt as a command-line argument.');
        process.exit(1);
    }
    const response = await getGeminiResponse(prompt);
    console.log('Gemini response:', response);
}

main();
