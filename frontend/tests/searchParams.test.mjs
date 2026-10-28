import assert from 'node:assert/strict'
import test from 'node:test'
import { buildSearchParams } from '../src/searchParams.js'

test('keyword search preserves page and encodes the search query', () => {
  const params = new URLSearchParams(buildSearchParams({query: '  artificial intelligence & docs  ', page: 3}))
  assert.equal(params.get('q'), 'artificial intelligence & docs')
  assert.equal(params.get('page'), '3')
})

test('semantic search includes category, file type and both date filters', () => {
  const params = new URLSearchParams(buildSearchParams({
    query: 'related documents',
    page: 2,
    category: 'Technology',
    fileType: 'pdf',
    dateFrom: '2026-10-01',
    dateTo: '2026-10-28',
  }))
  assert.deepEqual(Object.fromEntries(params), {
    q: 'related documents',
    page: '2',
    category: 'Technology',
    file_type: 'pdf',
    date_from: '2026-10-01',
    date_to: '2026-10-28',
  })
})

test('optional filters are omitted rather than sent empty', () => {
  const params = new URLSearchParams(buildSearchParams({query: 'science'}))
  assert.deepEqual(Object.fromEntries(params), {q: 'science', page: '1'})
})
