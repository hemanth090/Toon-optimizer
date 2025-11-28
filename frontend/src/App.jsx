import { useState } from 'react';
import StatusIndicator from './components/StatusIndicator';
import JsonToToon from './components/JsonToToon';
import ToonToJson from './components/ToonToJson';
import QueryAnalysis from './components/QueryAnalysis';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('json-to-toon');

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1 className="app-title">TOON Studio</h1>
          <p className="app-subtitle">Token Efficiency Toolkit</p>
        </div>

        <nav className="nav-menu">
          <button
            className={`nav-item ${activeTab === 'json-to-toon' ? 'active' : ''}`}
            onClick={() => setActiveTab('json-to-toon')}
          >
            <span className="nav-icon">📝</span>
            <span className="nav-label">JSON to TOON</span>
          </button>
          <button
            className={`nav-item ${activeTab === 'toon-to-json' ? 'active' : ''}`}
            onClick={() => setActiveTab('toon-to-json')}
          >
            <span className="nav-icon">🔄</span>
            <span className="nav-label">TOON to JSON</span>
          </button>
          <button
            className={`nav-item ${activeTab === 'query' ? 'active' : ''}`}
            onClick={() => setActiveTab('query')}
          >
            <span className="nav-icon">🤖</span>
            <span className="nav-label">Query & Analysis</span>
          </button>
        </nav>

        <div className="sidebar-footer">
          <StatusIndicator />
        </div>
      </aside>

      <main className="main-content">
        <header className="content-header">
          <h2>
            {activeTab === 'json-to-toon' && 'JSON to TOON Converter'}
            {activeTab === 'toon-to-json' && 'TOON to JSON Converter'}
            {activeTab === 'query' && 'AI-Powered Query & Analysis'}
          </h2>
          <p className="content-description">
            {activeTab === 'json-to-toon' && 'Convert JSON to efficient TOON format and save tokens'}
            {activeTab === 'toon-to-json' && 'Convert TOON format back to standard JSON'}
            {activeTab === 'query' && 'Ask questions about your data using Google Gemini AI'}
          </p>
        </header>

        <div className="content-body">
          {activeTab === 'json-to-toon' && <JsonToToon />}
          {activeTab === 'toon-to-json' && <ToonToJson />}
          {activeTab === 'query' && <QueryAnalysis />}
        </div>
      </main>
    </div>
  );
}

export default App;
