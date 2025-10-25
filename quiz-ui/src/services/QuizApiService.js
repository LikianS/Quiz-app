import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

export default {
  async getQuizInfo() {
    const response = await axios.get(`${API_URL}/quiz-info`);
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
  async updateQuestion(id, payload, imageFile) {
    const token = localStorage.getItem('token');
    const config = token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    if (imageFile) {
      const formData = new FormData();
      formData.append('image', imageFile);
      formData.append('data', JSON.stringify(payload));
      const response = await axios.put(`${API_URL}/questions/${id}`, formData, config);
      return response.data;
    } else {
      const response = await axios.put(`${API_URL}/questions/${id}`, payload, config);
      return response.data;
    }
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
