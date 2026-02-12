import { useState } from "react";
import { addManualExpense } from "../api/expenses";

export default function AddExpense() {
    const [amount,setAmount] = useState("");
    const[category,setCategory] = useState("");
    const [date,setDate] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        await addManualExpense({ amount, category, date });
        alert("Expense added successfully!");
};


    return(
        <div>
            <form onSubmit={handleSubmit}
                className="">
                <h2>Add Expense</h2>
                <input value={amount} type="number" placeholder="Amount" onChange={(e)=> setAmount(e.target.value)} required />
                <select value={category} className="" onChange={(e) => setCategory(e.target.value)}>
                    <option value="">Select Category</option>
                    <option value="Food">Food</option>
                    <option value="Transport">Transport</option>
                    <option value="Utilities">Utilities</option>
                    <option value="Entertainment">Entertainment</option>
                    <option value="Shopping">Shopping</option>
                </select>
                <input type="date" className="" onChange={(e) => setDate(e.target.value)} required />
                <button className="" type="submit">Save</button>
            </form>
        </div>
    );
}
