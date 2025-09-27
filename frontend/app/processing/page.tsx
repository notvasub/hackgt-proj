"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Zap, FileText, TrendingUp, CheckCircle } from "lucide-react"
import { useRouter } from "next/navigation"

export default function ProcessingPage() {
  const router = useRouter()
  const [progress, setProgress] = useState(0)
  const [currentStep, setCurrentStep] = useState(0)

  const steps = [
    { icon: Zap, title: "Analyzing incident data", description: "Processing photos and incident details" },
    { icon: FileText, title: "Generating refined prompts", description: "Creating optimized claim structure" },
    { icon: TrendingUp, title: "Maximizing claim value", description: "Applying optimization algorithms" },
    { icon: CheckCircle, title: "Finalizing your claim", description: "Preparing downloadable document" },
  ]

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress((prev) => {
        const newProgress = prev + 2

        // Update current step based on progress
        if (newProgress >= 25 && currentStep < 1) setCurrentStep(1)
        if (newProgress >= 50 && currentStep < 2) setCurrentStep(2)
        if (newProgress >= 75 && currentStep < 3) setCurrentStep(3)

        if (newProgress >= 100) {
          clearInterval(timer)
          setTimeout(() => router.push("/review"), 1000)
          return 100
        }

        return newProgress
      })
    }, 100)

    return () => clearInterval(timer)
  }, [currentStep, router])

  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <Card className="bg-card border-border/50">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl mb-2">Processing Your Claim</CardTitle>
            <p className="text-muted-foreground">
              Our AI is analyzing your information to create the optimal insurance claim.
            </p>
          </CardHeader>
          <CardContent className="space-y-8">
            {/* Progress Bar */}
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span>Progress</span>
                <span>{Math.round(progress)}%</span>
              </div>
              <Progress value={progress} className="h-2" />
            </div>

            {/* Steps */}
            <div className="space-y-4">
              {steps.map((step, index) => {
                const Icon = step.icon
                const isActive = index === currentStep
                const isCompleted = index < currentStep

                return (
                  <div
                    key={index}
                    className={`flex items-center space-x-4 p-4 rounded-lg transition-all ${
                      isActive
                        ? "bg-primary/10 border border-primary/20"
                        : isCompleted
                          ? "bg-secondary/50"
                          : "bg-secondary/20"
                    }`}
                  >
                    <div
                      className={`w-10 h-10 rounded-full flex items-center justify-center ${
                        isActive
                          ? "bg-primary text-primary-foreground"
                          : isCompleted
                            ? "bg-accent text-accent-foreground"
                            : "bg-muted text-muted-foreground"
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                    </div>
                    <div className="flex-1">
                      <h3 className={`font-medium ${isActive ? "text-foreground" : "text-muted-foreground"}`}>
                        {step.title}
                      </h3>
                      <p className="text-sm text-muted-foreground">{step.description}</p>
                    </div>
                    {isCompleted && <CheckCircle className="w-5 h-5 text-accent" />}
                  </div>
                )
              })}
            </div>

            {/* Loading Animation */}
            <div className="text-center">
              <div className="inline-flex items-center space-x-2 text-muted-foreground">
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
