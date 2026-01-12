import { useState} from "react";
import {login} from "../api/auth";
import {useNavigate} from "react-router-dom";

export default function Login(){
    const [email,setEmail] = useState("");
    const [password,setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try{
            const res = await login({email, password});
            localStorage.setItem("token", res.data.access_token);
            navigate("/dashboard");
        }catch(err){
            alert("Invalid credentials");
        }
    };

    return(
        <div className="">
            <form 
                onSubmit={handleSubmit}
                className="">
                    <h2>Login</h2>
                    <input 
                        type="email" placeholder="Email" className="" onChange={(e)=> setEmail(e.target.value)} required/>
                    <input
                        type="password" placeholder="Password" className="" onChange={(e) => setPassword(e.target.value) }required/>
                    <button className="">Login</button>
                </form>
        </div>
    );
}