import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import ErrorBoundary from './components/ErrorBoundary'

console.log('🚀 PredictPesa App Starting...');
console.log('Environment:', import.meta.env.MODE);

const rootElement = document.getElementById("root");

if (!rootElement) {
  console.error('❌ Root element not found!');
  document.body.innerHTML = '<div style="padding: 20px; font-family: system-ui;"><h1>Error: Root element not found</h1><p>The app could not mount properly.</p></div>';
} else {
  console.log('✅ Root element found, mounting app...');
  createRoot(rootElement).render(
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  );
  console.log('✅ App mounted successfully');
}
