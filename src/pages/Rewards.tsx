import { useState } from 'react';
import { Gift, Trophy, Users, Calendar, Zap, Star, Crown, Copy, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Label } from '@/components/ui/label';
import { useToast } from '@/components/ui/use-toast';

const Rewards = () => {
  const [claimingReward, setClaimingReward] = useState<number | null>(null);
  const [copiedCode, setCopiedCode] = useState(false);
  const [copiedLink, setCopiedLink] = useState(false);
  const { toast } = useToast();

  const rewardStats = {
    totalClaimable: '0.45',
    totalClaimableUSD: '$18,000',
    lifetimeEarned: '2.34',
    pendingRewards: 6,
    currentStreak: 15,
    referralCount: 8
  };

  const claimableRewards = [
    {
      id: 1,
      type: 'Market Resolution',
      market: "Nigeria's Inflation Rate 2024",
      amount: '0.15 BTC',
      source: 'Winning prediction',
      earned: '2 days ago',
      canClaim: true
    },
    {
      id: 2,
      type: 'Referral Bonus',
      amount: '0.05 BTC',
      source: 'Friend joined via your link',
      earned: '5 days ago',
      canClaim: true
    },
    {
      id: 3,
      type: 'Streak Bonus',
      amount: '0.25 BTC',
      source: '15-day prediction streak',
      earned: '1 week ago',
      canClaim: true
    }
  ];

  const rewardHistory = [
    {
      id: 1,
      type: 'Market Win',
      market: 'Kenya Election Results',
      amount: '0.25 BTC',
      claimed: '2024-08-15',
      status: 'claimed'
    },
    {
      id: 2,
      type: 'Volume Bonus',
      amount: '0.08 BTC',
      claimed: '2024-08-10',
      status: 'claimed'
    },
    {
      id: 3,
      type: 'Achievement',
      achievement: 'First Prediction',
      amount: '0.01 BTC',
      claimed: '2024-07-25',
      status: 'claimed'
    }
  ];

  const achievements = [
    {
      id: 1,
      title: 'First Blood',
      description: 'Place your first prediction',
      reward: '0.01 BTC',
      progress: 100,
      unlocked: true,
      icon: Star
    },
    {
      id: 2,
      title: 'Hot Streak',
      description: 'Win 5 predictions in a row',
      reward: '0.05 BTC',
      progress: 80,
      unlocked: false,
      icon: Zap
    },
    {
      id: 3,
      title: 'Market Maker',
      description: 'Create 10 prediction markets',
      reward: '0.1 BTC',
      progress: 30,
      unlocked: false,
      icon: Trophy
    },
    {
      id: 4,
      title: 'Whale',
      description: 'Stake more than 1 BTC total',
      reward: '0.2 BTC',
      progress: 65,
      unlocked: false,
      icon: Crown
    }
  ];

  const referralProgram = {
    referralCode: 'PREDICT2024',
    referralsCount: 8,
    tier: 'Silver',
    nextTier: 'Gold',
    nextTierRequirement: 15,
    commissionRate: '5%'
  };

  const handleClaimReward = async (rewardId: number) => {
    setClaimingReward(rewardId);
    
    // Simulate claiming process
    setTimeout(() => {
      setClaimingReward(null);
      // In real app, remove claimed reward from list
    }, 2000);
  };

  const handleClaimAll = async () => {
    setClaimingReward(-1); // Special ID for claim all
    
    setTimeout(() => {
      setClaimingReward(null);
    }, 3000);
  };

  const copyToClipboard = async (text: string, type: 'code' | 'link') => {
    try {
      await navigator.clipboard.writeText(text);
      if (type === 'code') {
        setCopiedCode(true);
        setTimeout(() => setCopiedCode(false), 2000);
      } else {
        setCopiedLink(true);
        setTimeout(() => setCopiedLink(false), 2000);
      }
      toast({
        title: "Copied!",
        description: `${type === 'code' ? 'Referral code' : 'Referral link'} copied to clipboard`,
      });
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to copy to clipboard",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl md:text-4xl font-crypto font-bold mb-4">
          <span className="glow-text">Rewards</span> Hub
        </h1>
        <p className="text-muted-foreground text-lg">
          Earn Bitcoin through predictions, referrals, and achievements
        </p>
      </div>

      {/* Reward Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card className="stats-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Claimable</p>
                <p className="text-2xl font-crypto font-bold text-gold">
                  ₿{rewardStats.totalClaimable}
                </p>
                <p className="text-sm text-muted-foreground">{rewardStats.totalClaimableUSD}</p>
              </div>
              <Gift className="h-8 w-8 text-gold" />
            </div>
          </CardContent>
        </Card>

        <Card className="stats-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Lifetime Earned</p>
                <p className="text-2xl font-crypto font-bold text-cyber">
                  ₿{rewardStats.lifetimeEarned}
                </p>
                <p className="text-sm text-muted-foreground">All time</p>
              </div>
              <Trophy className="h-8 w-8 text-cyber" />
            </div>
          </CardContent>
        </Card>

        <Card className="stats-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Current Streak</p>
                <p className="text-2xl font-crypto font-bold text-success">
                  {rewardStats.currentStreak}
                </p>
                <p className="text-sm text-muted-foreground">days</p>
              </div>
              <Zap className="h-8 w-8 text-success" />
            </div>
          </CardContent>
        </Card>

        <Card className="stats-card">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Referrals</p>
                <p className="text-2xl font-crypto font-bold text-bitcoin">
                  {rewardStats.referralCount}
                </p>
                <p className="text-sm text-muted-foreground">friends</p>
              </div>
              <Users className="h-8 w-8 text-bitcoin" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Claimable Rewards Section */}
      <Card className="crypto-card mb-8">
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle className="font-crypto text-xl">Claimable Rewards</CardTitle>
            <Button 
              onClick={handleClaimAll}
              disabled={claimingReward !== null}
              className="crypto-button-gold"
            >
              {claimingReward === -1 ? 'Claiming...' : 'Claim All'}
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {claimableRewards.map((reward) => (
            <div key={reward.id} className="p-4 bg-dark-slate rounded-lg border border-border">
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <Badge variant="outline" className="text-xs">
                      {reward.type}
                    </Badge>
                    <span className="text-xs text-muted-foreground">
                      {reward.earned}
                    </span>
                  </div>
                  {reward.market && (
                    <h4 className="font-medium mb-1">{reward.market}</h4>
                  )}
                  <p className="text-sm text-muted-foreground">{reward.source}</p>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <div className="font-crypto font-bold text-gold text-lg">
                      {reward.amount}
                    </div>
                  </div>
                  <Button
                    onClick={() => handleClaimReward(reward.id)}
                    disabled={claimingReward !== null}
                    size="sm"
                    className="crypto-button-primary"
                  >
                    {claimingReward === reward.id ? 'Claiming...' : 'Claim'}
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Tabs for different reward types */}
      <Tabs defaultValue="history" className="mb-8">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="history">Reward History</TabsTrigger>
          <TabsTrigger value="achievements">Achievements</TabsTrigger>
          <TabsTrigger value="referrals">Referral Program</TabsTrigger>
        </TabsList>

        <TabsContent value="history" className="mt-6">
          <Card className="crypto-card">
            <CardHeader>
              <CardTitle className="font-crypto text-xl">Reward History</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {rewardHistory.map((reward) => (
                <div key={reward.id} className="p-4 bg-dark-slate rounded-lg border border-border">
                  <div className="flex justify-between items-center">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <Badge variant="secondary" className="text-xs">
                          {reward.type}
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          {new Date(reward.claimed).toLocaleDateString()}
                        </span>
                      </div>
                      {reward.market && (
                        <h4 className="font-medium">{reward.market}</h4>
                      )}
                      {reward.achievement && (
                        <h4 className="font-medium">{reward.achievement}</h4>
                      )}
                    </div>
                    
                    <div className="text-right">
                      <div className="font-crypto font-bold text-cyber">
                        {reward.amount}
                      </div>
                      <Badge variant="outline" className="text-xs mt-1">
                        Claimed
                      </Badge>
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="achievements" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {achievements.map((achievement) => (
              <Card key={achievement.id} className={`crypto-card ${achievement.unlocked ? 'border-success/50' : ''}`}>
                <CardContent className="p-6">
                  <div className="flex items-start space-x-4 mb-4">
                    <div className={`p-3 rounded-lg ${achievement.unlocked ? 'bg-success/20' : 'bg-muted/20'}`}>
                      <achievement.icon className={`h-6 w-6 ${achievement.unlocked ? 'text-success' : 'text-muted-foreground'}`} />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-crypto font-semibold mb-1">{achievement.title}</h3>
                      <p className="text-sm text-muted-foreground mb-2">{achievement.description}</p>
                      <div className="flex items-center space-x-2">
                        <Badge variant={achievement.unlocked ? 'default' : 'outline'} className="text-xs">
                          {achievement.reward}
                        </Badge>
                        {achievement.unlocked && (
                          <Badge variant="outline" className="text-xs text-success border-success">
                            Unlocked
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  {!achievement.unlocked && (
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">Progress</span>
                        <span className="font-crypto">{achievement.progress}%</span>
                      </div>
                      <Progress value={achievement.progress} className="h-2" />
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="referrals" className="mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="crypto-card">
              <CardHeader>
                <CardTitle className="font-crypto text-xl">Your Referral Stats</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-muted-foreground">Referrals</p>
                    <p className="text-2xl font-crypto font-bold text-cyber">
                      {referralProgram.referralsCount}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Current Tier</p>
                    <Badge variant="outline" className="text-bitcoin border-bitcoin">
                      {referralProgram.tier}
                    </Badge>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Commission Rate</p>
                    <p className="text-lg font-crypto font-bold text-success">
                      {referralProgram.commissionRate}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Next Tier</p>
                    <p className="text-sm text-gold">
                      {referralProgram.nextTier} ({referralProgram.nextTierRequirement} referrals)
                    </p>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Progress to {referralProgram.nextTier}</span>
                    <span className="font-crypto">
                      {referralProgram.referralsCount}/{referralProgram.nextTierRequirement}
                    </span>
                  </div>
                  <Progress 
                    value={(referralProgram.referralsCount / referralProgram.nextTierRequirement) * 100} 
                    className="h-2" 
                  />
                </div>
              </CardContent>
            </Card>

            <Card className="crypto-card">
              <CardHeader>
                <CardTitle className="font-crypto text-xl">Share Your Link</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label className="text-sm text-muted-foreground">Your Referral Code</Label>
                  <div className="flex space-x-2 mt-1">
                    <div className="flex-1 p-3 bg-dark-slate rounded-lg border border-border">
                      <span className="font-crypto text-cyber">{referralProgram.referralCode}</span>
                    </div>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => copyToClipboard(referralProgram.referralCode, 'code')}
                      className={copiedCode ? 'text-success border-success' : ''}
                    >
                      {copiedCode ? <CheckCircle className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                      {copiedCode ? 'Copied!' : 'Copy'}
                    </Button>
                  </div>
                </div>
                
                <div>
                  <Label className="text-sm text-muted-foreground">Referral Link</Label>
                  <div className="flex space-x-2 mt-1">
                    <div className="flex-1 p-3 bg-dark-slate rounded-lg border border-border">
                      <span className="text-xs text-muted-foreground break-all">
                        https://predictpesa.com/ref/{referralProgram.referralCode}
                      </span>
                    </div>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => copyToClipboard(`https://predictpesa.com/ref/${referralProgram.referralCode}`, 'link')}
                      className={copiedLink ? 'text-success border-success' : ''}
                    >
                      {copiedLink ? <CheckCircle className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                      {copiedLink ? 'Copied!' : 'Copy'}
                    </Button>
                  </div>
                </div>
                
                <div className="p-4 bg-bitcoin/10 rounded-lg border border-bitcoin/20">
                  <p className="text-sm text-bitcoin font-medium mb-2">Referral Benefits:</p>
                  <ul className="text-xs text-muted-foreground space-y-1">
                    <li>• Earn {referralProgram.commissionRate} of your referral's staking volume</li>
                    <li>• Get bonus rewards when they reach milestones</li>
                    <li>• Unlock higher commission tiers with more referrals</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Rewards;