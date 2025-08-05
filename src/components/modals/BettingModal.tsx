import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, AlertCircle, Loader2, TrendingUp } from 'lucide-react';

interface BettingModalProps {
  isOpen: boolean;
  onClose: () => void;
  market: {
    question: string;
    odds: { yes: number; no: number };
  };
  position: 'YES' | 'NO';
  amount: string;
}

const BettingModal = ({ isOpen, onClose, market, position, amount }: BettingModalProps) => {
  const [step, setStep] = useState<'confirm' | 'processing' | 'success' | 'error'>('confirm');
  const [transactionHash, setTransactionHash] = useState('');

  const odds = position === 'YES' ? market.odds.yes : market.odds.no;
  const potentialReturn = (parseFloat(amount) || 0) / odds;
  const profit = potentialReturn - (parseFloat(amount) || 0);

  const handleConfirmBet = async () => {
    setStep('processing');
    
    // Simulate transaction processing
    setTimeout(() => {
      const mockTxHash = `0x${Math.random().toString(16).substr(2, 64)}`;
      setTransactionHash(mockTxHash);
      setStep('success');
    }, 3000);
  };

  const handleClose = () => {
    setStep('confirm');
    setTransactionHash('');
    onClose();
  };

  const renderContent = () => {
    switch (step) {
      case 'confirm':
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-crypto mb-2">Confirm Your Bet</h3>
              <p className="text-muted-foreground text-sm">
                Review your bet details before confirming the transaction
              </p>
            </div>

            <div className="p-4 bg-dark-slate rounded-lg border border-border">
              <h4 className="font-medium mb-3">{market.question}</h4>
              
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Position:</span>
                  <Badge variant={position === 'YES' ? 'default' : 'secondary'}>
                    {position}
                  </Badge>
                </div>
                
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Bet Amount:</span>
                  <span className="font-crypto text-bitcoin">{amount} BTC</span>
                </div>
                
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Current Odds:</span>
                  <span className="font-crypto">{(odds * 100).toFixed(0)}%</span>
                </div>
                
                <div className="border-t border-border pt-3">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Potential Return:</span>
                    <span className="font-crypto text-cyber">{potentialReturn.toFixed(4)} BTC</span>
                  </div>
                  
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Potential Profit:</span>
                    <span className="font-crypto text-success">+{profit.toFixed(4)} BTC</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="p-4 bg-charcoal/50 rounded-lg border border-warning/20">
              <div className="flex items-start space-x-3">
                <AlertCircle className="h-5 w-5 text-warning mt-0.5 flex-shrink-0" />
                <div className="text-sm">
                  <p className="text-warning font-medium mb-1">Important:</p>
                  <p className="text-muted-foreground">
                    This transaction will stake your Bitcoin. You'll receive {position.toLowerCase()}BTC tokens
                    that can be traded before market resolution.
                  </p>
                </div>
              </div>
            </div>

            <div className="flex space-x-3">
              <Button variant="outline" onClick={handleClose} className="flex-1">
                Cancel
              </Button>
              <Button onClick={handleConfirmBet} className="crypto-button-primary flex-1">
                <TrendingUp className="mr-2 h-4 w-4" />
                Confirm Bet
              </Button>
            </div>
          </div>
        );

      case 'processing':
        return (
          <div className="text-center space-y-6">
            <div className="flex justify-center">
              <Loader2 className="h-16 w-16 text-cyber animate-spin" />
            </div>
            
            <div>
              <h3 className="text-lg font-crypto mb-2">Processing Transaction</h3>
              <p className="text-muted-foreground">
                Please wait while your bet is being processed on the blockchain...
              </p>
            </div>
            
            <div className="p-4 bg-dark-slate rounded-lg">
              <div className="text-sm space-y-2">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Position:</span>
                  <span className="text-cyber">{position}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Amount:</span>
                  <span className="text-bitcoin">{amount} BTC</span>
                </div>
              </div>
            </div>
          </div>
        );

      case 'success':
        return (
          <div className="text-center space-y-6">
            <div className="flex justify-center">
              <CheckCircle className="h-16 w-16 text-success" />
            </div>
            
            <div>
              <h3 className="text-lg font-crypto mb-2 text-success">Bet Placed Successfully!</h3>
              <p className="text-muted-foreground">
                Your bet has been confirmed and your tokens have been minted.
              </p>
            </div>
            
            <div className="p-4 bg-dark-slate rounded-lg">
              <div className="text-sm space-y-2">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Transaction Hash:</span>
                  <span className="text-cyber font-crypto text-xs break-all">
                    {transactionHash.slice(0, 10)}...{transactionHash.slice(-8)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Tokens Received:</span>
                  <span className="text-success font-crypto">
                    {(parseFloat(amount) * 100).toFixed(0)} {position.toLowerCase()}BTC
                  </span>
                </div>
              </div>
            </div>

            <div className="flex space-x-3">
              <Button variant="outline" onClick={handleClose} className="flex-1">
                Close
              </Button>
              <Button 
                onClick={() => window.open('/portfolio', '_blank')}
                className="crypto-button-primary flex-1"
              >
                View Portfolio
              </Button>
            </div>
          </div>
        );

      case 'error':
        return (
          <div className="text-center space-y-6">
            <div className="flex justify-center">
              <AlertCircle className="h-16 w-16 text-destructive" />
            </div>
            
            <div>
              <h3 className="text-lg font-crypto mb-2 text-destructive">Transaction Failed</h3>
              <p className="text-muted-foreground">
                Your bet could not be processed. Please try again.
              </p>
            </div>
            
            <div className="flex space-x-3">
              <Button variant="outline" onClick={handleClose} className="flex-1">
                Close
              </Button>
              <Button onClick={() => setStep('confirm')} className="crypto-button-primary flex-1">
                Try Again
              </Button>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={step === 'processing' ? undefined : handleClose}>
      <DialogContent className="bg-gunmetal border border-charcoal max-w-md">
        <DialogHeader>
          <DialogTitle className="font-crypto text-xl text-center">
            {step === 'confirm' && 'Place Bet'}
            {step === 'processing' && 'Processing...'}
            {step === 'success' && 'Success!'}
            {step === 'error' && 'Error'}
          </DialogTitle>
        </DialogHeader>
        
        {renderContent()}
      </DialogContent>
    </Dialog>
  );
};

export default BettingModal;