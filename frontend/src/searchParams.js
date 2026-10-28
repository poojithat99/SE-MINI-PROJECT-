/** Build the query string shared by keyword and semantic document searches. */
export function buildSearchParams({
  query,
  page = 1,
  category = '',
  fileType = '',
  dateFrom = '',
  dateTo = '',
}) {
  const params = new URLSearchParams({
    q: query.trim(),
    page: String(page),
  })

  if (category) params.set('category', category)
  if (fileType) params.set('file_type', fileType)
  if (dateFrom) params.set('date_from', dateFrom)
  if (dateTo) params.set('date_to', dateTo)

  return params.toString()
}
