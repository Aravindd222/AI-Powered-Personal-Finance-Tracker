import { useEffect,useState  } from "react";
import { getMonthlySummary } from "../api/expenses";
import {PieChart,Pie,Cell} from "recharts";

export default function Dashboard(){
    const [data,setData] = useState([]);
    
    useEffect(() => {
        getMonthlySummary().then((res) => setData(res.data));
    }, []);

    const COLORS = ['blue', 'orange', 'green', 'red'];

    return(
        <div className="">
            <h1 className="">Dashboard</h1>
            <div>
                <div>
                    <h2>Monthly Spending</h2>
                    <PieChart width={400} height={400}>
                        <Pie data={data} dataKey = "total" nameKey="category" outerRadius={150}>
                            {data.map((_,index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}

                        </Pie>
                    </PieChart>
                </div>
                <div>
                    <h2>Category Breakdown</h2>
                    <ul>
                        {data.map((item,idx)=>(
                            <li key={idx} className="">
                                <span>{item.category}</span>
                                <span>{item.total}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}