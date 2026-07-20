import { useEffect, useState } from "react";
import "./App.css";
import api from "./api";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

function App() {

  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const [form, setForm] = useState({
    Shipping_Mode: "Standard Class",
    Category_Name: "Fishing",
    Market: "Pacific Asia",
    Order_Region: "Southeast Asia",
    Order_Item_Quantity: 1,
    Product_Price: 327.75,
    Sales: 327.75,
    Days_for_shipping_real: 3,
    Days_for_shipment_scheduled: 4
  });

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setError(null);
      const summaryRes = await api.get("/dashboard/summary");
      const historyRes = await api.get("/prediction/history");
      setSummary(summaryRes.data);
      setHistory(historyRes.data);
    } catch (err) {
      console.error("Error loading dashboard data:", err);
      setError(err.message || "Failed to fetch data from the server.");
    }
  };

  const handleChange = (e) => {

    setForm({
      ...form,
      [e.target.name]:
        e.target.type === "number"
          ? Number(e.target.value)
          : e.target.value
    });

  };

  const predict = async () => {

    const res =
      await api.post(
        "/prediction/predict-delay",
        form
      );

    setResult(res.data);

    loadDashboard();

  };

  if (error) {
    return (
      <div style={{ padding: "2rem", textAlign: "center", fontFamily: "sans-serif" }}>
        <h2 style={{ color: "#e53e3e" }}>Failed to Load Dashboard</h2>
        <p style={{ color: "#4a5568" }}>{error}</p>
        <div style={{ marginTop: "1.5rem", padding: "1.5rem", backgroundColor: "#f7fafc", borderRadius: "8px", display: "inline-block", textAlign: "left", maxWidth: "600px", border: "1px solid #e2e8f0" }}>
          <h4 style={{ margin: "0 0 0.5rem 0", color: "#2d3748" }}>Troubleshooting Steps:</h4>
          <ol style={{ lineHeight: "1.6", margin: 0, paddingLeft: "1.2rem", color: "#4a5568" }}>
            <li>
              Make sure you have set the <strong>VITE_API_URL</strong> environment variable in Vercel to point to your deployed backend (e.g., <code>https://your-backend.onrender.com</code>).
            </li>
            <li>
              <strong>Redeploy the application in Vercel</strong> after setting or modifying the environment variable. Vercel needs to rebuild the frontend to inject it.
            </li>
            <li>
              Verify that your backend on Render is up, running, and not spinning down due to Render's free tier inactivity.
            </li>
            <li>
              Check the browser's developer console (F12 or right-click → Inspect → Console) for detailed error logs (e.g., CORS or Mixed Content errors).
            </li>
          </ol>
        </div>
        <br />
        <button 
          onClick={loadDashboard} 
          style={{ marginTop: "1.5rem", padding: "0.6rem 1.2rem", backgroundColor: "#3182ce", color: "white", border: "none", borderRadius: "4px", cursor: "pointer", fontSize: "1rem" }}
        >
          Try Again
        </button>
      </div>
    );
  }

  if (!summary)
    return <h2>Loading Dashboard...</h2>;

  const pieData = [
    {
      name: "Late",
      value: summary.late_deliveries
    },
    {
      name: "On Time",
      value: summary.on_time_deliveries
    }
  ];

  const barData = [
    {
      name: "Late",
      count: summary.late_deliveries
    },
    {
      name: "On Time",
      count: summary.on_time_deliveries
    }
  ];

  const COLORS = [
    "#dc2626",
    "#16a34a"
  ];

  return (

<div className="container">

<div className="header">

<h1>
Supply Chain AI Dashboard
</h1>

<p>
AI-powered Shipment Delay Prediction using Machine Learning
</p>

</div>

<div className="cards">

<div className="card blue">
<h3>Total Predictions</h3>
<h1>{summary.total_predictions}</h1>
</div>

<div className="card red">
<h3>Late Deliveries</h3>
<h1>{summary.late_deliveries}</h1>
</div>

<div className="card green">
<h3>On Time Deliveries</h3>
<h1>{summary.on_time_deliveries}</h1>
</div>

<div className="card purple">
<h3>Average Confidence</h3>
<h1>{summary.average_confidence}%</h1>
</div>

</div>

<div className="section">

<h2>
Delivery Performance
</h2>

<div
style={{
display:"flex",
flexWrap:"wrap",
gap:"40px",
justifyContent:"space-around"
}}
>

<div>

<ResponsiveContainer
width={400}
height={300}
>

<PieChart>

<Pie
data={pieData}
dataKey="value"
cx="50%"
cy="50%"
outerRadius={100}
label
>

{pieData.map((entry,index)=>(
<Cell
key={index}
fill={COLORS[index]}
/>
))}

</Pie>

<Tooltip/>
<Legend/>

</PieChart>

</ResponsiveContainer>

</div>

<div>

<ResponsiveContainer
width={400}
height={300}
>

<BarChart
data={barData}
>

<CartesianGrid strokeDasharray="3 3"/>

<XAxis dataKey="name"/>

<YAxis/>

<Tooltip/>

<Legend/>

<Bar
dataKey="count"
fill="#2563eb"
/>

</BarChart>

</ResponsiveContainer>

</div>

</div>

</div>

<div className="section">

<h2>
Predict Shipment Delay
</h2>

<select
  name="Shipping_Mode"
  value={form.Shipping_Mode}
  onChange={handleChange}
>
  <option>Standard Class</option>
  <option>Second Class</option>
  <option>First Class</option>
  <option>Same Day</option>
</select>

<input
  name="Category_Name"
  value={form.Category_Name}
  onChange={handleChange}
  placeholder="Category"
/>

<select
  name="Market"
  value={form.Market}
  onChange={handleChange}
>
  <option>Pacific Asia</option>
  <option>Europe</option>
  <option>USCA</option>
  <option>LATAM</option>
  <option>Africa</option>
</select>

<input
  name="Order_Region"
  value={form.Order_Region}
  onChange={handleChange}
  placeholder="Order Region"
/>

<input
  type="number"
  name="Order_Item_Quantity"
  value={form.Order_Item_Quantity}
  onChange={handleChange}
  placeholder="Quantity"
/>

<input
  type="number"
  name="Product_Price"
  value={form.Product_Price}
  onChange={handleChange}
  placeholder="Product Price"
/>

<input
  type="number"
  name="Sales"
  value={form.Sales}
  onChange={handleChange}
  placeholder="Sales"
/>

<input
  type="number"
  name="Days_for_shipping_real"
  value={form.Days_for_shipping_real}
  onChange={handleChange}
  placeholder="Actual Shipping Days"
/>

<input
  type="number"
  name="Days_for_shipment_scheduled"
  value={form.Days_for_shipment_scheduled}
  onChange={handleChange}
  placeholder="Scheduled Shipping Days"
/>

<button onClick={predict}>
  Predict Delay
</button>

</div>

{result && (

<div className="section">

<h2>Prediction Result</h2>

<h3>

Prediction :

<span
className={
result.late_delivery_risk===1
?
"status-late"
:
"status-ok"
}
>

{" "}

{
result.late_delivery_risk===1
?
"Late Delivery"
:
"On Time"
}

</span>

</h3>

<h3>

Confidence :

{result.confidence}%

</h3>

</div>

)}

<div className="section">

<h2>

Prediction History

</h2>

<table>

<thead>

<tr>

<th>ID</th>

<th>Category</th>

<th>Market</th>

<th>Region</th>

<th>Status</th>

<th>Confidence</th>

</tr>

</thead>

<tbody>

{history.map((item)=>(

<tr key={item.id}>

<td>{item.id}</td>

<td>{item.category_name}</td>

<td>{item.market}</td>

<td>{item.order_region}</td>

<td>

<span
className={
item.predicted_risk===1
?
"status-late"
:
"status-ok"
}
>

{
item.predicted_risk===1
?
"Late"
:
"On Time"
}

</span>

</td>

<td>

{item.confidence}%

</td>

</tr>

))}

</tbody>

</table>

</div>

<div className="footer">

<hr />

<p>

Supply Chain AI Prediction System

</p>

<p>

• Built with React + FastAPI + XGBoost

</p>

</div>

</div>

);

}

export default App;