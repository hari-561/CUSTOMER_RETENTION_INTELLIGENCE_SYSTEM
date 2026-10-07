import { useState } from "react";
import CustomerSearch from "./pages/CustomerSearch";
import ChurnSummary from "./pages/ChurnSummary";
import HighRiskCustomers from "./pages/HighRiskCustomers";
import ChurnPrediction from "./pages/ChurnPrediction";
// function App() {
//   const [activeTab, setActiveTab] =
//     useState("search");

//   return (
//     <div>
//       <h1>Customer Dashboard</h1>

//       <div style={{ marginBottom: "20px" }}>
//         <button
//           onClick={() =>
//             setActiveTab("search")
//           }
//         >
//           Customer Search
//         </button>
//       </div>

//       {activeTab === "search" && (
//         <CustomerSearch />
//       )}
//     </div>
//   );
// }

// export default App;


// function App() {
//   const [activeTab, setActiveTab] = useState("summary");

//   return (
//     <div>
//       <h1>Customer Dashboard</h1>

//       <div
//         style={{
//           display: "flex",
//           gap: "10px",
//           marginBottom: "20px",
//         }}
//       >
//         <button
//           onClick={() => setActiveTab("summary")}
//         >
//           Churn Summary
//         </button>

//         <button
//           onClick={() => setActiveTab("search")}
//         >
//           Customer Search
//         </button>
//       </div>

//       {activeTab === "summary" && <ChurnSummary />}

//       {activeTab === "search" && <CustomerSearch />}
//     </div>
//   );
// }

// export default App;


function App() {
  const [activeTab, setActiveTab] = useState("summary");

  return (
    <div>
      <h1>Customer Dashboard</h1>

      <div style={{ marginBottom: "20px" }}>
        <button onClick={() => setActiveTab("summary")}>
          Churn Summary
        </button>

        <button
          onClick={() => setActiveTab("search")}
          style={{ marginLeft: "10px" }}
        >
          Customer Search
        </button>

        <button
          onClick={() => setActiveTab("highRisk")}
          style={{ marginLeft: "10px" }}
        >
          High Risk Customers
        </button>
        <button
  onClick={() => setActiveTab("prediction")}
   style={{ marginLeft: "10px" }}
>
  Churn Prediction
</button>
      </div>

      {activeTab === "summary" && <ChurnSummary />}
      {activeTab === "search" && <CustomerSearch />}
      {activeTab === "highRisk" && (
        <HighRiskCustomers />
      )}
      {activeTab === "prediction" && (
  <ChurnPrediction />
)}
    </div>
  );
}

export default App;