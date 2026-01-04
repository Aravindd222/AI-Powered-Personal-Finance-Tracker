import axios from "axios";

const API = "https://127.0.0.1:8000";

export const login = (data) =>{
    axios.post(`${API}/auth/login`,data);
}

export const register = (data) => {
    axios.post(`${API}/auth/register`,data);
}

