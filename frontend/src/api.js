export function removeToken() {
  localStorage.removeItem('token');
}

export async function login(username, password) {
  const res = await fetch('/api/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error);
  }
  localStorage.setItem('token', data.token);
}

export async function getMe() {
  const token = localStorage.getItem('token');
  if (!token) {
    return null;
  }
  try {
    const res = await fetch('/api/home/', {
      headers: { Authorization: 'Bearer ' + token },
    });
    if (!res.ok) {
      removeToken();
      return null;
    }
    return await res.json();
  } catch {
    return null;
  }
}