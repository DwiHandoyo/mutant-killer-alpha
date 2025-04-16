
"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/hooks/use-toast";
import { Toaster } from "@/components/ui/toaster";

export default function Home() {
  const [gitUrl, setGitUrl] = useState("");
  const [status, setStatus] = useState("");
  const [results, setResults] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async () => {
    setIsLoading(true);
    setStatus("Cloning repository...");

    // Simulate processing (replace with actual backend call)
    setTimeout(() => {
      setStatus("Analyzing code...");
      setTimeout(() => {
        setStatus("Running mutation tests...");
        setTimeout(() => {
          setStatus("Generating test case suggestions...");
          setTimeout(() => {
            setResults("Suggested test cases: \n - Test case 1\n - Test case 2");
            setStatus("Complete!");
            setIsLoading(false);
            toast({
              title: "Mutation testing complete!",
              description: "Test case suggestions generated.",
            });
          }, 2000);
        }, 2000);
      }, 1500);
    }, 3000);
  };

  return (
    <div className="flex flex-col items-center justify-start min-h-screen bg-secondary p-4">
      <Toaster />
      <Card className="w-full max-w-3xl p-4 bg-card shadow-md rounded-lg">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-primary">MutationWatch</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label htmlFor="git-url" className="block text-sm font-medium text-foreground">
              Git Repository URL
            </label>
            <Input
              type="url"
              id="git-url"
              placeholder="https://github.com/example/repo"
              value={gitUrl}
              onChange={(e) => setGitUrl(e.target.value)}
              className="mt-1"
            />
          </div>
          <Button onClick={handleSubmit} disabled={isLoading}>
            {isLoading ? "Processing..." : "Analyze Repository"}
          </Button>
          {status && (
            <div className="mt-4">
              <p className="text-sm text-muted-foreground">Status: {status}</p>
            </div>
          )}
          {results && (
            <div className="mt-4">
              <label htmlFor="results" className="block text-sm font-medium text-foreground">
                Results
              </label>
              <Textarea
                id="results"
                value={results}
                readOnly
                className="mt-1 h-48 resize-none"
              />
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
