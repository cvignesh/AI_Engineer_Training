import fetch from 'node-fetch'

function buildAuthHeader(email: string, apiToken: string) {
  const token = Buffer.from(`${email}:${apiToken}`).toString('base64')
  return `Basic ${token}`
}

async function toPlainTextFromADF(adf: any): Promise<string> {
  if (!adf || !adf.content) return ''

  const parts: string[] = []

  function walk(nodes: any[]) {
    for (const node of nodes) {
      if (node.type === 'text' && typeof node.text === 'string') {
        parts.push(node.text)
      }
      if (node.content) walk(node.content)
      if (node.type === 'paragraph' || node.type === 'heading') parts.push('\n')
      if (node.type === 'listItem') parts.push('\n')
    }
  }

  walk(adf.content)
  return parts.join(' ').replace(/\s+\n\s+/g, '\n').trim()
}

export async function validateAuth(baseUrl: string, email: string, apiToken: string): Promise<boolean> {
  const url = `${baseUrl.replace(/\/$/, '')}/rest/api/3/myself`
  const res = await fetch(url, {
    method: 'GET',
    headers: {
      Authorization: buildAuthHeader(email, apiToken),
      Accept: 'application/json'
    }
  })

  return res.ok
}

export async function searchStories(baseUrl: string, email: string, apiToken: string, jql?: string): Promise<any> {
  const q = encodeURIComponent(jql || 'issuetype=Story ORDER BY updated DESC')
  const url = `${baseUrl.replace(/\/$/, '')}/rest/api/3/search?jql=${q}&maxResults=50&fields=summary`
  const res = await fetch(url, {
    method: 'GET',
    headers: {
      Authorization: buildAuthHeader(email, apiToken),
      Accept: 'application/json'
    }
  })

  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`Jira search failed: ${res.status} ${text}`)
  }

  const data = await res.json()
  return data
}

export async function getIssueDetails(baseUrl: string, email: string, apiToken: string, issueIdOrKey: string): Promise<{ id: string, key: string, summary?: string, description?: string, acceptanceCriteria?: string }> {
  const url = `${baseUrl.replace(/\/$/, '')}/rest/api/3/issue/${encodeURIComponent(issueIdOrKey)}?fields=summary,description`
  const res = await fetch(url, {
    method: 'GET',
    headers: {
      Authorization: buildAuthHeader(email, apiToken),
      Accept: 'application/json'
    }
  })

  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`Jira issue fetch failed: ${res.status} ${text}`)
  }

  const data: any = await res.json()
  const fields = data.fields || {}

  let description = ''
  if (typeof fields.description === 'string') {
    description = fields.description
  } else if (typeof fields.description === 'object') {
    // Try to convert ADF to plain text
    description = await toPlainTextFromADF(fields.description)
  }

  // Try extract Acceptance Criteria heuristically
  let acceptanceCriteria = ''
  if (description) {
    const acMatch = description.match(/(?:Acceptance Criteria|Acceptance criterion|AC)[:\-\s]*([\s\S]{1,2000})/i)
    if (acMatch) {
      acceptanceCriteria = acMatch[1].trim()
    }
  }

  return {
    id: data.id,
    key: data.key,
    summary: fields.summary,
    description: description,
    acceptanceCriteria: acceptanceCriteria
  }
}

export default {
  validateAuth,
  searchStories,
  getIssueDetails
}
