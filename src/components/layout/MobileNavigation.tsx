import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, TrendingUp, Briefcase, Gift, User } from 'lucide-react';

const MobileNavigation = () => {
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Markets', href: '/markets', icon: TrendingUp },
    { name: 'Portfolio', href: '/portfolio', icon: Briefcase },
    { name: 'Rewards', href: '/rewards', icon: Gift },
    { name: 'Profile', href: '/profile', icon: User },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 bg-gunmetal border-t border-charcoal md:hidden">
      <div className="grid grid-cols-5 h-16">
        {navItems.map((item) => (
          <Link
            key={item.name}
            to={item.href}
            className={`flex flex-col items-center justify-center space-y-1 transition-smooth ${
              isActive(item.href)
                ? 'text-cyber glow'
                : 'text-muted-foreground hover:text-cyber'
            }`}
          >
            <item.icon className="h-5 w-5" />
            <span className="text-xs font-crypto">{item.name}</span>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default MobileNavigation;