import API from "./api";

export async function login(email, password) {
  const res = await API.post("/auth/login", {
    email,
    password,
  });
  return res.data;
}

export async function register(email, password) {
  const res = await API.post("/auth/register", {
    email,
    password,
  });
  return res.data;
}

