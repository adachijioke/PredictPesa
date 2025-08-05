import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Bitcoin, TrendingUp, Target, Award, Plus, Eye, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const Dashboard = () => {
  const [connectedWallet] = useState('0x1234...5678'); // Mock connected state
  
  const portfolioStats = {
    totalValue: '2.45',
    totalValueUSD: '$98,000',
    unrealizedPnL: '+0.23',
    realizedPnL: '+1.12',
    successRate: '67%',
    totalTrades: 45
  };

  const trendingMarkets = [
    {
      id: 1,
      question: "Will Nigeria's inflation rate exceed 25% by December 2025?",
      category: "Economics",
      odds: { yes: 0.65, no: 0.35 },
      volume: "12.5 BTC",
      timeLeft: "45 days",
      trend: "up"
    },
    {
      id: 2,
      question: "Will Super Eagles qualify for 2026 World Cup?",
      category: "Sports",
      odds: { yes: 0.78, no: 0.22 },
      volume: "8.3 BTC",
      timeLeft: "120 days",
      trend: "stable"
    },
    {
      id: 3,
      question: "Will Bitcoin reach $150,000 by end of 2025?",
      category: "Crypto",
      odds: { yes: 0.42, no: 0.58 },
      volume: "45.2 BTC",
      timeLeft: "280 days",
      trend: "up"
    }
  ];

  const recentActivity = [
    {
      id: 1,
      type: 'bet',
      market: "Nigeria GDP Growth 2025",
      position: "YES",
      amount: "0.1 BTC",
      status: "winning",
      pnl: "+0.02 BTC",
      time: "2 hours ago"
    },
    {
      id: 2,
      type: 'claim',
      market: "Kenya Election Results",
      amount: "0.15 BTC",
      status: "completed",
      time: "1 day ago"
    },
    {
      id: 3,
      type: 'bet',
      market: "South Africa Interest Rates",
      position: "NO",
      amount: "0.05 BTC",
      status: "losing",
      pnl: "-0.01 BTC",
      time: "3 days ago"
    }
  ];

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Welcome Section */}
      <div className="mb-8">
        <h1 className="text-3xl md:text-4xl font-crypto font-bold mb-4">
          Welcome back to <span className="glow-text">PredictPesa</span>
        </h1>
        {connectedWallet && (
          <p className="text-muted-foreground">
            Connected wallet: <span className="text-cyber font-crypto">{connectedWallet}</span>
          </p>
        )}
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
                <p className="text-sm text-muted-foreground">Active Positions</p>
                <p className="text-2xl font-crypto font-bold text-cyber">8</p>
                <p className="text-sm text-success">P&L: {portfolioStats.unrealizedPnL} BTC</p>
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
                <p className="text-2xl font-crypto font-bold text-success">{portfolioStats.successRate}</p>
                <p className="text-sm text-muted-foreground">{portfolioStats.totalTrades} trades</p>
              </div>
              <Target className="h-8 w-8 text-success" />
            </div>
          </CardContent>
        </Card>

        <Card className="stats-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Winnings</p>
                <p className="text-2xl font-crypto font-bold text-gold">₿{portfolioStats.realizedPnL}</p>
                <p className="text-sm text-success">All time</p>
              </div>
              <Award className="h-8 w-8 text-gold" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <Link to="/markets">
          <Button className="crypto-button-primary w-full h-16 text-lg">
            <Plus className="mr-2 h-5 w-5" />
            Create New Bet
          </Button>
        </Link>
        
        <Link to="/markets">
          <Button className="crypto-button-secondary w-full h-16 text-lg">
            <Eye className="mr-2 h-5 w-5" />
            View All Markets
          </Button>
        </Link>
        
        <Link to="/rewards">
          <Button className="crypto-button-gold w-full h-16 text-lg">
            <Award className="mr-2 h-5 w-5" />
            Check Rewards
          </Button>
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Trending Markets */}
        <Card className="crypto-card">
          <CardHeader>
            <CardTitle className="font-crypto text-xl">Trending Markets</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {trendingMarkets.map((market) => (
              <Link key={market.id} to={`/markets/${market.id}`}>
                <div className="p-4 bg-dark-slate rounded-lg border border-border hover:border-primary/30 transition-smooth cursor-pointer group">
                  <div className="flex justify-between items-start mb-3">
                    <Badge variant="outline" className="text-xs">{market.category}</Badge>
                    <div className="flex items-center text-xs text-muted-foreground">
                      {market.trend === 'up' ? (
                        <ArrowUpRight className="h-3 w-3 text-success mr-1" />
                      ) : (
                        <ArrowDownRight className="h-3 w-3 text-muted-foreground mr-1" />
                      )}
                      {market.volume}
                    </div>
                  </div>
                  
                  <h4 className="font-medium mb-3 group-hover:text-cyber transition-smooth">
                    {market.question}
                  </h4>
                  
                  <div className="flex justify-between items-center text-sm">
                    <div className="flex space-x-4">
                      <span className="text-success">YES {(market.odds.yes * 100).toFixed(0)}%</span>
                      <span className="text-destructive">NO {(market.odds.no * 100).toFixed(0)}%</span>
                    </div>
                    <span className="text-muted-foreground">{market.timeLeft}</span>
                  </div>
                </div>
              </Link>
            ))}
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card className="crypto-card">
          <CardHeader>
            <CardTitle className="font-crypto text-xl">Recent Activity</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="p-4 bg-dark-slate rounded-lg border border-border">
                <div className="flex justify-between items-start mb-2">
                  <Badge 
                    variant={activity.type === 'bet' ? 'default' : 'secondary'}
                    className="text-xs"
                  >
                    {activity.type.toUpperCase()}
                  </Badge>
                  <span className="text-xs text-muted-foreground">{activity.time}</span>
                </div>
                
                <h4 className="font-medium mb-2">{activity.market}</h4>
                
                <div className="flex justify-between items-center text-sm">
                  <div className="flex items-center space-x-2">
                    {activity.position && (
                      <Badge variant="outline" className="text-xs">
                        {activity.position}
                      </Badge>
                    )}
                    <span className="text-bitcoin">{activity.amount}</span>
                  </div>
                  
                  {activity.pnl && (
                    <span className={`font-crypto ${
                      activity.status === 'winning' 
                        ? 'text-success' 
                        : activity.status === 'losing' 
                        ? 'text-destructive' 
                        : 'text-muted-foreground'
                    }`}>
                      {activity.pnl}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;