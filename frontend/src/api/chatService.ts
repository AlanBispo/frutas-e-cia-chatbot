import axios from 'axios';
export interface Message {
  text: string;
  sender: 'user' | 'bot';
}

export interface OffersResponse {
  texto: string;
  items: any[];
}

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export const sendMessageToBot = async (message: string): Promise<string> => {
  const response = await api.post('/chat/', { message });
  return response.data.reply;
};

export const getDailyOffers = async (): Promise<OffersResponse> => {
  const response = await api.get('/ofertas/hoje');
  return response.data;
};