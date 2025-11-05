import express from 'express'
import { JiraConnectRequestSchema, JiraStoryDetailsRequestSchema, JiraStoriesResponseSchema } from '../schemas'
import * as jiraClient from '../utils/jiraClient'

export const jiraRouter = express.Router()

// POST /api/jira/connect
jiraRouter.post('/connect', async (req: express.Request, res: express.Response) => {
  const validation = JiraConnectRequestSchema.safeParse(req.body)
  if (!validation.success) {
    res.status(400).json({ error: `Validation error: ${validation.error.message}` })
    return
  }

  const { baseUrl, email, apiToken } = validation.data

  try {
    const ok = await jiraClient.validateAuth(baseUrl, email, apiToken)
    if (!ok) {
      res.status(401).json({ error: 'Authentication failed: invalid credentials or insufficient permissions' })
      return
    }

    res.json({ success: true })
  } catch (err) {
    console.error('Jira connect error:', err)
    res.status(502).json({ error: err instanceof Error ? err.message : 'Failed to connect to Jira' })
  }
})

// POST /api/jira/stories
jiraRouter.post('/stories', async (req: express.Request, res: express.Response) => {
  // Body can contain baseUrl, email, apiToken and optional jql
  const body = req.body || {}
  const validation = JiraConnectRequestSchema.safeParse(body)
  if (!validation.success) {
    res.status(400).json({ error: `Validation error: ${validation.error.message}` })
    return
  }

  const { baseUrl, email, apiToken } = validation.data
  const jql = body.jql as string | undefined

  try {
    const data = await jiraClient.searchStories(baseUrl, email, apiToken, jql)
    // Validate shape lightly
    const response = {
      issues: (data.issues || []).map((i: any) => ({ id: i.id, key: i.key, summary: i.fields?.summary }))
    }

    const parsed = JiraStoriesResponseSchema.parse(response)
    res.json(parsed)
  } catch (err) {
    console.error('Jira stories error:', err)
    res.status(err instanceof Error ? 502 : 500).json({ error: err instanceof Error ? err.message : 'Failed to fetch stories' })
  }
})

// POST /api/jira/stories/details
jiraRouter.post('/stories/details', async (req: express.Request, res: express.Response) => {
  const validation = JiraStoryDetailsRequestSchema.safeParse(req.body)
  if (!validation.success) {
    res.status(400).json({ error: `Validation error: ${validation.error.message}` })
    return
  }

  const { baseUrl, email, apiToken, issueIdOrKey } = validation.data

  try {
    const details = await jiraClient.getIssueDetails(baseUrl, email, apiToken, issueIdOrKey)
    res.json({
      id: details.id,
      key: details.key,
      summary: details.summary,
      description: details.description,
      acceptanceCriteria: (details as any).acceptanceCriteria || ''
    })
  } catch (err) {
    console.error('Jira story details error:', err)
    res.status(err instanceof Error ? 502 : 500).json({ error: err instanceof Error ? err.message : 'Failed to fetch story details' })
  }
})

export default jiraRouter
