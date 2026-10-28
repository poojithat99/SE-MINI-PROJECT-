/** Ask the backend to invalidate the access token during logout. */
export async function revokeAccessToken(token, apiUrl, fetcher = fetch) {
  if (!token) return

  const response = await fetcher(`${apiUrl}/api/auth/logout`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  })

  if (!response.ok) {
    throw new Error(`Server logout failed (HTTP ${response.status})`)
  }
}
