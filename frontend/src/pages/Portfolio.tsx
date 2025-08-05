import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Bitcoin, TrendingUp, TrendingDown, Eye, ArrowRight, Download } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

const Portfolio = () => {
  const [selectedTab, setSelectedTab] = useState('active');

  const portfolioStats = {
    totalValue: '2.45',
    totalValueUSD: '$98,000',
    unrealizedPnL: '+0.23',
    realizedPnL: '+1.12',
    successRate: '67%',
    totalTrades: 45,
    activePositions: 8,
    winningPositions: 5,
    losingPositions: 1,
    breakEvenPositions: 2
  };

  const activePositions = [
    {
      id: 1,
      market: "Will Nigeria's inflation exceed 25% by Dec 2025?",
      position: "YES",
      amount: "0.1 BTC",
      currentValue: "0.12 BTC",
      pnl: "+0.02 BTC",
      pnlPercent: "+20%",
      status: "winning",
      tokens: "150 yesBTC",
      odds: "65%",
      timeLeft: "45 days"
    },
    {
      id: 2,
      market: "Will Super Eagles qualify for 2026 World Cup?",
      position: "YES",
      amount: "0.05 BTC",
      currentValue: "0.048 BTC",
      pnl: "-0.002 BTC",
      pnlPercent: "-4%",
      status: "losing",
      tokens: "78 yesBTC",
      odds: "78%",
      timeLeft: "120 days"
    },
    {
      id: 3,
      market: "Will Bitcoin reach $150,000 by end of 2025?",
      position: "NO",
      amount: "0.2 BTC",
      currentValue: "0.21 BTC",
      pnl: "+0.01 BTC",
      pnlPercent: "+5%",
      status: "winning",
      tokens: "200 noBTC",
      odds: "58%",
      timeLeft: "280 days"
    }
  ];

  const positionHistory = [
    {
      id: 1,
      market: "Kenya Election Results 2024",
      position: "YES",
      amount: "0.15 BTC",
      finalValue: "0.25 BTC",
      pnl: "+0.10 BTC",
      pnlPercent: "+67%",
      status: "won",
      resolvedDate: "2024-08-15",
      outcome: "Correct prediction"
    },
    {
      id: 2,
      market: "Ghana GDP Growth Q3 2024",
      position: "NO",
      amount: "0.08 BTC",
      finalValue: "0.00 BTC",
      pnl: "-0.08 BTC",
      pnlPercent: "-100%",
      status: "lost",
      resolvedDate: "2024-10-20",
      outcome: "Incorrect prediction"
    }
  ];

  const tokenBalances = [
    { token: "yesBTC", balance: "428", value: "0.32 BTC", apy: "12.5%" },
    { token: "noBTC", balance: "200", value: "0.21 BTC", apy: "8.7%" },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'winning':
      case 'won':
        return 'text-success';
      case 'losing':
      case 'lost':
        return 'text-destructive';
      default:
        return 'text-muted-foreground';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'winning':
      case 'won':
        return <TrendingUp className="h-4 w-4 text-success" />;
      case 'losing':
      case 'lost':
        return <TrendingDown className="h-4 w-4 text-destructive" />;
      default:
        return null;
    }
  };

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl md:text-4xl font-crypto font-bold">
          Your <span className="glow-text">Portfolio</span>
        </h1>
        <Button variant="outline" className="crypto-button-secondary">
          <Download className="mr-2 h-4 w-4" />
          Export Data
        </Button>
      </div>

      {/* Portfolio Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card className="stats-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Value</p>
                <p className="text-2xl font-crypto font-bold text-bitcoin">
                  ₿{portfolioStats.totalValue}
                </p>
                <p className="text-sm text-muted-foreground">{portfolioStats.totalValueUSD}</p>
              </div>
              <Bitcoin className="h-8 w-8 text-bitcoin" />
            </div>
          </CardContent>
        </Card>

        <Card className="stats-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Unrealized P&L</p>
                <p className="text-2xl font-crypto font-bold text-success">
                  {portfolioStats.unrealizedPnL} BTC
                </p>
                <p className="text-sm text-muted-foreground">{portfolioStats.activePositions} positions</p>
              </div>
              <TrendingUp className="h-8 w-8 text-success" />
            </div>
          </CardContent>
        </Card>

        <Card className="stats-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Realized P&L</p>
                <p className="text-2xl font-crypto font-bold text-cyber">
                  {portfolioStats.realizedPnL} BTC
                </p>
                <p className="text-sm text-muted-foreground">All time</p>
              </div>
              <TrendingUp className="h-8 w-8 text-cyber" />
            </div>
          </CardContent>
        </Card>

        <Card className="stats-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Success Rate</p>
                <p className="text-2xl font-crypto font-bold text-gold">
                  {portfolioStats.successRate}
                </p>
                <p className="text-sm text-muted-foreground">{portfolioStats.totalTrades} trades</p>
              </div>
              <TrendingUp className="h-8 w-8 text-gold" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Portfolio Tabs */}
      <Tabs value={selectedTab} onValueChange={setSelectedTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="active">Active Positions</TabsTrigger>
          <TabsTrigger value="history">Position History</TabsTrigger>
          <TabsTrigger value="tokens">Token Balances</TabsTrigger>
        </TabsList>

        <TabsContent value="active" className="mt-6">
          <div className="space-y-4">
            {activePositions.map((position) => (
              <Card key={position.id} className="market-card">
                <CardContent className="p-6">
                  <div className="flex flex-col md:flex-row md:items-center justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <Badge variant={position.position === 'YES' ? 'default' : 'secondary'}>
                          {position.position}
                        </Badge>
                        <span className="text-sm text-muted-foreground">
                          {position.odds} odds
                        </span>
                      </div>
                      <h3 className="font-medium text-foreground mb-2">
                        {position.market}
                      </h3>
                      <p className="text-sm text-muted-foreground">
                        Ends in {position.timeLeft}
                      </p>
                    </div>
                    
                    <div className="flex items-center space-x-4 mt-4 md:mt-0">
                      {getStatusIcon(position.status)}
                      <div className="text-right">
                        <div className={`font-crypto font-semibold ${getStatusColor(position.status)}`}>
                          {position.pnl} ({position.pnlPercent})
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {position.currentValue} current
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 text-sm">
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
                    <div>
                      <span className="text-muted-foreground">Status:</span>
                      <div className={`font-crypto capitalize ${getStatusColor(position.status)}`}>
                        {position.status}
                      </div>
                    </div>
                  </div>

                  <div className="flex space-x-3">
                    <Link to={`/markets/${position.id}`}>
                      <Button variant="outline" size="sm">
                        <Eye className="mr-2 h-4 w-4" />
                        View Market
                      </Button>
                    </Link>
                    <Button variant="outline" size="sm">
                      Sell Position
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="history" className="mt-6">
          <div className="space-y-4">
            {positionHistory.map((position) => (
              <Card key={position.id} className="crypto-card">
                <CardContent className="p-6">
                  <div className="flex flex-col md:flex-row md:items-center justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <Badge variant={position.position === 'YES' ? 'default' : 'secondary'}>
                          {position.position}
                        </Badge>
                        <Badge variant="outline" className="text-xs">
                          Resolved
                        </Badge>
                      </div>
                      <h3 className="font-medium text-foreground mb-2">
                        {position.market}
                      </h3>
                      <p className="text-sm text-muted-foreground">
                        Resolved on {new Date(position.resolvedDate).toLocaleDateString()}
                      </p>
                    </div>
                    
                    <div className="flex items-center space-x-4 mt-4 md:mt-0">
                      {getStatusIcon(position.status)}
                      <div className="text-right">
                        <div className={`font-crypto font-semibold ${getStatusColor(position.status)}`}>
                          {position.pnl} ({position.pnlPercent})
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {position.finalValue} final
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                    <div>
                      <span className="text-muted-foreground">Staked:</span>
                      <div className="font-crypto text-bitcoin">{position.amount}</div>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Final Value:</span>
                      <div className="font-crypto text-cyber">{position.finalValue}</div>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Outcome:</span>
                      <div className="font-crypto">{position.outcome}</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="tokens" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {tokenBalances.map((token) => (
              <Card key={token.token} className="crypto-card">
                <CardHeader>
                  <CardTitle className="font-crypto text-xl flex items-center justify-between">
                    {token.token}
                    <Badge variant="outline" className="text-xs">
                      {token.apy} APY
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-muted-foreground">Balance:</span>
                    <span className="font-crypto text-2xl font-bold text-cyber">
                      {token.balance}
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-muted-foreground">Value:</span>
                    <span className="font-crypto text-lg text-bitcoin">
                      {token.value}
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-muted-foreground">Yield Earning:</span>
                    <span className="font-crypto text-success">
                      {token.apy}
                    </span>
                  </div>
                  
                  <div className="flex space-x-3 pt-4">
                    <Button variant="outline" size="sm" className="flex-1">
                      Trade
                    </Button>
                    <Button className="crypto-button-primary flex-1">
                      <ArrowRight className="mr-2 h-4 w-4" />
                      Stake More
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Portfolio;