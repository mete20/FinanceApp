import React, { useState } from 'react';

function Dashboard() {
  const [users, setUsers] = useState([]);
  const [stocks, setStocks] = useState([]);
  const [currentView, setCurrentView] = useState(''); // 'users', 'stocks', etc.

  const fetchData = (endpoint, setter) => {
    fetch(`http://localhost:8000/${endpoint}`)
      .then(response => response.json())
      .then(data => setter(data))
      .catch(error => console.error('Error fetching data:', error));
  };

  const handleButtonClick = (view) => {
    setCurrentView(view);
    switch(view) {
      case 'users':
        fetchData('users', setUsers);
        break;
      case 'stocks':
        fetchData('stocks', setStocks);
        break;
      // Add more cases for other buttons
      default:
        break;
    }
  };

  return (
    <div>
      <button onClick={() => handleButtonClick('users')}>Get Users</button>
      <button onClick={() => handleButtonClick('stocks')}>Get Stocks</button>
      {/* Add more buttons for other data */}

      {currentView === 'users' && (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              {/* Add more table headers */}
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.name}</td>
                {/* Add more user details */}
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {currentView === 'stocks' && (
        <ul>
          {stocks.map(stock => (
            <li key={stock.id}>{stock.name} - {stock.price}</li>
          ))}
        </ul>
      )}
      {/* Add more views for other data */}
    </div>
  );
}

export default Dashboard;
