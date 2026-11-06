// Thin wrapper around fetch for the Django JSON API (same origin, session cookie auth).

function getCookie(name) {
  const match = document.cookie.split('; ').find((row) => row.startsWith(`${name}=`));
  return match ? decodeURIComponent(match.split('=')[1]) : '';
}

export class ApiError extends Error {
  constructor(status, message, errors = {}) {
    super(message);
    this.status = status;
    this.errors = errors;
  }
}

async function request(path, { method = 'GET', body } = {}) {
  const headers = { Accept: 'application/json' };
  if (method !== 'GET') {
    headers['Content-Type'] = 'application/json';
    headers['X-CSRFToken'] = getCookie('csrftoken');
  }
  let response;
  try {
    response = await fetch(path, {
      method,
      headers,
      credentials: 'same-origin',
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch {
    throw new ApiError(0, 'Network error: the server could not be reached.');
  }
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new ApiError(response.status, data.error || `Request failed (${response.status})`, data.errors);
  return data;
}

export const api = {
  me: () => request('/djangoapp/me'),
  login: (userName, password) => request('/djangoapp/login', { method: 'POST', body: { userName, password } }),
  logout: () => request('/djangoapp/logout', { method: 'POST' }),
  register: (form) => request('/djangoapp/register', { method: 'POST', body: form }),
  dealers: (state) => request(state && state !== 'All' ? `/djangoapp/get_dealers/${encodeURIComponent(state)}` : '/djangoapp/get_dealers'),
  dealer: (id) => request(`/djangoapp/dealer/${id}`),
  reviews: (id) => request(`/djangoapp/reviews/dealer/${id}`),
  addReview: (review) => request('/djangoapp/add_review', { method: 'POST', body: review }),
  cars: () => request('/djangoapp/get_cars'),
};
