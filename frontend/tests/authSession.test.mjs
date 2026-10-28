import assert from 'node:assert/strict'
import test from 'node:test'
import { revokeAccessToken } from '../src/authSession.js'

test('logout revokes token by POSTing to backend with bearer header', async () => {
  const calls = []
  await revokeAccessToken('test-token', 'http://127.0.0.1:8000', async (...args) => {
    calls.push(args)
    return { ok: true, status: 204 }
  })
  assert.deepEqual(calls, [[
    'http://127.0.0.1:8000/api/auth/logout',
    { method: 'POST', headers: { Authorization: 'Bearer test-token' } },
  ]])
})

test('logout skips backend request when there is no token', async () => {
  await revokeAccessToken(null, 'http://127.0.0.1:8000', () => {
    throw new Error('Unexpected request')
  })
})

test('logout surfaces unsuccessful server response', async () => {
  await assert.rejects(
    revokeAccessToken('test-token', 'http://127.0.0.1:8000', async () => ({ ok: false, status: 503 })),
    /HTTP 503/,
  )
})
