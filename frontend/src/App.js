import React from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { GenerateDescription } from './pages';
import './styles/App.css';

function App() {

  return (
    <div className="App">
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
      />
      <header className="App-header">
        <h1>AI-Powered Menu Intelligence Widget</h1>
      </header>
      
      <GenerateDescription />
    </div>
  );
}

export default App;
