import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, SortAsc, Clock, Users, Bitcoin, TrendingUp, ArrowUpRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const Markets = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedRegion, setSelectedRegion] = useState('all');
  const [sortBy, setSortBy] = useState('popular');

  const categories = ['All', 'Economics', 'Sports', 'Politics', 'Weather', 'Crypto', 'Technology'];
  const regions = ['All', 'Nigeria', 'Kenya', 'Ghana', 'South Africa', 'Global'];

  const markets = [
    {
      id: 1,
      question: "Will Nigeria's inflation rate exceed 25% by December 2025?",
      category: "Economics",
      region: "Nigeria",
      odds: { yes: 0.65, no: 0.35 },
      volume: "12.5 BTC",
      participants: 1247,
      endDate: "2025-12-31",
      description: "Based on official CBN inflation data",
      trend: "up",
      timeLeft: "45 days"
    },
    {
      id: 2,
      question: "Will Super Eagles qualify for 2026 World Cup?",
      category: "Sports",
      region: "Nigeria",
      odds: { yes: 0.78, no: 0.22 },
      volume: "8.3 BTC",
      participants: 892,
      endDate: "2025-11-20",
      trend: "stable",
      timeLeft: "120 days"
    },
    {
      id: 3,
      question: "Will Bitcoin reach $150,000 by end of 2025?",
      category: "Crypto",
      region: "Global",
      odds: { yes: 0.42, no: 0.58 },
      volume: "45.2 BTC",
      participants: 3421,
      endDate: "2025-12-31",
      trend: "up",
      timeLeft: "280 days"
    },
    {
      id: 4,
      question: "Will Kenya's GDP grow by more than 6% in 2025?",
      category: "Economics",
      region: "Kenya",
      odds: { yes: 0.55, no: 0.45 },
      volume: "6.7 BTC",
      participants: 567,
      endDate: "2025-12-31",
      trend: "stable",
      timeLeft: "310 days"
    },
    {
      id: 5,
      question: "Will it rain more than 100mm in Lagos in March 2025?",
      category: "Weather",
      region: "Nigeria",
      odds: { yes: 0.73, no: 0.27 },
      volume: "3.2 BTC",
      participants: 234,
      endDate: "2025-03-31",
      trend: "down",
      timeLeft: "85 days"
    },
    {
      id: 6,
      question: "Will Ghana's cedi strengthen against USD by 10% in 2025?",
      category: "Economics",
      region: "Ghana",
      odds: { yes: 0.31, no: 0.69 },
      volume: "4.8 BTC",
      participants: 445,
      endDate: "2025-12-31",
      trend: "up",
      timeLeft: "320 days"
    }
  ];

  const filteredMarkets = markets.filter(market => {
    const matchesSearch = market.question.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || market.category.toLowerCase() === selectedCategory;
    const matchesRegion = selectedRegion === 'all' || market.region.toLowerCase() === selectedRegion;
    
    return matchesSearch && matchesCategory && matchesRegion;
  });

  const sortedMarkets = [...filteredMarkets].sort((a, b) => {
    switch (sortBy) {
      case 'newest':
        return new Date(b.endDate).getTime() - new Date(a.endDate).getTime();
      case 'ending-soon':
        return new Date(a.endDate).getTime() - new Date(b.endDate).getTime();
      case 'volume':
        return parseFloat(b.volume) - parseFloat(a.volume);
      default: // popular
        return b.participants - a.participants;
    }
  });

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl md:text-4xl font-crypto font-bold mb-4">
          Prediction <span className="glow-text">Markets</span>
        </h1>
        <p className="text-muted-foreground text-lg">
          Stake Bitcoin on real-world outcomes across Africa and beyond
        </p>
      </div>

      {/* Filters */}
      <div className="bg-gunmetal p-6 rounded-lg border border-charcoal mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {/* Search */}
          <div className="lg:col-span-2">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search markets..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>

          {/* Category Filter */}
          <Select value={selectedCategory} onValueChange={setSelectedCategory}>
            <SelectTrigger>
              <Filter className="h-4 w-4 mr-2" />
              <SelectValue placeholder="Category" />
            </SelectTrigger>
            <SelectContent>
              {categories.map(category => (
                <SelectItem key={category} value={category.toLowerCase()}>
                  {category}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Region Filter */}
          <Select value={selectedRegion} onValueChange={setSelectedRegion}>
            <SelectTrigger>
              <SelectValue placeholder="Region" />
            </SelectTrigger>
            <SelectContent>
              {regions.map(region => (
                <SelectItem key={region} value={region.toLowerCase()}>
                  {region}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Sort */}
          <Select value={sortBy} onValueChange={setSortBy}>
            <SelectTrigger>
              <SortAsc className="h-4 w-4 mr-2" />
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="popular">Popular</SelectItem>
              <SelectItem value="newest">Newest</SelectItem>
              <SelectItem value="ending-soon">Ending Soon</SelectItem>
              <SelectItem value="volume">Highest Volume</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Results Count */}
      <div className="flex justify-between items-center mb-6">
        <p className="text-muted-foreground">
          Showing {sortedMarkets.length} markets
        </p>
        <Link to="/create-market">
          <Button className="crypto-button-primary">
            Create Market
          </Button>
        </Link>
      </div>

      {/* Markets Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sortedMarkets.map((market, index) => (
          <Link key={market.id} to={`/markets/${market.id}`}>
            <Card className="market-card animate-fade-in" style={{ animationDelay: `${index * 50}ms` }}>
              <CardContent className="p-6">
                {/* Header */}
                <div className="flex justify-between items-start mb-4">
                  <div className="flex space-x-2">
                    <Badge variant="outline" className="text-xs">
                      {market.category}
                    </Badge>
                    <Badge variant="secondary" className="text-xs">
                      {market.region}
                    </Badge>
                  </div>
                  {market.trend === 'up' && (
                    <ArrowUpRight className="h-4 w-4 text-success" />
                  )}
                </div>

                {/* Question */}
                <h3 className="font-medium text-foreground mb-4 group-hover:text-cyber transition-smooth">
                  {market.question}
                </h3>

                {/* Odds */}
                <div className="grid grid-cols-2 gap-3 mb-4">
                  <div className="bg-success/10 border border-success/20 rounded-lg p-3 text-center">
                    <div className="text-success font-crypto font-semibold">YES</div>
                    <div className="text-success text-lg font-bold">
                      {(market.odds.yes * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-3 text-center">
                    <div className="text-destructive font-crypto font-semibold">NO</div>
                    <div className="text-destructive text-lg font-bold">
                      {(market.odds.no * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>

                {/* Stats */}
                <div className="flex justify-between items-center text-sm text-muted-foreground mb-4">
                  <div className="flex items-center space-x-1">
                    <Bitcoin className="h-4 w-4 text-bitcoin" />
                    <span>{market.volume}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Users className="h-4 w-4" />
                    <span>{market.participants.toLocaleString()}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Clock className="h-4 w-4" />
                    <span>{market.timeLeft}</span>
                  </div>
                </div>

                {/* Action Button */}
                <Button className="crypto-button-primary w-full group-hover:glow">
                  <TrendingUp className="mr-2 h-4 w-4" />
                  Bet Now
                </Button>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      {/* Load More */}
      {sortedMarkets.length > 0 && (
        <div className="text-center mt-8">
          <Button variant="outline" className="crypto-button-secondary">
            Load More Markets
          </Button>
        </div>
      )}

      {/* No Results */}
      {sortedMarkets.length === 0 && (
        <div className="text-center py-12">
          <p className="text-muted-foreground text-lg mb-4">
            No markets found matching your criteria
          </p>
          <Button onClick={() => {
            setSearchQuery('');
            setSelectedCategory('all');
            setSelectedRegion('all');
          }} variant="outline">
            Clear Filters
          </Button>
        </div>
      )}
    </div>
  );
};

export default Markets;