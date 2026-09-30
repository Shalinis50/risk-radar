import { useState } from "react";
import "./App.css";
import riskRadarLogo from "./assets/riskradar-logo.png";

const initialTransactions = [
  {
    id: 1,
    user: "USER001",
    amount: 95000,
    location: "Chennai",
    risk: "HIGH",
    score: 90,
    rules: ["unusual amount", "transaction velocity"],
    status: "FLAGGED",
  },
  {
    id: 2,
    user: "USER002",
    amount: 2500,
    location: "Bangalore",
    risk: "MEDIUM",
    score: 40,
    rules: ["transaction velocity"],
    status: "FLAGGED",
  },
];

function App() {
  const [transactions, setTransactions] =
    useState(initialTransactions);

  function updateStatus(id, status) {
    setTransactions((currentTransactions) =>
      currentTransactions.map((transaction) =>
        transaction.id === id
          ? { ...transaction, status }
          : transaction
      )
    );
  }

  function refreshDashboard() {
    setTransactions(initialTransactions);
  }

  const flaggedCount = transactions.filter(
    (transaction) => transaction.status === "FLAGGED"
  ).length;

  const highRiskCount = transactions.filter(
    (transaction) => transaction.risk === "HIGH"
  ).length;

  const reviewedCount = transactions.filter(
    (transaction) =>
      transaction.status === "REVIEWED" ||
      transaction.status === "CLEARED"
  ).length;

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
  <img
    src={riskRadarLogo}
    alt="RiskRadar logo"
    className="brand-logo"
  />

  <div className="brand-text">
    <h2>RiskRadar</h2>
    <span>Fraud Intelligence Console</span>
  </div>
</div>

        <div className="system-status">
          <span className="status-dot"></span>
          System Online
        </div>
      </header>

      <main className="dashboard">
        <section className="page-heading">
          <div>
            <span className="eyebrow">RISK OPERATIONS</span>
            <h1>Transaction Review</h1>
            <p>
              Monitor suspicious transactions and review
              potential fraud activity.
            </p>
          </div>

          <button
            className="refresh-button"
            onClick={refreshDashboard}
          >
            ↻ Refresh
          </button>
        </section>

        <section className="summary">
          <div className="summary-card">
            <div className="card-icon blue">!</div>
            <div>
              <span>Flagged Transactions</span>
              <strong>{flaggedCount}</strong>
            </div>
          </div>

          <div className="summary-card">
            <div className="card-icon red">⚠</div>
            <div>
              <span>High Risk</span>
              <strong>{highRiskCount}</strong>
            </div>
          </div>

          <div className="summary-card">
            <div className="card-icon green">✓</div>
            <div>
              <span>Reviewed</span>
              <strong>{reviewedCount}</strong>
            </div>
          </div>
        </section>

        <section className="table-section">
          <div className="section-header">
            <div>
              <h2>Flagged Transactions</h2>
              <p>Transactions requiring analyst attention</p>
            </div>

            <span className="live-badge">
              ● LIVE
            </span>
          </div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Transaction</th>
                  <th>User</th>
                  <th>Amount</th>
                  <th>Location</th>
                  <th>Risk Level</th>
                  <th>Triggered Rules</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>
                {transactions.map((transaction) => (
                  <tr key={transaction.id}>
                    <td>
                      <span className="transaction-id">
                        TXN-{String(transaction.id).padStart(4, "0")}
                      </span>
                    </td>

                    <td>
                      <span className="user-id">
                        {transaction.user}
                      </span>
                    </td>

                    <td>
                      <strong className="amount">
                        ₹{transaction.amount.toLocaleString("en-IN")}
                      </strong>
                    </td>

                    <td>
                      <span className="location">
                        ● {transaction.location}
                      </span>
                    </td>

                    <td>
                      <div className="risk-cell">
                        <span
                          className={`risk-badge ${transaction.risk.toLowerCase()}`}
                        >
                          {transaction.risk}
                        </span>

                        <div className="risk-score">
                          <div className="score-bar">
                            <div
                              className={`score-fill ${transaction.risk.toLowerCase()}`}
                              style={{
                                width: `${transaction.score}%`,
                              }}
                            ></div>
                          </div>

                          <span>
                            {transaction.score}/100
                          </span>
                        </div>
                      </div>
                    </td>

                    <td>
                      <div className="rules">
                        {transaction.rules.map((rule) => (
                          <span
                            className="rule-tag"
                            key={rule}
                          >
                            {rule}
                          </span>
                        ))}
                      </div>
                    </td>

                    <td>
                      <span
                        className={`status-badge ${transaction.status.toLowerCase()}`}
                      >
                        {transaction.status}
                      </span>
                    </td>

                    <td>
                      <div className="actions">
                        <button
                          className="review-button"
                          onClick={() =>
                            updateStatus(
                              transaction.id,
                              "REVIEWED"
                            )
                          }
                        >
                          ✓ Review
                        </button>

                        <button
                          className="clear-button"
                          onClick={() =>
                            updateStatus(
                              transaction.id,
                              "CLEARED"
                            )
                          }
                        >
                          Clear
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <footer className="footer">
          RiskRadar Fraud Detection System
          <span>•</span>
          Analyst Review Console
        </footer>
      </main>
    </div>
  );
}

export default App;