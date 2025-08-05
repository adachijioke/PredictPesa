import { Bitcoin, Twitter, Github, Linkedin, Mail, Globe } from 'lucide-react';
import { Button } from '@/components/ui/button';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gunmetal border-t border-border mt-20">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Brand Section */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Bitcoin className="h-8 w-8 text-bitcoin" />
              <span className="text-2xl font-crypto font-bold glow-text">PredictPesa</span>
            </div>
            <p className="text-muted-foreground text-sm">
              Africa's Bitcoin-native prediction market. Stake Bitcoin, forecast everything, trade your belief.
            </p>
            <div className="flex space-x-3">
              <Button variant="ghost" size="icon" className="hover:text-bitcoin">
                <Twitter className="h-4 w-4" />
              </Button>
              <Button variant="ghost" size="icon" className="hover:text-bitcoin">
                <Github className="h-4 w-4" />
              </Button>
              <Button variant="ghost" size="icon" className="hover:text-bitcoin">
                <Linkedin className="h-4 w-4" />
              </Button>
              <Button variant="ghost" size="icon" className="hover:text-bitcoin">
                <Mail className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Markets */}
          <div className="space-y-4">
            <h3 className="font-crypto font-semibold text-foreground">Markets</h3>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">Economics</a></li>
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">Politics</a></li>
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">Sports</a></li>
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">Weather</a></li>
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">Technology</a></li>
            </ul>
          </div>

          {/* Platform */}
          <div className="space-y-4">
            <h3 className="font-crypto font-semibold text-foreground">Platform</h3>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">How it Works</a></li>
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">API Docs</a></li>
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">Security</a></li>
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">Whitepaper</a></li>
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">Tokenomics</a></li>
            </ul>
          </div>

          {/* Support */}
          <div className="space-y-4">
            <h3 className="font-crypto font-semibold text-foreground">Support</h3>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">Help Center</a></li>
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">Terms of Service</a></li>
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">Privacy Policy</a></li>
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">Bug Reports</a></li>
              <li><a href="#" className="text-muted-foreground hover:text-bitcoin transition-smooth">Contact</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-border mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-4 text-sm text-muted-foreground">
            <span>© {currentYear} PredictPesa. All rights reserved.</span>
            <div className="flex items-center space-x-1">
              <Globe className="h-4 w-4" />
              <span>Powered by Hedera & Bitcoin</span>
            </div>
          </div>
          <div className="mt-4 md:mt-0 text-sm text-muted-foreground">
            Built for Africa, secured by Bitcoin
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;