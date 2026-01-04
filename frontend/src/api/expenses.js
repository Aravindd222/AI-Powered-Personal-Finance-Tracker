import axios from "axios";

const API = "https://127.0.0.1:8000";

const authHeader = () => ({
    headers:{
        Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
});

export const addManualExpense = (data) => {
    axios.post(`${API}/expenses/manual`,data,authHeader());
}

export const uploadBill = (file) => {
    const formData = new FormData();
    formData.append("file",file)

    return axios.post(`${API}/expenses/ocr`,formData,authHeader());

};

export const getMonthlySummary = () => {
    axios.get(`${API}/expenses/monthly-summary`,authHeader());
}
