import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

export default {
  async getQuizInfo() {
    const response = await axios.get(`${API_URL}/quiz-info`);
    return response.data;
  },
  async getAllQuestions() {
    const response = await axios.get(`${API_URL}/questions/all`);
    return response.data;
  },
  async getQuestion(position) {
    const response = await axios.get(`${API_URL}/questions?position=${position}`);
    return response.data;
  },
  async getQuestionById(id) {
    const token = localStorage.getItem('token');
    const config = token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    const response = await axios.get(`${API_URL}/questions/${id}`, config);
    return response.data;
  },
  async submitParticipation(playerName, answers, score) {
    const response = await axios.post(`${API_URL}/participations`, {
      playerName,
      answers,
      score,
    });
    return response.data;
  },
  async generateQuestions(payload) {
    const token = localStorage.getItem('token')
    const config = token ? { headers: { Authorization: `Bearer ${token}` } } : {}
    const response = await axios.post(`${API_URL}/questions/generate`, payload, config)
    return response.data
  },
  async insertQuestion(payload) {
    const token = localStorage.getItem('token')
    const config = token ? { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } } : { headers: { 'Content-Type': 'application/json' } }
    const response = await axios.post(`${API_URL}/questions`, payload, config)
    return response.data
  },
  async updateQuestion(id, payload, imageFile) {
    const token = localStorage.getItem('token');
    const config = token ? { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } } : { headers: { 'Content-Type': 'application/json' } };
    const response = await axios.put(`${API_URL}/questions/${id}`, payload, config);
    return response.data;
  },
  async loginAdmin(password) {
    const response = await axios.post(`${API_URL}/login`, { password });
    return response.data;
  },

  async getLogs(token) {
    const config = token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    const response = await axios.get(`${API_URL}/logs`, config);
    return response.data;
  },

  async deleteQuestion(id) {
    const token = localStorage.getItem('token');
    const config = token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    const response = await axios.delete(`${API_URL}/questions/${id}`, config);
    return response.data;
  },
};
