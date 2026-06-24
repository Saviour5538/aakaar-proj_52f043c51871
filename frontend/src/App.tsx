import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AiList from './pages/AiList';
import AiForm from './pages/AiForm';
import DocumentsList from './pages/DocumentsList';
import DocumentsForm from './pages/DocumentsForm';
import ClientList from './pages/ClientList';
import ClientForm from './pages/ClientForm';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/ai-list" element={<AiList />} />
            <Route path="/ai-form" element={<AiForm />} />
            <Route path="/documents-list" element={<DocumentsList />} />
            <Route path="/documents-form" element={<DocumentsForm />} />
            <Route path="/client-list" element={<ClientList />} />
            <Route path="/client-form" element={<ClientForm />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;