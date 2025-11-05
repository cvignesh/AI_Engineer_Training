import { z } from 'zod'

export const GenerateRequestSchema = z.object({
  storyTitle: z.string().min(1, 'Story title is required'),
  acceptanceCriteria: z.string().min(1, 'Acceptance criteria is required'),
  description: z.string().optional(),
  additionalInfo: z.string().optional()
})

export const TestCaseSchema = z.object({
  id: z.string(),
  title: z.string(),
  steps: z.array(z.string()),
  testData: z.string().optional(),
  expectedResult: z.string(),
  category: z.string()
})

export const GenerateResponseSchema = z.object({
  cases: z.array(TestCaseSchema),
  model: z.string().optional(),
  promptTokens: z.number(),
  completionTokens: z.number()
})

// Type exports
export type GenerateRequest = z.infer<typeof GenerateRequestSchema>
export type TestCase = z.infer<typeof TestCaseSchema>
export type GenerateResponse = z.infer<typeof GenerateResponseSchema>

// Jira-related schemas
export const JiraConnectRequestSchema = z.object({
  baseUrl: z.string().url(),
  email: z.string().min(1),
  apiToken: z.string().min(1)
})

export const JiraStorySummarySchema = z.object({
  id: z.string(),
  key: z.string(),
  summary: z.string().optional()
})

export const JiraStoriesResponseSchema = z.object({
  issues: z.array(JiraStorySummarySchema)
})

export const JiraStoryDetailsRequestSchema = z.object({
  baseUrl: z.string().url(),
  email: z.string().min(1),
  apiToken: z.string().min(1),
  issueIdOrKey: z.string().min(1)
})

export const JiraStoryDetailsSchema = z.object({
  id: z.string(),
  key: z.string(),
  summary: z.string().optional(),
  description: z.string().optional(),
  acceptanceCriteria: z.string().optional()
})

export type JiraConnectRequest = z.infer<typeof JiraConnectRequestSchema>
export type JiraStorySummary = z.infer<typeof JiraStorySummarySchema>
export type JiraStoriesResponse = z.infer<typeof JiraStoriesResponseSchema>
export type JiraStoryDetailsRequest = z.infer<typeof JiraStoryDetailsRequestSchema>
export type JiraStoryDetails = z.infer<typeof JiraStoryDetailsSchema>