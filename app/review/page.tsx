"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Download, Edit, ArrowLeft, FileText, TrendingUp } from "lucide-react"
import Link from "next/link"

export default function ReviewPage() {
  const [isEditing, setIsEditing] = useState<string | null>(null)
  const [claimData, setClaimData] = useState({
    incidentDescription:
      "On January 15, 2025, at approximately 2:30 PM, I was involved in a motor vehicle collision at the intersection of Main Street and Oak Avenue during light rain conditions. While proceeding through a green traffic light, the other vehicle failed to yield the right-of-way when making a left turn, resulting in a T-bone collision with the driver's side of my 2022 Honda Accord. The impact caused significant damage to the driver's side door, front quarter panel, and side mirror, with additional damage to the front bumper and headlight assembly.",
    damageAssessment:
      "The collision resulted in extensive damage to multiple vehicle components: (1) Driver's side door - severe denting and paint damage requiring full replacement, (2) Front left quarter panel - structural damage with paint transfer from other vehicle, (3) Driver's side mirror - completely detached and non-functional, (4) Front bumper - cracked and misaligned, (5) Left headlight assembly - cracked lens with potential electrical damage, (6) Potential frame damage requiring professional inspection. All damage is consistent with a side-impact collision and directly attributable to the incident.",
    claimJustification:
      "This claim is fully justified under my comprehensive coverage policy. The other driver's failure to yield right-of-way during a left turn constitutes clear liability, as documented in the police report (Report #2025-0115-001). The extensive damage requires immediate repair to ensure vehicle safety and roadworthiness. I have maintained continuous coverage with no prior claims, demonstrating responsible policy management. The requested compensation reflects fair market repair costs based on certified estimates from authorized repair facilities.",
    requestedAmount: "$12,450",
  })

  const strengthScore = 92

  const handleEdit = (field: string) => {
    setIsEditing(field)
  }

  const handleSave = (field: string, value: string) => {
    setClaimData((prev) => ({ ...prev, [field]: value }))
    setIsEditing(null)
  }

  const handleDownload = () => {
    // In a real app, this would generate and download a PDF
    const claimText = `
INSURANCE CLAIM DOCUMENT

Incident Description:
${claimData.incidentDescription}

Damage Assessment:
${claimData.damageAssessment}

Claim Justification:
${claimData.claimJustification}

Requested Amount: ${claimData.requestedAmount}
    `.trim()

    const blob = new Blob([claimText], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "insurance-claim.txt"
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border/50 backdrop-blur-sm bg-background/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/upload" className="flex items-center space-x-2">
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Upload</span>
            </Link>
            <Badge variant="secondary" className="bg-accent/10 text-accent border-accent/20">
              Claim Generated
            </Badge>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-4">Your Optimized Insurance Claim</h1>
          <p className="text-muted-foreground">Review and edit your AI-generated claim before downloading.</p>
        </div>

        {/* Claim Strength */}
        <Card className="mb-8 bg-accent/5 border-accent/20">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-5 h-5 text-accent" />
                <span className="font-medium">Claim Strength Score</span>
              </div>
              <Badge className="bg-accent text-accent-foreground">{strengthScore}/100</Badge>
            </div>
            <Progress value={strengthScore} className="h-2 mb-2" />
            <p className="text-sm text-muted-foreground">
              Excellent! Your claim has been optimized for maximum reimbursement potential.
            </p>
          </CardContent>
        </Card>

        {/* Claim Sections */}
        <div className="space-y-6">
          {/* Incident Description */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle className="flex items-center space-x-2">
                <FileText className="w-5 h-5" />
                <span>Incident Description</span>
              </CardTitle>
              <Button variant="outline" size="sm" onClick={() => handleEdit("incidentDescription")}>
                <Edit className="w-4 h-4 mr-2" />
                Edit
              </Button>
            </CardHeader>
            <CardContent>
              {isEditing === "incidentDescription" ? (
                <div className="space-y-4">
                  <Textarea
                    value={claimData.incidentDescription}
                    onChange={(e) => setClaimData((prev) => ({ ...prev, incidentDescription: e.target.value }))}
                    className="min-h-32"
                  />
                  <div className="flex space-x-2">
                    <Button size="sm" onClick={() => handleSave("incidentDescription", claimData.incidentDescription)}>
                      Save
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => setIsEditing(null)}>
                      Cancel
                    </Button>
                  </div>
                </div>
              ) : (
                <p className="text-muted-foreground leading-relaxed">{claimData.incidentDescription}</p>
              )}
            </CardContent>
          </Card>

          {/* Damage Assessment */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>Damage Assessment</CardTitle>
              <Button variant="outline" size="sm" onClick={() => handleEdit("damageAssessment")}>
                <Edit className="w-4 h-4 mr-2" />
                Edit
              </Button>
            </CardHeader>
            <CardContent>
              {isEditing === "damageAssessment" ? (
                <div className="space-y-4">
                  <Textarea
                    value={claimData.damageAssessment}
                    onChange={(e) => setClaimData((prev) => ({ ...prev, damageAssessment: e.target.value }))}
                    className="min-h-32"
                  />
                  <div className="flex space-x-2">
                    <Button size="sm" onClick={() => handleSave("damageAssessment", claimData.damageAssessment)}>
                      Save
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => setIsEditing(null)}>
                      Cancel
                    </Button>
                  </div>
                </div>
              ) : (
                <p className="text-muted-foreground leading-relaxed">{claimData.damageAssessment}</p>
              )}
            </CardContent>
          </Card>

          {/* Claim Justification */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>Claim Justification</CardTitle>
              <Button variant="outline" size="sm" onClick={() => handleEdit("claimJustification")}>
                <Edit className="w-4 h-4 mr-2" />
                Edit
              </Button>
            </CardHeader>
            <CardContent>
              {isEditing === "claimJustification" ? (
                <div className="space-y-4">
                  <Textarea
                    value={claimData.claimJustification}
                    onChange={(e) => setClaimData((prev) => ({ ...prev, claimJustification: e.target.value }))}
                    className="min-h-32"
                  />
                  <div className="flex space-x-2">
                    <Button size="sm" onClick={() => handleSave("claimJustification", claimData.claimJustification)}>
                      Save
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => setIsEditing(null)}>
                      Cancel
                    </Button>
                  </div>
                </div>
              ) : (
                <p className="text-muted-foreground leading-relaxed">{claimData.claimJustification}</p>
              )}
            </CardContent>
          </Card>

          {/* Requested Amount */}
          <Card>
            <CardHeader>
              <CardTitle>Requested Amount</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-accent">{claimData.requestedAmount}</div>
              <p className="text-sm text-muted-foreground mt-2">Based on market rates and damage assessment</p>
            </CardContent>
          </Card>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 mt-8">
          <Button onClick={handleDownload} className="bg-accent text-accent-foreground hover:bg-accent/90 flex-1">
            <Download className="w-4 h-4 mr-2" />
            Download Claim
          </Button>
          <Button variant="outline" className="flex-1 bg-transparent">
            Save & Continue Later
          </Button>
        </div>
      </div>
    </div>
  )
}
