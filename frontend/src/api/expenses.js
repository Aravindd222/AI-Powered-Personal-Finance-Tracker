import axios from "axios";

const API = "http://localhost:8000";

const authHeader = () => ({
    headers:{
        Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
});

export const addManualExpense = (data) => {
    return axios.post(`${API}/expenses/manual`,data,authHeader());
};

export const uploadBill = (file) => {
    const formData = new FormData();
    formData.append("file",file)

    return axios.post(`${API}/expenses/ocr`,formData,authHeader());

};

export const getMonthlySummary = () => {
    return axios.get(`${API}/expenses/monthly-summary`,authHeader());
};
