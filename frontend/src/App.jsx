import { useState } from "react";
import "./App.css";

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

  const flaggedCount = transactions.filter(
    (transaction) => transaction.status === "FLAGGED"
  ).length;

  const highRiskCount = transactions.filter(
    (transaction) => transaction.risk === "HIGH"
  ).length;

  return (
    <div className="dashboard">
      <header className="header">
        <div>
          <h1>Fraud Detection Console</h1>
          <p>Transaction Risk Review Dashboard</p>
        </div>

        <button className="refresh-button">
          Refresh
        </button>
      </header>

      <section className="summary">
        <div className="summary-card">
          <span>Flagged Transactions</span>
          <strong>{transactions.length}</strong>
        </div>

        <div className="summary-card">
          <span>High Risk</span>
          <strong>{highRiskCount}</strong>
        </div>

        <div className="summary-card">
          <span>Pending Review</span>
          <strong>{flaggedCount}</strong>
        </div>
      </section>

      <section className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>User</th>
              <th>Amount</th>
              <th>Location</th>
              <th>Risk</th>
              <th>Rules Triggered</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {transactions.map((transaction) => (
              <tr key={transaction.id}>
                <td>#{transaction.id}</td>

                <td>{transaction.user}</td>

                <td>
                  ₹{transaction.amount.toLocaleString("en-IN")}
                </td>

                <td>{transaction.location}</td>

                <td>
                  <span
                    className={`risk-badge ${transaction.risk.toLowerCase()}`}
                  >
                    {transaction.risk}
                  </span>

                  <div className="score">
                    {transaction.score}/100
                  </div>
                </td>

                <td>
                  {transaction.rules.map((rule) => (
                    <span className="rule-tag" key={rule}>
                      {rule}
                    </span>
                  ))}
                </td>

                <td>{transaction.status}</td>

                <td>
                  <button
                    className="review-button"
                    onClick={() =>
                      updateStatus(
                        transaction.id,
                        "REVIEWED"
                      )
                    }
                  >
                    Reviewed
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
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}

export default App;