'use server';
/**
 * @fileOverview An AI agent that suggests test cases based on surviving mutants.
 *
 * - suggestTestCases - A function that handles the test case suggestion process.
 * - SuggestTestCasesInput - The input type for the suggestTestCases function.
 * - SuggestTestCasesOutput - The return type for the suggestTestCases function.
 */

import {ai} from '@/ai/ai-instance';
import {z} from 'genkit';

const SuggestTestCasesInputSchema = z.object({
  mutantAnalysis: z
    .string()
    .describe(
      'Analysis of surviving mutants, including code snippets and descriptions.'
    ),
  language: z.enum(['PHP']).describe('The programming language of the code.'),
});
export type SuggestTestCasesInput = z.infer<typeof SuggestTestCasesInputSchema>;

const SuggestTestCasesOutputSchema = z.object({
  testCaseSuggestions: z
    .array(z.string())
    .describe('Array of suggested test case stubs.'),
});
export type SuggestTestCasesOutput = z.infer<typeof SuggestTestCasesOutputSchema>;

export async function suggestTestCases(
  input: SuggestTestCasesInput
): Promise<SuggestTestCasesOutput> {
  return suggestTestCasesFlow(input);
}

const prompt = ai.definePrompt({
  name: 'suggestTestCasesPrompt',
  input: {
    schema: z.object({
      mutantAnalysis: z
        .string()
        .describe(
          'Analysis of surviving mutants, including code snippets and descriptions.'
        ),
      language: z.enum(['PHP']).describe('The programming language of the code.'),
    }),
  },
  output: {
    schema: z.object({
      testCaseSuggestions: z
        .array(z.string())
        .describe('Array of suggested test case stubs.'),
    }),
  },
  prompt: `You are an AI assistant that analyzes surviving mutants from mutation testing and suggests test cases to improve code coverage.

  Analyze the following mutant analysis and generate basic test case stubs that would kill the mutants.
  The test cases should be in the language specified.

  Language: {{{language}}}
  Mutant Analysis: {{{mutantAnalysis}}}

  Test Case Suggestions:
  `,
});

const suggestTestCasesFlow = ai.defineFlow<
  typeof SuggestTestCasesInputSchema,
  typeof SuggestTestCasesOutputSchema
>(
  {
    name: 'suggestTestCasesFlow',
    inputSchema: SuggestTestCasesInputSchema,
    outputSchema: SuggestTestCasesOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
