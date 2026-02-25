import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export const sendMessageToBot = async (message: string) => {
  const response = await api.post('/chat/', { message });
  return response.data.reply;
};