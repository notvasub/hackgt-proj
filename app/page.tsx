import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ArrowRight, Shield, Zap, FileText, TrendingUp, Users, Star, Lock } from "lucide-react"
import Link from "next/link"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border/50 backdrop-blur-sm bg-background/80 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <Shield className="w-5 h-5 text-primary-foreground" />
              </div>
              <span className="text-xl font-bold text-foreground">ClaimMax AI</span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <Link href="#about" className="text-muted-foreground hover:text-foreground transition-colors">
                About the Tech
              </Link>
              <Link href="#features" className="text-muted-foreground hover:text-foreground transition-colors">
                Features
              </Link>
              <Link href="#security" className="text-muted-foreground hover:text-foreground transition-colors">
                Security
              </Link>
              <Button asChild className="bg-accent text-accent-foreground hover:bg-accent/90">
                <Link href="/upload">Get Started</Link>
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 grid-pattern"></div>
        <div className="absolute inset-0 gradient-overlay"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
          <div className="text-center">
            <Badge variant="secondary" className="mb-6 bg-primary/10 text-primary border-primary/20">
              AI-Powered Insurance Claims
            </Badge>
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-balance mb-6">
              Maximize Your{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
                Insurance Claims
              </span>{" "}
              with AI
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-8 text-pretty">
              Transform your insurance claim experience with our AI-driven platform. Upload incident details, photos,
              and policy information to generate optimized claims that maximize your reimbursement potential.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button asChild size="lg" className="bg-accent text-accent-foreground hover:bg-accent/90">
                <Link href="/upload">
                  Start My Claim <ArrowRight className="ml-2 w-4 h-4" />
                </Link>
              </Button>
              <Button variant="outline" size="lg" asChild>
                <Link href="#about">Learn How It Works</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Statement */}
      <section className="py-24 bg-card/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4 text-balance">Ensure Your Coverage</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Insurance claims shouldn't be complicated. Here's why the current system fails you.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="bg-card border-border/50">
              <CardContent className="p-8">
                <div className="text-2xl font-bold mb-2 text-chart-2">33%</div>
                <p className="text-muted-foreground">
                  More than one-third of auto insurance customers are not very satisfied with their claims experience in
                  2025. (JD Power)
                </p>
              </CardContent>
            </Card>
            <Card className="bg-card border-border/50">
              <CardContent className="p-8">
                <div className="text-2xl font-bold mb-2 text-chart-2">22%</div>
                <p className="text-muted-foreground">
                  Of consumers—about 1 in 5—have avoided filing an auto insurance claim because the digital claim
                  process was too frustrating or complicated to navigate.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-card border-border/50">
              <CardContent className="p-8">
                <div className="text-2xl font-bold mb-2 text-chart-2">Manual</div>
                <p className="text-muted-foreground">
                  Manual claim processing increases errors and delays, with customers citing lost documents, repeated
                  data entry, and confusing paper-based forms as common hurdles.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* About the Tech */}
      <section id="about" className="py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">About the Tech</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Our AI-powered system transforms your incident details into maximally optimized insurance claims.
            </p>
          </div>

          {/* Process Flow */}
          <div className="relative">
            <div className="flex flex-col lg:flex-row items-center justify-between space-y-8 lg:space-y-0 lg:space-x-8">
              {/* User */}
              <div className="flex flex-col items-center text-center">
                <div className="w-16 h-16 bg-accent rounded-full flex items-center justify-center mb-4">
                  <Users className="w-8 h-8 text-accent-foreground" />
                </div>
                <h3 className="font-semibold mb-2">User</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>Incident-relevant data</div>
                  <div>Pictures of Damage</div>
                  <div>Insurance claim</div>
                </div>
              </div>

              <ArrowRight className="w-6 h-6 text-muted-foreground hidden lg:block" />

              {/* Analyzer LLM */}
              <div className="flex flex-col items-center text-center">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mb-4">
                  <Zap className="w-8 h-8 text-primary-foreground" />
                </div>
                <h3 className="font-semibold mb-2">Analyzer LLM</h3>
                <p className="text-sm text-muted-foreground max-w-32">Processes incident data and images</p>
              </div>

              <ArrowRight className="w-6 h-6 text-muted-foreground hidden lg:block" />

              {/* Generate */}
              <div className="flex flex-col items-center text-center">
                <div className="w-16 h-16 bg-secondary rounded-full flex items-center justify-center mb-4">
                  <FileText className="w-8 h-8 text-secondary-foreground" />
                </div>
                <h3 className="font-semibold mb-2">Generate</h3>
                <p className="text-sm text-muted-foreground max-w-32">Refined prompt creation</p>
              </div>

              <ArrowRight className="w-6 h-6 text-muted-foreground hidden lg:block" />

              {/* Finalizer */}
              <div className="flex flex-col items-center text-center">
                <div className="w-16 h-16 bg-chart-3 rounded-full flex items-center justify-center mb-4">
                  <TrendingUp className="w-8 h-8 text-white" />
                </div>
                <h3 className="font-semibold mb-2">Finalizer</h3>
                <p className="text-sm text-muted-foreground max-w-32">Optimization engine</p>
              </div>

              <ArrowRight className="w-6 h-6 text-muted-foreground hidden lg:block" />

              {/* Output */}
              <div className="flex flex-col items-center text-center">
                <div className="w-16 h-16 bg-accent rounded-full flex items-center justify-center mb-4">
                  <Star className="w-8 h-8 text-accent-foreground" />
                </div>
                <h3 className="font-semibold mb-2">Output</h3>
                <p className="text-sm text-muted-foreground max-w-32">Maximally optimized insurance claim</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-24 bg-card/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Powerful Features</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Everything you need to maximize your insurance claim success.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="bg-card border-border/50">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                  <FileText className="w-6 h-6 text-primary" />
                </div>
                <h3 className="font-semibold mb-2">Smart Document Analysis</h3>
                <p className="text-muted-foreground">
                  AI analyzes your incident photos and details to identify all claimable damages.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-card border-border/50">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center mb-4">
                  <TrendingUp className="w-6 h-6 text-accent" />
                </div>
                <h3 className="font-semibold mb-2">Claim Optimization</h3>
                <p className="text-muted-foreground">
                  Maximize your reimbursement with AI-generated claims that highlight every detail.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-card border-border/50">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-chart-3/10 rounded-lg flex items-center justify-center mb-4">
                  <Zap className="w-6 h-6 text-chart-3" />
                </div>
                <h3 className="font-semibold mb-2">Instant Processing</h3>
                <p className="text-muted-foreground">Get your optimized claim in minutes, not hours or days.</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Security */}
      <section id="security" className="py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <Lock className="w-8 h-8 text-primary" />
            </div>
            <h2 className="text-2xl font-bold mb-4">Your Data is Secure</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              We use enterprise-grade encryption and never store your personal information. Your privacy and security
              are our top priorities.
            </p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 bg-card/50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">Ready to Maximize Your Claim?</h2>
          <p className="text-xl text-muted-foreground mb-8">
            Join thousands of users who have successfully optimized their insurance claims with AI.
          </p>
          <Button asChild size="lg" className="bg-accent text-accent-foreground hover:bg-accent/90">
            <Link href="/upload">
              Start My Claim <ArrowRight className="ml-2 w-4 h-4" />
            </Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <Shield className="w-5 h-5 text-primary-foreground" />
              </div>
              <span className="text-xl font-bold">ClaimMax AI</span>
            </div>
            <div className="flex space-x-6 text-sm text-muted-foreground">
              <Link href="/privacy" className="hover:text-foreground transition-colors">
                Privacy Policy
              </Link>
              <Link href="/terms" className="hover:text-foreground transition-colors">
                Terms of Service
              </Link>
              <Link href="/contact" className="hover:text-foreground transition-colors">
                Contact
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
