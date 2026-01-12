import { useState } from "react";
import { uploadBill} from "../api/expenses";

export default function OcrUpload() {
    const [file,setFile] = useState(null);
    const[result,setResult] = useState("");

    const handleUpload = async (e) => {
        const res = await uploadBill(file);
        setResult(res.data);
    };

    return (
        <div>
            <div>
                <h2>Upload Bill</h2>

                <input type="file" onChange={(e)=> setFile(e.target.files[0])} />
                <button onClick={handleUpload} className="">Extract</button>
                {result && (
                    <div>
                        <p>Amount: Rs. {result.amount}</p>
                        <p>Category: {result.category}</p>
                        <p>Date: {result.date}</p>
                    </div>
                )}
            </div>
        </div>
    );
}