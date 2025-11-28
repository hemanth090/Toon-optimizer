const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// API Service for backend communication
class ApiService {
    async get(endpoint) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }

    async post(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }
}

const api = new ApiService();

// API Methods
export const getStatus = () => api.get('/api/status');

export const getHealth = () => api.get('/api/health');

export const convertJsonToToon = (jsonInput, indent = 2, delimiter = ',') =>
    api.post('/api/convert/json-to-toon', {
        json_input: jsonInput,
        indent,
        delimiter,
    });

export const convertToonToJson = (toonInput) =>
    api.post('/api/convert/toon-to-json', {
        toon_input: toonInput,
    });

export const queryData = (dataText, question, dataFormat) =>
    api.post('/api/query', {
        data_text: dataText,
        question,
        data_format: dataFormat,
    });

export const countTokens = (text) =>
    api.post('/api/count', { text });

export default api;
