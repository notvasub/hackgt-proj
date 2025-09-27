"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Upload, ArrowLeft, ArrowRight, FileImage, X } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"

export default function UploadPage() {
  const router = useRouter()
  const [step, setStep] = useState(1)
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const [formData, setFormData] = useState({
    incidentDescription: "",
    incidentDate: "",
    incidentLocation: "",
    insuranceProvider: "",
    policyNumber: "",
    claimType: "",
  })

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || [])
    setUploadedFiles((prev) => [...prev, ...files])
  }

  const removeFile = (index: number) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const handleNext = () => {
    if (step < 3) {
      setStep(step + 1)
    } else {
      router.push("/processing")
    }
  }

  const canProceed = () => {
    if (step === 1) {
      return uploadedFiles.length > 0 && formData.incidentDescription.trim() !== ""
    }
    if (step === 2) {
      return (
        formData.insuranceProvider.trim() !== "" && formData.policyNumber.trim() !== "" && formData.claimType !== ""
      )
    }
    return true
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border/50 backdrop-blur-sm bg-background/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center space-x-2">
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Home</span>
            </Link>
            <div className="text-sm text-muted-foreground">Step {step} of 3</div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium">Progress</span>
            <span className="text-sm text-muted-foreground">{Math.round((step / 3) * 100)}%</span>
          </div>
          <div className="w-full bg-secondary rounded-full h-2">
            <div
              className="bg-primary h-2 rounded-full transition-all duration-300"
              style={{ width: `${(step / 3) * 100}%` }}
            />
          </div>
        </div>

        {/* Step 1: Upload Incident Details */}
        {step === 1 && (
          <Card>
            <CardHeader>
              <CardTitle>Upload Incident Details</CardTitle>
              <p className="text-muted-foreground">Upload photos of the damage and describe what happened.</p>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* File Upload */}
              <div>
                <Label htmlFor="file-upload" className="text-base font-medium">
                  Upload Photos
                </Label>
                <div className="mt-2">
                  <label
                    htmlFor="file-upload"
                    className="relative cursor-pointer rounded-lg border-2 border-dashed border-border hover:border-primary/50 transition-colors"
                  >
                    <div className="flex flex-col items-center justify-center px-6 py-12">
                      <Upload className="w-12 h-12 text-muted-foreground mb-4" />
                      <div className="text-center">
                        <p className="text-lg font-medium">Click to upload photos</p>
                        <p className="text-muted-foreground">or drag and drop</p>
                        <p className="text-sm text-muted-foreground mt-2">PNG, JPG, GIF up to 10MB each</p>
                      </div>
                    </div>
                    <input
                      id="file-upload"
                      name="file-upload"
                      type="file"
                      className="sr-only"
                      multiple
                      accept="image/*"
                      onChange={handleFileUpload}
                    />
                  </label>
                </div>
              </div>

              {/* Uploaded Files */}
              {uploadedFiles.length > 0 && (
                <div>
                  <Label className="text-base font-medium">Uploaded Files</Label>
                  <div className="mt-2 space-y-2">
                    {uploadedFiles.map((file, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-secondary rounded-lg">
                        <div className="flex items-center space-x-3">
                          <FileImage className="w-5 h-5 text-muted-foreground" />
                          <span className="text-sm">{file.name}</span>
                        </div>
                        <Button variant="ghost" size="sm" onClick={() => removeFile(index)}>
                          <X className="w-4 h-4" />
                        </Button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Incident Description */}
              <div>
                <Label htmlFor="description" className="text-base font-medium">
                  Incident Description
                </Label>
                <Textarea
                  id="description"
                  placeholder="Describe what happened in detail. Include the time, weather conditions, and any other relevant information..."
                  className="mt-2 min-h-32"
                  value={formData.incidentDescription}
                  onChange={(e) => handleInputChange("incidentDescription", e.target.value)}
                />
              </div>

              {/* Optional Metadata */}
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="date">Date of Incident</Label>
                  <Input
                    id="date"
                    type="date"
                    className="mt-2"
                    value={formData.incidentDate}
                    onChange={(e) => handleInputChange("incidentDate", e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor="location">Location</Label>
                  <Input
                    id="location"
                    placeholder="City, State or Address"
                    className="mt-2"
                    value={formData.incidentLocation}
                    onChange={(e) => handleInputChange("incidentLocation", e.target.value)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 2: Insurance Provider Metadata */}
        {step === 2 && (
          <Card>
            <CardHeader>
              <CardTitle>Insurance Information</CardTitle>
              <p className="text-muted-foreground">Provide your insurance details to generate an optimized claim.</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <Label htmlFor="provider" className="text-base font-medium">
                  Insurance Provider Name
                </Label>
                <Input
                  id="provider"
                  placeholder="e.g., State Farm, Geico, Allstate"
                  className="mt-2"
                  value={formData.insuranceProvider}
                  onChange={(e) => handleInputChange("insuranceProvider", e.target.value)}
                />
              </div>

              <div>
                <Label htmlFor="policy" className="text-base font-medium">
                  Policy Number
                </Label>
                <Input
                  id="policy"
                  placeholder="Your policy number"
                  className="mt-2"
                  value={formData.policyNumber}
                  onChange={(e) => handleInputChange("policyNumber", e.target.value)}
                />
              </div>

              <div>
                <Label htmlFor="claim-type" className="text-base font-medium">
                  Claim Type
                </Label>
                <Select value={formData.claimType} onValueChange={(value) => handleInputChange("claimType", value)}>
                  <SelectTrigger className="mt-2">
                    <SelectValue placeholder="Select claim type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="auto">Auto Insurance</SelectItem>
                    <SelectItem value="home">Home Insurance</SelectItem>
                    <SelectItem value="health">Health Insurance</SelectItem>
                    <SelectItem value="renters">Renters Insurance</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 3: Review */}
        {step === 3 && (
          <Card>
            <CardHeader>
              <CardTitle>Review Your Information</CardTitle>
              <p className="text-muted-foreground">
                Please review your information before generating your optimized claim.
              </p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <h3 className="font-medium mb-2">Uploaded Files</h3>
                <p className="text-muted-foreground">{uploadedFiles.length} files uploaded</p>
              </div>

              <div>
                <h3 className="font-medium mb-2">Incident Description</h3>
                <p className="text-muted-foreground">{formData.incidentDescription}</p>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <h3 className="font-medium mb-2">Insurance Provider</h3>
                  <p className="text-muted-foreground">{formData.insuranceProvider}</p>
                </div>
                <div>
                  <h3 className="font-medium mb-2">Claim Type</h3>
                  <p className="text-muted-foreground capitalize">{formData.claimType}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Navigation Buttons */}
        <div className="flex justify-between mt-8">
          <Button variant="outline" onClick={() => setStep(Math.max(1, step - 1))} disabled={step === 1}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Previous
          </Button>
          <Button
            onClick={handleNext}
            disabled={!canProceed()}
            className="bg-accent text-accent-foreground hover:bg-accent/90"
          >
            {step === 3 ? "Generate Claim" : "Next"}
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </div>
    </div>
  )
}
