import { useEffect, useState } from "react";
import api from "../api";

function HighRiskCustomers() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [limit, setLimit] = useState(50);

  const [minTenure, setMinTenure] = useState("");
  const [maxTenure, setMaxTenure] = useState("");

  const [sortOrder, setSortOrder] = useState("asc");

  const fetchCustomers = async (
    currentLimit = limit
  ) => {
    try {
      setLoading(true);
      setError("");

      const params = {
        limit: currentLimit,
      };

      if (minTenure !== "") {
        params.min_tenure = Number(minTenure);
      }

      if (maxTenure !== "") {
        params.max_tenure = Number(maxTenure);
      }

      const response = await api.get(
        "/customers/high-risk",
        { params }
      );

      setCustomers(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch high-risk customers");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const handleSearch = () => {
    setLimit(50);
    fetchCustomers(50);
  };

  const handleLoadMore = () => {
    const newLimit = limit + 50;

    setLimit(newLimit);

    fetchCustomers(newLimit);
  };

  const handleSort = () => {
    const sortedCustomers = [...customers].sort(
      (a, b) => {
        return sortOrder === "asc"
          ? a.tenure - b.tenure
          : b.tenure - a.tenure;
      }
    );

    setCustomers(sortedCustomers);

    setSortOrder(
      sortOrder === "asc" ? "desc" : "asc"
    );
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>High Risk Customers</h1>

      <p>
        Customers identified as likely to churn
        based on tenure, contract type, and
        other risk indicators.
      </p>

      {/* Filters */}
      <div
        style={{
          display: "flex",
          gap: "10px",
          marginBottom: "20px",
          alignItems: "center",
          flexWrap: "wrap",
        }}
      >
        <input
          type="number"
          placeholder="Min Tenure"
          value={minTenure}
          onChange={(e) =>
            setMinTenure(e.target.value)
          }
        />

        <input
          type="number"
          placeholder="Max Tenure"
          value={maxTenure}
          onChange={(e) =>
            setMaxTenure(e.target.value)
          }
        />

        <button onClick={handleSearch}>
          Apply Filters
        </button>

        <button
          onClick={() => {
            setMinTenure("");
            setMaxTenure("");
            setLimit(50);

            fetchCustomers(50);
          }}
        >
          Reset
        </button>
      </div>

      {loading && (
        <h3>Loading high-risk customers...</h3>
      )}

      {error && (
        <h3 style={{ color: "red" }}>
          {error}
        </h3>
      )}

      {!loading && !error && (
        <>
          <div
            style={{
              background: "#fff3cd",
              padding: "12px",
              borderRadius: "8px",
              marginBottom: "20px",
              fontWeight: "bold",
            }}
          >
            {customers.length} high-risk customers
            identified
          </div>

          {customers.length === 0 ? (
            <h3>No high-risk customers found</h3>
          ) : (
            <>
              <table
                style={{
                  width: "100%",
                  borderCollapse: "collapse",
                }}
              >
                <thead>
                  <tr>
                    <th style={headerStyle}>
                      Customer ID
                    </th>

                    <th
                      style={{
                        ...headerStyle,
                        cursor: "pointer",
                      }}
                      onClick={handleSort}
                    >
                      Tenure{" "}
                      {sortOrder === "asc"
                        ? "▲"
                        : "▼"}
                    </th>

                    <th style={headerStyle}>
                      Monthly Charges
                    </th>

                    <th style={headerStyle}>
                      Contract Type
                    </th>

                    <th style={headerStyle}>
                      Risk Reason
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {customers.map((customer) => (
                    <tr key={customer.customer_id}>
                      <td style={cellStyle}>
                        {customer.customer_id}
                      </td>

                      <td style={cellStyle}>
                        {customer.tenure}
                      </td>

                      <td style={cellStyle}>
                        $
                        {Number(
                          customer.monthly_charges
                        ).toFixed(2)}
                      </td>

                      <td style={cellStyle}>
                        {customer.contract_type}
                      </td>

                      <td style={cellStyle}>
                        {customer.risk_reason}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <button
                onClick={handleLoadMore}
                style={{
                  marginTop: "20px",
                  padding: "10px 20px",
                }}
              >
                Load More (+50)
              </button>
            </>
          )}
        </>
      )}
    </div>
  );
}

const headerStyle = {
  border: "1px solid #ddd",
  padding: "12px",
  backgroundColor: "#f5f5f5",
  textAlign: "left",
};

const cellStyle = {
  border: "1px solid #ddd",
  padding: "12px",
};

export default HighRiskCustomers;