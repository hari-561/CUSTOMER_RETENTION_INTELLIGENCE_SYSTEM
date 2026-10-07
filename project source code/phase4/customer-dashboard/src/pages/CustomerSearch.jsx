import { useState } from "react";
import api from "../api";

function CustomerSearch() {
  const [customerId, setCustomerId] = useState("");
  const [customer, setCustomer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    if (!customerId.trim()) {
      setError("Please enter a Customer ID");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setCustomer(null);

      const response = await api.get(`/customers/${customerId}`);

      setCustomer(response.data);
    } catch (err) {
      if (err.response?.status === 404) {
        setError("Customer not found");
      } else {
        setError("Failed to fetch customer details");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Customer Search</h2>

      <input
        type="text"
        placeholder="Enter Customer ID"
        value={customerId}
        onChange={(e) => setCustomerId(e.target.value)}
        style={{
          padding: "10px",
          width: "250px",
          marginRight: "10px",
        }}
      />

      <button onClick={handleSearch}>
        Search
      </button>

      {loading && (
        <p style={{ marginTop: "15px" }}>
          Loading...
        </p>
      )}

      {error && (
        <p
          style={{
            color: "red",
            marginTop: "15px",
          }}
        >
          {error}
        </p>
      )}

      {customer && (
        <div
          style={{
            marginTop: "20px",
            border: "1px solid #ddd",
            borderRadius: "10px",
            padding: "20px",
            maxWidth: "500px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
          }}
        >
          <h3>Customer Details</h3>

          <p>
            <strong>Customer ID:</strong>{" "}
            {customer.customer_id}
          </p>

          <p>
            <strong>Tenure:</strong>{" "}
            {customer.tenure}
          </p>

          <p>
            <strong>Contract Type:</strong>{" "}
            {customer.contract_type}
          </p>

          <p>
            <strong>Internet Service:</strong>{" "}
            {customer.internet_service}
          </p>

          <p>
            <strong>Monthly Charges:</strong> ₹
            {customer.monthly_charges}
          </p>

          <p>
            <strong>Status:</strong>{" "}
            <span
              style={{
                padding: "6px 12px",
                borderRadius: "6px",
                color: "white",
                backgroundColor:
                  customer.churn
                    ? "#dc3545"
                    : "#28a745",
              }}
            >
              {customer.churn
                ? "Churned"
                : "Active"}
            </span>
          </p>
        </div>
      )}
    </div>
  );
}

export default CustomerSearch;