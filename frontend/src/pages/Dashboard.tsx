import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchDocuments } from '../api/client';

interface Document {
  id: string;
  name: string;
  uploaded_at: string;
}

const Dashboard: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetchDocuments();
        setDocuments(response);
      } catch (err) {
        setError('Failed to fetch documents. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleUploadClick = () => {
    navigate('/upload');
  };

  const handleChatClick = () => {
    navigate('/chat');
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      {error && (
        <div className="bg-red-100 text-red-700 p-4 rounded mb-6">
          {error}
        </div>
      )}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white shadow rounded p-4">
          <h2 className="text-lg font-semibold">Total Documents</h2>
          <p className="text-2xl font-bold">{documents.length}</p>
        </div>
        <div className="bg-white shadow rounded p-4">
          <h2 className="text-lg font-semibold">Recent Uploads</h2>
          <p className="text-2xl font-bold">{documents.slice(0, 5).length}</p>
        </div>
        <div className="bg-white shadow rounded p-4">
          <h2 className="text-lg font-semibold">Quick Actions</h2>
          <p className="text-2xl font-bold">2</p>
        </div>
      </div>
      <div className="bg-white shadow rounded p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Recent Documents</h2>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr>
                <th className="border-b p-2">Name</th>
                <th className="border-b p-2">Uploaded At</th>
              </tr>
            </thead>
            <tbody>
              {documents.slice(0, 5).map((doc) => (
                <tr key={doc.id}>
                  <td className="border-b p-2">{doc.name}</td>
                  <td className="border-b p-2">{new Date(doc.uploaded_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
      <div className="flex gap-4">
        <button
          onClick={handleUploadClick}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Upload Documents
        </button>
        <button
          onClick={handleChatClick}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        >
          Start Chat
        </button>
      </div>
    </div>
  );
};

export default Dashboard;