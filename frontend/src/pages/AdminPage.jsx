import React from 'react';
import { Dashboard } from '../components/Admin/Dashboard';
import { UserManagement } from '../components/Admin/UserManagement';
import { CrisisAlerts } from '../components/Admin/CrisisAlerts';

export const AdminPage = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="admin-page">
      <h1>Admin Panel</h1>
      <div className="admin-tabs">
        <button
          className={activeTab === 'dashboard' ? 'active' : ''}
          onClick={() => setActiveTab('dashboard')}
        >
          Dashboard
        </button>
        <button
          className={activeTab === 'users' ? 'active' : ''}
          onClick={() => setActiveTab('users')}
        >
          Users
        </button>
        <button
          className={activeTab === 'alerts' ? 'active' : ''}
          onClick={() => setActiveTab('alerts')}
        >
          Crisis Alerts
        </button>
      </div>

      <div className="admin-content">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'users' && <UserManagement />}
        {activeTab === 'alerts' && <CrisisAlerts />}
      </div>
    </div>
  );
};
