import { Outlet } from 'react-router-dom';
import Header from './Header';
import MobileNavigation from './MobileNavigation';

const Layout = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="pb-16 md:pb-0">
        <Outlet />
      </main>
      <MobileNavigation />
    </div>
  );
};

export default Layout;