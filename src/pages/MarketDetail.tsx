import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Clock, Users, Bitcoin, TrendingUp, Info, Share2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import BettingModal from '@/components/modals/BettingModal';

const MarketDetail = () => {
  const { id } = useParams();
  const [isBettingModalOpen, setIsBettingModalOpen] = useState(false);
  const [selectedPosition, setSelectedPosition] = useState<'YES' | 'NO'>('YES');
  const [betAmount, setBetAmount] = useState('');
  const [showUSD, setShowUSD] = useState(false);

  // Mock market data - in real app this would come from API
  const market = {
    id: parseInt(id || '1'),
    question: "Will Nigeria's inflation rate exceed 25% by December 2025?",
    category: "Economics",
    region: "Nigeria",
    odds: { yes: 0.65, no: 0.35 },
    volume: "12.5 BTC",
    participants: 1247,
    endDate: "2025-12-31",
    description: "This market will resolve based on official inflation data published by the Central Bank of Nigeria (CBN). The market resolves to YES if the official inflation rate for any month in 2025 exceeds 25%, and NO otherwise.",
    creator: "0x1234...5678",
    timeLeft: "45 days, 12 hours",
    resolutionCriteria: [
      "Official CBN inflation data must be published",
      "Rate must exceed 25% for any single month in 2025",
      "Data must be from recognized financial institutions",
      "Resolution within 7 days of official announcement"
    ],
    priceHistory: [
      { time: '1w ago', yes: 0.58, no: 0.42 },
      { time: '6d ago', yes: 0.61, no: 0.39 },
      { time: '5d ago', yes: 0.63, no: 0.37 },
      { time: '4d ago', yes: 0.62, no: 0.38 },
      { time: '3d ago', yes: 0.64, no: 0.36 },
      { time: '2d ago', yes: 0.65, no: 0.35 },
      { time: '1d ago', yes: 0.66, no: 0.34 },
      { time: 'now', yes: 0.65, no: 0.35 }
    ]
  };

  const userPositions = [
    {
      position: "YES",
      amount: "0.1 BTC",
      currentValue: "0.12 BTC",
      pnl: "+0.02 BTC",
      pnlPercent: "+20%",
      tokens: "150 yesBTC"
    }
  ];

  const handlePlaceBet = (position: 'YES' | 'NO') => {
    setSelectedPosition(position);
    setIsBettingModalOpen(true);
  };

  const calculatePotentialReturns = () => {
    const amount = parseFloat(betAmount) || 0;
    if (amount === 0) return '0.00';
    
    const odds = selectedPosition === 'YES' ? market.odds.yes : market.odds.no;
    const potential = amount / odds;
    return potential.toFixed(4);
  };

  return (
    <>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back Button */}
        <Link to="/markets" className="inline-flex items-center text-cyber hover:text-cyber/80 mb-6">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Markets
        </Link>

        {/* Market Header */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <Card className="crypto-card mb-6">
              <CardContent className="p-6">
                <div className="flex flex-wrap gap-2 mb-4">
                  <Badge variant="outline">{market.category}</Badge>
                  <Badge variant="secondary">{market.region}</Badge>
                </div>
                
                <h1 className="text-2xl md:text-3xl font-crypto font-bold mb-4">
                  {market.question}
                </h1>
                
                <div className="grid grid-cols-3 gap-4 text-center mb-6">
                  <div>
                    <div className="flex items-center justify-center mb-1">
                      <Bitcoin className="h-4 w-4 text-bitcoin mr-1" />
                      <span className="text-sm text-muted-foreground">Volume</span>
                    </div>
                    <div className="font-crypto font-semibold text-bitcoin">{market.volume}</div>
                  </div>
                  
                  <div>
                    <div className="flex items-center justify-center mb-1">
                      <Users className="h-4 w-4 text-cyber mr-1" />
                      <span className="text-sm text-muted-foreground">Participants</span>
                    </div>
                    <div className="font-crypto font-semibold text-cyber">
                      {market.participants.toLocaleString()}
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex items-center justify-center mb-1">
                      <Clock className="h-4 w-4 text-gold mr-1" />
                      <span className="text-sm text-muted-foreground">Time Left</span>
                    </div>
                    <div className="font-crypto font-semibold text-gold">{market.timeLeft}</div>
                  </div>
                </div>

                <p className="text-muted-foreground">{market.description}</p>
              </CardContent>
            </Card>

            {/* Tabs for Details */}
            <Tabs defaultValue="overview" className="mb-6">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="analytics">Analytics</TabsTrigger>
                <TabsTrigger value="positions">My Positions</TabsTrigger>
              </TabsList>
              
              <TabsContent value="overview" className="mt-6">
                <Card className="crypto-card">
                  <CardHeader>
                    <CardTitle className="font-crypto">Resolution Criteria</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {market.resolutionCriteria.map((criteria, index) => (
                        <li key={index} className="flex items-start">
                          <Info className="h-4 w-4 text-cyber mt-1 mr-2 flex-shrink-0" />
                          <span className="text-sm">{criteria}</span>
                        </li>
                      ))}
                    </ul>
                    
                    <div className="mt-6 p-4 bg-dark-slate rounded-lg">
                      <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">Creator:</span>
                        <span className="font-crypto text-cyber">{market.creator}</span>
                      </div>
                      <div className="flex justify-between text-sm mt-2">
                        <span className="text-muted-foreground">End Date:</span>
                        <span>{new Date(market.endDate).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              
              <TabsContent value="analytics" className="mt-6">
                <Card className="crypto-card">
                  <CardHeader>
                    <CardTitle className="font-crypto">Price History</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {market.priceHistory.map((point, index) => (
                        <div key={index} className="flex justify-between items-center p-3 bg-dark-slate rounded-lg">
                          <span className="text-sm text-muted-foreground">{point.time}</span>
                          <div className="flex space-x-4">
                            <span className="text-success">YES {(point.yes * 100).toFixed(0)}%</span>
                            <span className="text-destructive">NO {(point.no * 100).toFixed(0)}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              
              <TabsContent value="positions" className="mt-6">
                <Card className="crypto-card">
                  <CardHeader>
                    <CardTitle className="font-crypto">Your Positions</CardTitle>
                  </CardHeader>
                  <CardContent>
                    {userPositions.length > 0 ? (
                      <div className="space-y-4">
                        {userPositions.map((position, index) => (
                          <div key={index} className="p-4 bg-dark-slate rounded-lg">
                            <div className="flex justify-between items-start mb-3">
                              <Badge variant={position.position === 'YES' ? 'default' : 'secondary'}>
                                {position.position}
                              </Badge>
                              <span className={`font-crypto ${
                                position.pnl.startsWith('+') ? 'text-success' : 'text-destructive'
                              }`}>
                                {position.pnl} ({position.pnlPercent})
                              </span>
                            </div>
                            
                            <div className="grid grid-cols-2 gap-4 text-sm">
                              <div>
                                <span className="text-muted-foreground">Staked:</span>
                                <div className="font-crypto text-bitcoin">{position.amount}</div>
                              </div>
                              <div>
                                <span className="text-muted-foreground">Current Value:</span>
                                <div className="font-crypto text-cyber">{position.currentValue}</div>
                              </div>
                              <div>
                                <span className="text-muted-foreground">Tokens:</span>
                                <div className="font-crypto">{position.tokens}</div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-center text-muted-foreground py-8">
                        You don't have any positions in this market yet.
                      </p>
                    )}
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>

          {/* Betting Panel */}
          <div className="lg:col-span-1">
            <Card className="crypto-card sticky top-24">
              <CardHeader>
                <CardTitle className="font-crypto text-xl">Place Your Bet</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Current Odds */}
                <div className="grid grid-cols-2 gap-3">
                  <Button
                    variant={selectedPosition === 'YES' ? 'default' : 'outline'}
                    onClick={() => setSelectedPosition('YES')}
                    className={`h-16 flex flex-col ${
                      selectedPosition === 'YES' 
                        ? 'bg-success hover:bg-success/90 text-black' 
                        : 'border-success/50 hover:border-success hover:bg-success/10'
                    }`}
                  >
                    <span className="font-crypto font-semibold">YES</span>
                    <span className="text-lg font-bold">
                      {(market.odds.yes * 100).toFixed(0)}%
                    </span>
                  </Button>
                  
                  <Button
                    variant={selectedPosition === 'NO' ? 'default' : 'outline'}
                    onClick={() => setSelectedPosition('NO')}
                    className={`h-16 flex flex-col ${
                      selectedPosition === 'NO' 
                        ? 'bg-destructive hover:bg-destructive/90' 
                        : 'border-destructive/50 hover:border-destructive hover:bg-destructive/10'
                    }`}
                  >
                    <span className="font-crypto font-semibold">NO</span>
                    <span className="text-lg font-bold">
                      {(market.odds.no * 100).toFixed(0)}%
                    </span>
                  </Button>
                </div>

                {/* Bet Amount */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <Label htmlFor="bet-amount">Bet Amount</Label>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm">BTC</span>
                      <Switch checked={showUSD} onCheckedChange={setShowUSD} />
                      <span className="text-sm">USD</span>
                    </div>
                  </div>
                  <Input
                    id="bet-amount"
                    type="number"
                    placeholder={showUSD ? "0.00 USD" : "0.00 BTC"}
                    value={betAmount}
                    onChange={(e) => setBetAmount(e.target.value)}
                    className="text-center font-crypto"
                  />
                  
                  <div className="grid grid-cols-4 gap-2">
                    {['0.01', '0.05', '0.1', '0.5'].map(amount => (
                      <Button
                        key={amount}
                        variant="outline"
                        size="sm"
                        onClick={() => setBetAmount(amount)}
                        className="text-xs"
                      >
                        {amount} BTC
                      </Button>
                    ))}
                  </div>
                </div>

                {/* Potential Returns */}
                <div className="p-4 bg-dark-slate rounded-lg">
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-muted-foreground">Potential Returns:</span>
                    <span className="font-crypto text-cyber">
                      {calculatePotentialReturns()} BTC
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Profit:</span>
                    <span className="font-crypto text-success">
                      +{(parseFloat(calculatePotentialReturns()) - (parseFloat(betAmount) || 0)).toFixed(4)} BTC
                    </span>
                  </div>
                </div>

                {/* Place Bet Button */}
                <Button
                  onClick={() => handlePlaceBet(selectedPosition)}
                  disabled={!betAmount || parseFloat(betAmount) <= 0}
                  className="crypto-button-primary w-full h-12 text-lg"
                >
                  <TrendingUp className="mr-2 h-5 w-5" />
                  Bet {selectedPosition}
                </Button>

                {/* Share Button */}
                <Button variant="outline" className="w-full">
                  <Share2 className="mr-2 h-4 w-4" />
                  Share Market
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      <BettingModal
        isOpen={isBettingModalOpen}
        onClose={() => setIsBettingModalOpen(false)}
        market={market}
        position={selectedPosition}
        amount={betAmount}
      />
    </>
  );
};

export default MarketDetail;