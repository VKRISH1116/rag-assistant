/**
 * Main App Component
 * 
 * This is the main React component that:
 * 1. Shows document upload interface
 * 2. Displays chat interface for Q&A
 * 3. Connects to FastAPI backend
 */

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
import DocumentUpload from './components/DocumentUpload';
import ChatInterface from './components/ChatInterface';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [documentUploaded, setDocumentUploaded] = useState(false);
  const [documentName, setDocumentName] = useState('');
  const [stats, setStats] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [mode, setMode] = useState('Loading...');

  const refreshDashboard = async () => {
    try {
      const [healthResponse, statsResponse, documentsResponse] = await Promise.all([
        axios.get(`${API_URL}/health`),
        axios.get(`${API_URL}/stats`),
        axios.get(`${API_URL}/documents`),
      ]);
      setMode(healthResponse.data.mode || 'Unknown');
      setStats(statsResponse.data);
      setDocuments(documentsResponse.data.documents || []);
      setDocumentUploaded((statsResponse.data.total_documents || 0) > 0);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    refreshDashboard();
  }, []);

  const handleDeleteDocument = async (documentId) => {
    try {
      await axios.delete(`${API_URL}/documents/${encodeURIComponent(documentId)}`);
      await refreshDashboard();
    } catch (error) {
      console.error(error);
    }
  };

  const handleExportConversation = () => {
    window.open(`${API_URL}/export/default`, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 RAG Assistant</h1>
        <p>Intelligent Document Q&A with RAG & Agentic AI</p>
      </header>

      <main className="App-main">
        <section className="upload-section">
          <DocumentUpload
            onUploadSuccess={async (filename) => {
              setDocumentUploaded(true);
              setDocumentName(filename);
              await refreshDashboard();
            }}
          />
          {documentUploaded && (
            <div className="success-message">
              ✅ Document "{documentName}" uploaded successfully!
            </div>
          )}
        </section>

        <section className="overview-section">
          <div className="overview-card">
            <h3>⚙️ Backend status</h3>
            <p>{mode}</p>
            {stats && (
              <>
                <p>Total chunks: {stats.total_chunks}</p>
                <p>Documents indexed: {stats.total_documents}</p>
              </>
            )}
          </div>
          <div className="overview-card">
            <h3>📚 Managed documents</h3>
            {documents.length === 0 ? (
              <p>No documents uploaded yet.</p>
            ) : (
              <ul>
                {documents.map((doc) => (
                  <li key={doc.document_id}>
                    <span>{doc.filename}</span>
                    <small>{doc.chunks} chunks</small>
                    <button onClick={() => handleDeleteDocument(doc.document_id)}>Delete</button>
                  </li>
                ))}
              </ul>
            )}
            <button className="export-button" onClick={handleExportConversation}>Export conversation</button>
          </div>
        </section>

        <section className="chat-section">
          <ChatInterface disabled={!documentUploaded} />
        </section>
      </main>

      <footer className="App-footer">
        <p>Built with FastAPI, LangChain, LlamaIndex, and React</p>
      </footer>
    </div>
  );
}

export default App;


