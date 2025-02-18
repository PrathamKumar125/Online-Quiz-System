import api from './api';

export const auth = {
    login: async (credentials) => {
        const formData = new URLSearchParams();
        formData.append('username', credentials.username);
        formData.append('password', credentials.password);
        
        const response = await api.post('/api/token', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
        }
        return response;
    },
    logout: () => {
        localStorage.removeItem('token');
    },
    getCurrentUser: async () => {
        const response = await api.get('/users/me');
        return response.data;
    }
};

export default auth;