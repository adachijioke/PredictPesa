import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Bitcoin, TrendingUp, Shield, Zap, Globe } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import WalletConnectionModal from '@/components/modals/WalletConnectionModal';
import CountUpStat from '@/components/ui/CountUpStat';
import Footer from '@/components/layout/Footer';
import heroAfricaMap from '@/assets/hero-africa-map.jpg';
import africaGlobe from '@/assets/africa-globe.jpg';
import cryptoCityscape from '@/assets/crypto-cityscape.jpg';

const Home = () => {
  const [isWalletModalOpen, setIsWalletModalOpen] = useState(false);

  const features = [
    {
      icon: Bitcoin,
      title: 'Bitcoin-Native Staking',
      description: 'Stake Bitcoin directly on prediction markets powered by Hedera hashgraph technology.',
      color: 'text-bitcoin'
    },
    {
      icon: TrendingUp,
      title: 'Trade Your Beliefs',
      description: 'Convert predictions into tradeable yesBTC and noBTC tokens. Exit positions anytime.',
      color: 'text-cyber'
    },
    {
      icon: Shield,
      title: 'AI-Powered Resolution',
      description: 'Advanced AI oracles ensure fair and accurate market resolution from trusted data sources.',
      color: 'text-success'
    },
    {
      icon: Globe,
      title: 'Africa-Focused Markets',
      description: 'Predict outcomes across African economies, politics, weather, and cultural events.',
      color: 'text-gold'
    }
  ];

  const stats = [
    { label: 'Total Volume', value: '₿2,847', change: '+23.4%' },
    { label: 'Active Markets', value: '156', change: '+12' },
    { label: 'Participants', value: '12,847', change: '+8.7%' },
    { label: 'Success Rate', value: '73.2%', change: '+2.1%' }
  ];

  const handleWalletConnect = (address: string) => {
    setIsWalletModalOpen(false);
    // Redirect to dashboard after connection
    setTimeout(() => {
      window.location.href = '/dashboard';
    }, 1000);
  };

  return (
    <>
      <div className="min-h-screen">
        {/* Hero Section */}
        <section 
          className="relative min-h-screen flex items-center justify-center bg-cover bg-center bg-no-repeat"
          style={{ backgroundImage: `url(${heroAfricaMap})` }}
        >
          <div className="absolute inset-0 bg-black/60"></div>
          <div className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div className="max-w-4xl mx-auto animate-fade-in">
              <h1 className="text-4xl md:text-6xl lg:text-7xl font-crypto font-bold mb-6">
                Stake Bitcoin.{' '}
                <span className="glow-text">Forecast Everything.</span>{' '}
                Trade Your Belief.
              </h1>
              
              <p className="text-xl md:text-2xl text-foreground/90 mb-8 max-w-3xl mx-auto">
                An on-chain prediction market powered by AI, Hedera, and DeFi. 
                Forecast elections, FX rates, food prices, and more across Africa.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <Link to="/markets">
                  <Button className="crypto-button-primary text-lg px-8 py-4">
                    Explore Markets
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
                
                <Button 
                  onClick={() => setIsWalletModalOpen(true)}
                  variant="outline"
                  className="crypto-button-secondary text-lg px-8 py-4 border-cyber/50 hover:border-cyber"
                >
                  Connect Wallet
                </Button>
              </div>
            </div>
            
            {/* Floating Globe */}
            <div className="absolute bottom-20 right-10 hidden lg:block animate-float">
              <img 
                src={africaGlobe} 
                alt="Africa Globe" 
                className="w-32 h-32 rounded-full glow opacity-80"
              />
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-16 bg-gunmetal">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {stats.map((stat, index) => (
                 <div key={stat.label} className="stats-card text-center animate-slide-up" style={{ animationDelay: `${index * 100}ms` }}>
                   <CountUpStat 
                     value={stat.value} 
                     className="text-2xl md:text-3xl font-crypto font-bold text-cyber mb-2"
                   />
                  <div className="text-sm text-muted-foreground mb-1">{stat.label}</div>
                  <div className="text-xs text-success">{stat.change}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Innovation Section */}
        <section className="py-20 bg-gradient-to-r from-dark-slate to-gunmetal relative overflow-hidden">
          <div className="absolute inset-0 opacity-30">
            <img 
              src={cryptoCityscape} 
              alt="Crypto Cityscape" 
              className="w-full h-full object-cover"
            />
          </div>
          <div className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl md:text-4xl font-crypto font-bold mb-6">
              <span className="glow-text">Revolutionizing</span> African Finance
            </h2>
            <p className="text-xl text-foreground/90 mb-8 max-w-3xl mx-auto">
              Bringing Bitcoin-powered prediction markets to Africa's rapidly growing economy. 
              Join the financial revolution that's reshaping how we forecast the future.
            </p>
            <div className="flex justify-center items-center space-x-8 text-cyber">
              <div className="text-center">
                <Bitcoin className="h-16 w-16 mx-auto mb-2 animate-pulse" />
                <span className="text-sm">Bitcoin Native</span>
              </div>
              <div className="text-center">
                <Globe className="h-16 w-16 mx-auto mb-2 animate-spin-slow" />
                <span className="text-sm">Africa Focused</span>
              </div>
              <div className="text-center">
                <Shield className="h-16 w-16 mx-auto mb-2 animate-pulse" />
                <span className="text-sm">AI Secured</span>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-background">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-crypto font-bold mb-4">
                Why Choose <span className="glow-text">PredictPesa</span>?
              </h2>
              <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                Africa's most advanced prediction market platform, built for the future of decentralized forecasting.
              </p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <Card key={feature.title} className="market-card animate-fade-in" style={{ animationDelay: `${index * 150}ms` }}>
                  <CardContent className="p-6 text-center">
                    <feature.icon className={`h-12 w-12 mx-auto mb-4 ${feature.color}`} />
                    <h3 className="text-xl font-crypto font-semibold mb-3">{feature.title}</h3>
                    <p className="text-muted-foreground">{feature.description}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-gradient-to-r from-gunmetal to-dark-slate">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl md:text-4xl font-crypto font-bold mb-6">
              Ready to Start <span className="glow-text">Predicting</span>?
            </h2>
            <p className="text-xl text-foreground/90 mb-8 max-w-2xl mx-auto">
              Join thousands of users already earning Bitcoin by forecasting real-world events across Africa.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/markets">
                <Button className="crypto-button-primary text-lg px-8 py-4">
                  Browse Markets
                  <TrendingUp className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              
              <Button 
                onClick={() => setIsWalletModalOpen(true)}
                className="crypto-button-gold text-lg px-8 py-4"
              >
                <Zap className="mr-2 h-5 w-5" />
                Get Started
              </Button>
            </div>
          </div>
        </section>
      </div>

      <Footer />

      <WalletConnectionModal
        isOpen={isWalletModalOpen}
        onClose={() => setIsWalletModalOpen(false)}
        onConnect={handleWalletConnect}
      />
    </>
  );
};

export default Home;