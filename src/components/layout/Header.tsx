import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Bitcoin, Menu, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import WalletConnectionModal from '../modals/WalletConnectionModal';

const Header = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isWalletModalOpen, setIsWalletModalOpen] = useState(false);
  const [connectedWallet, setConnectedWallet] = useState<string | null>(null);
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Markets', href: '/markets' },
    { name: 'Portfolio', href: '/portfolio' },
    { name: 'Rewards', href: '/rewards' },
  ];

  const isActive = (path: string) => location.pathname === path;

  const handleWalletConnect = (address: string) => {
    setConnectedWallet(address);
    setIsWalletModalOpen(false);
  };

  const handleWalletDisconnect = () => {
    setConnectedWallet(null);
  };

  const formatAddress = (address: string) => {
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  };

  return (
    <>
      <header className="sticky top-0 z-50 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b border-gunmetal">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2 group">
              <Bitcoin className="h-8 w-8 text-bitcoin transition-transform group-hover:rotate-12" />
              <span className="font-crypto text-xl font-bold glow-text">
                PredictPesa
              </span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center space-x-8">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`font-medium transition-smooth hover:text-cyber ${
                    isActive(item.href)
                      ? 'text-cyber glow'
                      : 'text-foreground'
                  }`}
                >
                  {item.name}
                </Link>
              ))}
            </nav>

            {/* Wallet Connection & Mobile Menu */}
            <div className="flex items-center space-x-4">
              {connectedWallet ? (
                <div className="hidden md:flex items-center space-x-2">
                  <div className="crypto-card py-2 px-3">
                    <span className="text-sm font-crypto text-cyber">
                      {formatAddress(connectedWallet)}
                    </span>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleWalletDisconnect}
                    className="border-destructive/50 text-destructive hover:bg-destructive/10"
                  >
                    Disconnect
                  </Button>
                </div>
              ) : (
                <Button
                  onClick={() => setIsWalletModalOpen(true)}
                  className="hidden md:flex crypto-button-primary"
                >
                  Connect Wallet
                </Button>
              )}

              {/* Mobile menu button */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="md:hidden"
              >
                {isMobileMenuOpen ? (
                  <X className="h-5 w-5" />
                ) : (
                  <Menu className="h-5 w-5" />
                )}
              </Button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {isMobileMenuOpen && (
            <div className="md:hidden py-4 animate-fade-in">
              <nav className="flex flex-col space-y-4">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    to={item.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={`font-medium transition-smooth hover:text-cyber ${
                      isActive(item.href)
                        ? 'text-cyber'
                        : 'text-foreground'
                    }`}
                  >
                    {item.name}
                  </Link>
                ))}
                
                {connectedWallet ? (
                  <div className="flex flex-col space-y-2 pt-4 border-t border-gunmetal">
                    <span className="text-sm text-cyber font-crypto">
                      {formatAddress(connectedWallet)}
                    </span>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleWalletDisconnect}
                      className="border-destructive/50 text-destructive hover:bg-destructive/10 w-fit"
                    >
                      Disconnect
                    </Button>
                  </div>
                ) : (
                  <Button
                    onClick={() => {
                      setIsWalletModalOpen(true);
                      setIsMobileMenuOpen(false);
                    }}
                    className="crypto-button-primary w-fit"
                  >
                    Connect Wallet
                  </Button>
                )}
              </nav>
            </div>
          )}
        </div>
      </header>

      <WalletConnectionModal
        isOpen={isWalletModalOpen}
        onClose={() => setIsWalletModalOpen(false)}
        onConnect={handleWalletConnect}
      />
    </>
  );
};

export default Header;