import { GenerateRequest, GenerateResponse } from './types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8081/api'

export async function generateTests(request: GenerateRequest): Promise<GenerateResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/generate-tests`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`)
    }

    const data: GenerateResponse = await response.json()
    return data
  } catch (error) {
    console.error('Error generating tests:', error)
    throw error instanceof Error ? error : new Error('Unknown error occurred')
  }
}

export async function connectToJira(payload: { baseUrl: string; email: string; apiToken: string }): Promise<{ success: boolean }> {
  try {
    const res = await fetch(`${API_BASE_URL}/jira/connect`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: 'Unknown error' }))
      throw new Error(err.error || `HTTP error ${res.status}`)
    }

    return await res.json()
  } catch (error) {
    console.error('Error connecting to Jira:', error)
    throw error instanceof Error ? error : new Error('Unknown error')
  }
}

export async function fetchJiraStories(payload: { baseUrl: string; email: string; apiToken: string; jql?: string }) {
  try {
    const res = await fetch(`${API_BASE_URL}/jira/stories`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: 'Unknown error' }))
      throw new Error(err.error || `HTTP error ${res.status}`)
    }

    return await res.json()
  } catch (error) {
    console.error('Error fetching Jira stories:', error)
    throw error instanceof Error ? error : new Error('Unknown error')
  }
}

export async function fetchJiraStoryDetails(payload: { baseUrl: string; email: string; apiToken: string; issueIdOrKey: string }) {
  try {
    const res = await fetch(`${API_BASE_URL}/jira/stories/details`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: 'Unknown error' }))
      throw new Error(err.error || `HTTP error ${res.status}`)
    }

    return await res.json()
  } catch (error) {
    console.error('Error fetching Jira story details:', error)
    throw error instanceof Error ? error : new Error('Unknown error')
  }
}