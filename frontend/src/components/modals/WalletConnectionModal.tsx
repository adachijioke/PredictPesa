import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Wallet, Shield, Smartphone, Globe } from 'lucide-react';

interface WalletConnectionModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConnect: (address: string) => void;
}

const WalletConnectionModal = ({ isOpen, onClose, onConnect }: WalletConnectionModalProps) => {
  const walletOptions = [
    {
      name: 'MetaMask',
      icon: Wallet,
      description: 'Connect using MetaMask browser extension',
      color: 'text-bitcoin',
      onClick: () => handleWalletConnection('metamask')
    },
    {
      name: 'HashPack',
      icon: Shield,
      description: 'Hedera native wallet for HTS tokens',
      color: 'text-cyber',
      onClick: () => handleWalletConnection('hashpack')
    },
    {
      name: 'WalletConnect',
      icon: Smartphone,
      description: 'Connect with mobile wallets via QR code',
      color: 'text-success',
      onClick: () => handleWalletConnection('walletconnect')
    },
    {
      name: 'Browser Wallet',
      icon: Globe,
      description: 'Other browser-based wallets',
      color: 'text-gold',
      onClick: () => handleWalletConnection('browser')
    }
  ];

  const handleWalletConnection = async (walletType: string) => {
    if (walletType === 'browser') {
      // Detect and connect to browser wallets
      if (typeof window !== 'undefined') {
        try {
          // Check for various wallet providers
          if ((window as any).ethereum) {
            const provider = (window as any).ethereum;
            const accounts = await provider.request({ method: 'eth_requestAccounts' });
            if (accounts.length > 0) {
              onConnect(accounts[0]);
              return;
            }
          }
          
          // If no wallets detected, show mock connection
          setTimeout(() => {
            onConnect('0x9876...5432');
          }, 1000);
        } catch (error) {
          console.error('Error connecting to browser wallet:', error);
          // Fallback to mock connection
          setTimeout(() => {
            onConnect('0x9876...5432');
          }, 1000);
        }
      }
    } else {
      // Simulate wallet connection with different addresses
      const mockAddresses = {
        metamask: '0x1234...5678',
        hashpack: '0.0.123456',
        walletconnect: '0xabcd...efgh',
        browser: '0x9876...5432'
      };
      
      // Simulate connection delay
      setTimeout(() => {
        onConnect(mockAddresses[walletType as keyof typeof mockAddresses]);
      }, 1000);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="bg-gunmetal border border-charcoal max-w-md">
        <DialogHeader>
          <DialogTitle className="font-crypto text-xl text-bitcoin text-center">
            Connect Your Wallet
          </DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4 mt-6">
          <p className="text-center text-muted-foreground text-sm">
            Choose your preferred wallet to connect to PredictPesa
          </p>
          
          <div className="space-y-3">
            {walletOptions.map((wallet) => (
              <Button
                key={wallet.name}
                onClick={wallet.onClick}
                variant="outline"
                className="w-full h-auto p-4 crypto-card hover:border-primary/50 group"
              >
                <div className="flex items-center space-x-4 w-full">
                  <wallet.icon className={`h-8 w-8 ${wallet.color} group-hover:scale-110 transition-transform`} />
                  <div className="flex-1 text-left">
                    <div className="font-crypto font-medium">{wallet.name}</div>
                    <div className="text-sm text-muted-foreground">{wallet.description}</div>
                  </div>
                </div>
              </Button>
            ))}
          </div>
          
          <div className="mt-6 p-4 bg-dark-slate rounded-lg border border-border">
            <p className="text-xs text-muted-foreground text-center">
              By connecting a wallet, you agree to our Terms of Service and Privacy Policy.
              Your wallet will be used to stake Bitcoin and trade prediction tokens.
            </p>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default WalletConnectionModal;