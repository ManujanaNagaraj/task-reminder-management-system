const BASE_URL = 'http://127.0.0.1:8000/api';

const auth = {
    getToken: () => localStorage.getItem('token'),
    setToken: (token) => localStorage.setItem('token', token),
    removeToken: () => localStorage.removeItem('token'),
    isAuthenticated: () => !!localStorage.getItem('token'),

    login: async (username, password) => {
        try {
            const response = await fetch(`${BASE_URL}/login/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            if (response.ok) {
                auth.setToken(data.token);
                return { success: true };
            }
            return { success: false, error: data.non_field_errors?.[0] || 'Login failed' };
        } catch (error) {
            return { success: false, error: 'Network error occurred' };
        }
    },

    register: async (username, password, email, phone) => {
        try {
            const response = await fetch(`${BASE_URL}/register/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password, email, phone })
            });
            const data = await response.json();
            if (response.ok) {
                // Automatically login after successful registration
                return await auth.login(username, password);
            }
            return {
                success: false,
                error: data.username?.[0] || data.email?.[0] || data.password?.[0] || data.non_field_errors?.[0] || 'Registration failed'
            };
        } catch (error) {
            return { success: false, error: 'Network error occurred' };
        }
    },

    logout: () => {
        auth.removeToken();
        window.location.href = '/login.html';
    }
};

const api = {
    get: async (endpoint) => {
        const token = auth.getToken();
        if (!token) return null;

        try {
            const response = await fetch(`${BASE_URL}${endpoint}`, {
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            if (response.status === 401) {
                auth.logout();
                return null;
            }
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },

    getTasks: () => api.get('/tasks/'),
    getCalendarTasks: () => api.get('/tasks/calendar/')
};

// UI Helpers
function formatDate(dateString) {
    const options = { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

function checkAuthRedirect() {
    const isAuth = auth.isAuthenticated();
    const path = window.location.pathname;

    // Normalize path to handle local running (e.g. /login.html vs /frontend/login.html)
    const isLoginPage = path.endsWith('login.html');
    const isDashboard = path.endsWith('dashboard.html');

    if (!isAuth && isDashboard) {
        window.location.href = 'login.html';
    } else if (isAuth && isLoginPage) {
        window.location.href = 'dashboard.html';
    }
}
