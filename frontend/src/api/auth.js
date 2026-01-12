import axios from "axios";

const API = "http://localhost:8000";

export const login = (data) =>{
    return axios.post(`${API}/auth/login`,data);
}

export const register = (data) => {
    return axios.post(`${API}/auth/register`,data);
}

