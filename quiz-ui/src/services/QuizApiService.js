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

  async submitParticipation(playerName, answers, score) {
    const response = await axios.post(`${API_URL}/participations`, {
      playerName,
      answers,
      score,
    });
    return response.data;
  },
};
