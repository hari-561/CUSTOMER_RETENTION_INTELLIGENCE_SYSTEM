import { useState } from "react";
import api from "../api";

function ChurnPrediction() {
  const [formData, setFormData] = useState({
    tenure: "",
    monthly_charges: "",
    contract_type: "Month-to-month",
    service_count: 0,
    internet_service:"DSL"
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // -----------------------------------------
  // Handle input changes
  // -----------------------------------------

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // -----------------------------------------
  // Risk color
  // -----------------------------------------

  const getRiskColor = (riskScore) => {
    if (riskScore < 0.3) {
      return "#28a745";
    }

    if (riskScore <= 0.6) {
      return "#ffc107";
    }

    return "#dc3545";
  };

  // -----------------------------------------
  // Risk label
  // -----------------------------------------

  const getRiskLabel = (riskScore) => {
    if (riskScore < 0.3) {
      return "Low Risk";
    }

    if (riskScore <= 0.6) {
      return "Medium Risk";
    }

    return "High Risk";
  };

  // -----------------------------------------
  // Submit prediction
  // -----------------------------------------

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const payload = {
        tenure: Number(formData.tenure),
        monthly_charges: Number(formData.monthly_charges),
        contract_type: formData.contract_type,
        service_count: Number(formData.service_count),
        internet_service:formData.internet_service
      };

      console.log("Sending payload:", payload);

      const response = await api.post(
        "/predict-churn",
        payload
      );

      console.log("API response:", response.data);

      setResult(response.data);

    } catch (err) {
      console.error("Prediction error:", err);

      if (err.response?.status === 422) {
        const validationErrors =
          err.response.data?.detail;

        if (
          validationErrors &&
          Array.isArray(validationErrors)
        ) {
          const message = validationErrors
            .map((item) => item.msg)
            .join(", ");

          setError(message);
        } else {
          setError("Validation error");
        }
      } else {
        setError(
          err.response?.data?.detail ||
          "Failed to generate churn prediction"
        );
      }

    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>

      <h1>Churn Prediction</h1>

      <p>
        Enter customer attributes to estimate
        churn probability and prediction confidence.
      </p>

      {/* ---------------------------------- */}
      {/* Prediction Form */}
      {/* ---------------------------------- */}

      <form
        onSubmit={handleSubmit}
        style={{
          maxWidth: "500px",
          display: "flex",
          flexDirection: "column",
          gap: "15px",
        }}
      >

        {/* Tenure */}

        <div>
          <label>Tenure</label>

          <input
            type="number"
            name="tenure"
            value={formData.tenure}
            onChange={handleChange}
            required
            min="0"
            style={{
              width: "100%",
              padding: "8px",
              marginTop: "5px",
            }}
          />
        </div>

        {/* Monthly Charges */}

        <div>
          <label>Monthly Charges</label>

          <input
            type="number"
            name="monthly_charges"
            value={formData.monthly_charges}
            onChange={handleChange}
            required
            min="0"
            step="0.01"
            style={{
              width: "100%",
              padding: "8px",
              marginTop: "5px",
            }}
          />
        </div>

        {/* Internet Service */}

        <div>
          <label>Internet Service</label>

          <select
            name="internet_service"
            value={formData.internet_service}
            onChange={handleChange}
            style={{
              width: "100%",
              padding: "8px",
              marginTop: "5px",
            }}
          >
            <option value="DSL">
              DSL
            </option>

            <option value="Fiber optic">
              Fiber optic
            </option>

            <option value="No">
              No service
            </option>
          </select>
        </div>

        {/* Service Count */}

        <div>
          <label>Service Count</label>

          <input
            type="number"
            name="service_count"
            value={formData.service_count}
            onChange={handleChange}
            required
            min="0"
            max="6"
            style={{
              width: "100%",
              padding: "8px",
              marginTop: "5px",
            }}
          />
        </div>

          <div>
          <label>Contract Type</label>

          <select
            name="contract_type"
            value={formData.contract_type}
            onChange={handleChange}
            style={{
              width: "100%",
              padding: "8px",
              marginTop: "5px",
            }}
          >
            <option value="Month-to-month">
              Month-to-month
            </option>

            <option value="One year">
              One year
            </option>

            <option value="Two year">
              Two year
            </option>
          </select>
        </div>


        {/* Submit */}

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "10px",
            cursor: loading
              ? "not-allowed"
              : "pointer",
          }}
        >
          {loading
            ? "Predicting..."
            : "Predict Churn"}
        </button>

      </form>

      {/* ---------------------------------- */}
      {/* Error */}
      {/* ---------------------------------- */}

      {error && (
        <div
          style={{
            marginTop: "20px",
            color: "red",
            fontWeight: "bold",
          }}
        >
          {error}
        </div>
      )}

      {/* ---------------------------------- */}
      {/* Prediction Result */}
      {/* ---------------------------------- */}

      {result && (
        <div
          style={{
            marginTop: "30px",
            padding: "20px",
            borderRadius: "10px",
            backgroundColor: "#f8f9fa",
            border: "1px solid #ddd",
            maxWidth: "500px",
          }}
        >

          <h2>Prediction Result</h2>

          {/* Risk Score */}

          <p>
            <strong>Risk Score:</strong>{" "}
            {(result.risk_score * 100).toFixed(1)}%
          </p>

          {/* Prediction */}

          <p>
            <strong>Prediction:</strong>{" "}
            {result.prediction}
          </p>

          {/* Confidence */}

          <p>
            <strong>Confidence:</strong>{" "}
            {(result.confidence * 100).toFixed(1)}%
          </p>

          {/* Risk Indicator */}

          <div
            style={{
              marginTop: "15px",
              padding: "15px",
              borderRadius: "8px",
              color: "white",
              backgroundColor: getRiskColor(
                result.risk_score
              ),
            }}
          >
            <strong>
              {getRiskLabel(result.risk_score)}
            </strong>

            <div
              style={{
                marginTop: "5px",
              }}
            >
              Risk Score:{" "}
              {(result.risk_score * 100).toFixed(1)}%
            </div>

            <div
              style={{
                marginTop: "5px",
              }}
            >
              Prediction: {result.prediction}
            </div>

            <div
              style={{
                marginTop: "5px",
              }}
            >
              Confidence:{" "}
              {(result.confidence * 100).toFixed(1)}%
            </div>
          </div>

        </div>
      )}

    </div>
  );
}

export default ChurnPrediction;