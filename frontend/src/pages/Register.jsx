import {useState} from 'react';
import {register} from '../api/auth';
import {useNavigate} from 'react-router-dom';

export default function Register(){
    const [email,setEmail] = useState("");
    const [password,setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();  // Prevent default form submission behavior/ no refresh
        try{
            await register({email,password})
            navigate("/login");
        }catch{
            alert("Registration failed");
        }

    };
    return(
        <div className='' >
            <form onSubmit={handleSubmit} className=''>
                <h2>Register</h2>
                <input type="email"
                    placeholder='Email' onChange = {(e) => setEmail(e.target.value)}  required/> 
                <input type="password"
                    placeholder='Password' onChange = {(e) => setPassword(e.target.value)}  required/> 
                <button>Register</button>
            </form>
        </div>
    );
}