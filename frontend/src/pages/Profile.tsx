import { useState } from 'react';
import { User, Settings, Download, LogOut, Bell, Globe, Moon, Sun, Shield, Wallet } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Label } from '@/components/ui/label';

const Profile = () => {
  const [notifications, setNotifications] = useState({
    email: true,
    push: false,
    sms: true,
    marketUpdates: true,
    rewards: true,
    security: true
  });
  
  const [preferences, setPreferences] = useState({
    currency: 'BTC',
    language: 'en',
    theme: 'dark',
    timezone: 'Africa/Lagos'
  });

  const userStats = {
    totalVolume: '₿4.27',
    totalTrades: 143,
    winRate: '67.8%',
    currentStreak: 7,
    level: 'Gold Trader',
    joinDate: 'March 2024',
    walletAddress: '0x1234...5678'
  };

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl md:text-4xl font-crypto font-bold mb-8">
        <span className="glow-text">Profile</span>
      </h1>
      
      <div className="grid lg:grid-cols-3 gap-8">
        {/* User Info Card */}
        <div className="lg:col-span-1">
          <Card className="crypto-card">
            <CardContent className="p-6 text-center">
              <div className="relative inline-block mb-4">
                <User className="h-20 w-20 mx-auto text-cyber bg-dark-slate rounded-full p-4" />
                <Badge className="absolute -bottom-1 -right-1 bg-gold text-black text-xs">
                  {userStats.level}
                </Badge>
              </div>
              <h2 className="text-xl font-crypto mb-2">Anonymous Trader</h2>
              <p className="text-muted-foreground text-sm mb-4">Member since {userStats.joinDate}</p>
              
              <div className="grid grid-cols-2 gap-4 text-center">
                <div className="bg-dark-slate rounded-lg p-3">
                  <div className="text-lg font-crypto text-cyber">{userStats.totalVolume}</div>
                  <div className="text-xs text-muted-foreground">Total Volume</div>
                </div>
                <div className="bg-dark-slate rounded-lg p-3">
                  <div className="text-lg font-crypto text-success">{userStats.winRate}</div>
                  <div className="text-xs text-muted-foreground">Win Rate</div>
                </div>
                <div className="bg-dark-slate rounded-lg p-3">
                  <div className="text-lg font-crypto text-bitcoin">{userStats.totalTrades}</div>
                  <div className="text-xs text-muted-foreground">Total Trades</div>
                </div>
                <div className="bg-dark-slate rounded-lg p-3">
                  <div className="text-lg font-crypto text-gold">{userStats.currentStreak}</div>
                  <div className="text-xs text-muted-foreground">Current Streak</div>
                </div>
              </div>
              
              <div className="mt-6 p-3 bg-gunmetal rounded-lg">
                <div className="flex items-center text-sm">
                  <Wallet className="h-4 w-4 mr-2 text-bitcoin" />
                  <span className="text-muted-foreground">Connected Wallet:</span>
                </div>
                <div className="font-mono text-xs text-cyber mt-1">{userStats.walletAddress}</div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Settings Tabs */}
        <div className="lg:col-span-2">
          <Tabs defaultValue="preferences" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="preferences">Preferences</TabsTrigger>
              <TabsTrigger value="notifications">Notifications</TabsTrigger>
              <TabsTrigger value="security">Security</TabsTrigger>
            </TabsList>

            <TabsContent value="preferences" className="space-y-6">
              <Card className="crypto-card">
                <CardHeader>
                  <CardTitle className="font-crypto flex items-center">
                    <Settings className="mr-2 h-5 w-5" />
                    Display Preferences
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <Label>Preferred Currency</Label>
                      <Select value={preferences.currency} onValueChange={(value) => setPreferences({...preferences, currency: value})}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="BTC">Bitcoin (BTC)</SelectItem>
                          <SelectItem value="USD">US Dollar (USD)</SelectItem>
                          <SelectItem value="NGN">Nigerian Naira (NGN)</SelectItem>
                          <SelectItem value="KES">Kenyan Shilling (KES)</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label>Language</Label>
                      <Select value={preferences.language} onValueChange={(value) => setPreferences({...preferences, language: value})}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="en">English</SelectItem>
                          <SelectItem value="fr">Français</SelectItem>
                          <SelectItem value="sw">Kiswahili</SelectItem>
                          <SelectItem value="ha">Hausa</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label>Timezone</Label>
                      <Select value={preferences.timezone} onValueChange={(value) => setPreferences({...preferences, timezone: value})}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="Africa/Lagos">West Africa Time</SelectItem>
                          <SelectItem value="Africa/Nairobi">East Africa Time</SelectItem>
                          <SelectItem value="Africa/Cairo">Egypt Time</SelectItem>
                          <SelectItem value="Africa/Johannesburg">South Africa Time</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label>Theme</Label>
                      <Select value={preferences.theme} onValueChange={(value) => setPreferences({...preferences, theme: value})}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="dark">Dark Mode</SelectItem>
                          <SelectItem value="blue">Cyber Blue</SelectItem>
                          <SelectItem value="gold">Bitcoin Gold</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="notifications" className="space-y-6">
              <Card className="crypto-card">
                <CardHeader>
                  <CardTitle className="font-crypto flex items-center">
                    <Bell className="mr-2 h-5 w-5" />
                    Notification Settings
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <Label className="text-base">Email Notifications</Label>
                        <p className="text-sm text-muted-foreground">Receive email updates</p>
                      </div>
                      <Switch 
                        checked={notifications.email}
                        onCheckedChange={(checked) => setNotifications({...notifications, email: checked})}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <Label className="text-base">Push Notifications</Label>
                        <p className="text-sm text-muted-foreground">Browser push notifications</p>
                      </div>
                      <Switch 
                        checked={notifications.push}
                        onCheckedChange={(checked) => setNotifications({...notifications, push: checked})}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <Label className="text-base">SMS Alerts</Label>
                        <p className="text-sm text-muted-foreground">Critical market updates via SMS</p>
                      </div>
                      <Switch 
                        checked={notifications.sms}
                        onCheckedChange={(checked) => setNotifications({...notifications, sms: checked})}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <Label className="text-base">Market Updates</Label>
                        <p className="text-sm text-muted-foreground">New markets and price changes</p>
                      </div>
                      <Switch 
                        checked={notifications.marketUpdates}
                        onCheckedChange={(checked) => setNotifications({...notifications, marketUpdates: checked})}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <Label className="text-base">Reward Notifications</Label>
                        <p className="text-sm text-muted-foreground">Claimable rewards and bonuses</p>
                      </div>
                      <Switch 
                        checked={notifications.rewards}
                        onCheckedChange={(checked) => setNotifications({...notifications, rewards: checked})}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <Label className="text-base">Security Alerts</Label>
                        <p className="text-sm text-muted-foreground">Login and security notifications</p>
                      </div>
                      <Switch 
                        checked={notifications.security}
                        onCheckedChange={(checked) => setNotifications({...notifications, security: checked})}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="security" className="space-y-6">
              <Card className="crypto-card">
                <CardHeader>
                  <CardTitle className="font-crypto flex items-center">
                    <Shield className="mr-2 h-5 w-5" />
                    Account Security
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-4">
                    <Button className="crypto-button-primary w-full">
                      <Shield className="mr-2 h-4 w-4" />
                      Enable Two-Factor Authentication
                    </Button>
                    
                    <Button variant="outline" className="w-full">
                      <Download className="mr-2 h-4 w-4" />
                      Export Transaction History
                    </Button>
                    
                    <Button variant="outline" className="w-full">
                      <Download className="mr-2 h-4 w-4" />
                      Download Account Data
                    </Button>
                    
                    <Button variant="outline" className="w-full border-destructive/50 text-destructive hover:bg-destructive/10">
                      <LogOut className="mr-2 h-4 w-4" />
                      Disconnect Wallet
                    </Button>
                  </div>
                  
                  <div className="bg-bitcoin/10 rounded-lg p-4 border border-bitcoin/20">
                    <h3 className="font-crypto text-bitcoin mb-2">Security Tips</h3>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• Never share your wallet private keys</li>
                      <li>• Always verify transaction details before signing</li>
                      <li>• Enable 2FA for enhanced security</li>
                      <li>• Use hardware wallets for large amounts</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
};

export default Profile;