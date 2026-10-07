import { useEffect, useState } from "react";
import api from "../api";

function ChurnSummary() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await api.get("/churn/summary");
        setSummary(response.data);
      } catch (err) {
        console.error(err);
        setError("Failed to load churn summary");
      } finally {
        setLoading(false);
      }
    };

    fetchSummary();
  }, []);

  if (loading) {
    return <h2>Loading...</h2>;
  }

  if (error) {
    return <h2 style={{ color: "red" }}>{error}</h2>;
  }

  if (!summary) {
    return <h2>No data available</h2>;
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Churn Summary Dashboard</h1>

      <p style={{ color: "#666" }}>
        This page provides an overview of customer churn metrics
        and contract-wise churn performance.
      </p>

      {/* KPI Cards */}
      <div
        style={{
          display: "flex",
          gap: "20px",
          marginTop: "20px",
          marginBottom: "30px",
        }}
      >
        <div style={cardStyle}>
          <h3>Total Customers</h3>
          <h2>{summary.summary.total_customers}</h2>
        </div>

        <div style={cardStyle}>
          <h3>Total Churned</h3>
          <h2>{summary.summary.total_churned}</h2>
        </div>

        <div style={cardStyle}>
          <h3>Churn Rate</h3>
          <h2>
            {(summary.summary.churn_rate * 100).toFixed(1)}%
          </h2>
        </div>
      </div>

      {/* Contract Churn Table */}
      <h2>Contract Type Churn Analysis</h2>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "15px",
        }}
      >
        <thead>
          <tr style={{ backgroundColor: "#f5f5f5" }}>
            <th style={tableHeader}>Contract Type</th>
            <th style={tableHeader}>Churn Rate</th>
            <th style={tableHeader}>Visual</th>
          </tr>
        </thead>

        <tbody>
          {summary.churn_by_contract_type.map((item) => (
            <tr key={item.contract_type}>
              <td style={tableCell}>
                {item.contract_type}
              </td>

              <td style={tableCell}>
                {(item.churn_rate * 100).toFixed(1)}%
              </td>

              <td style={tableCell}>
                <div
                  style={{
                    width: "250px",
                    backgroundColor: "#eee",
                    borderRadius: "5px",
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      width: `${item.churn_rate * 100}%`,
                      height: "20px",
                      backgroundColor: "#0d6efd",
                    }}
                  />
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Internet Service Churn Table */}
      <h2 style={{ marginTop: "30px" }}>
        Internet Service Churn Analysis
      </h2>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "15px",
        }}
      >
        <thead>
          <tr style={{ backgroundColor: "#f5f5f5" }}>
            <th style={tableHeader}>Internet Service</th>
            <th style={tableHeader}>Churn Rate</th>
            <th style={tableHeader}>Visual</th>
          </tr>
        </thead>

        <tbody>
          {summary.churn_by_internet_service.map((item) => (
            <tr key={item.internet_service}>
              <td style={tableCell}>
                {item.internet_service}
              </td>

              <td style={tableCell}>
                {(item.churn_rate * 100).toFixed(1)}%
              </td>

              <td style={tableCell}>
                <div
                  style={{
                    width: "250px",
                    backgroundColor: "#eee",
                    borderRadius: "5px",
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      width: `${item.churn_rate * 100}%`,
                      height: "20px",
                      backgroundColor: "#0d6efd",
                    }}
                  />
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const cardStyle = {
  flex: 1,
  padding: "20px",
  backgroundColor: "#f8f9fa",
  borderRadius: "10px",
  boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
  textAlign: "center",
};

const tableHeader = {
  border: "1px solid #ddd",
  padding: "12px",
  textAlign: "left",
};

const tableCell = {
  border: "1px solid #ddd",
  padding: "12px",
};

export default ChurnSummary;