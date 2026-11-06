// Fills the right side of the navigation bar on the static pages with the
// current Django session user (or Login / Register links) and handles logout.
(function () {
  const slot = document.getElementById('nav-auth');
  if (!slot) return;

  function csrfToken() {
    const row = document.cookie.split('; ').find((c) => c.startsWith('csrftoken='));
    return row ? decodeURIComponent(row.split('=')[1]) : '';
  }

  function renderGuest() {
    slot.innerHTML =
      '<a class="nav-link" href="/login">Login</a>' +
      '<a class="btn btn-accent btn-sm" href="/register">Register</a>';
  }

  function renderUser(name) {
    slot.innerHTML = '';
    const user = document.createElement('span');
    user.className = 'nav-user';
    const avatar = document.createElement('span');
    avatar.className = 'avatar';
    avatar.textContent = name.slice(0, 1).toUpperCase();
    user.append(avatar, document.createTextNode(name));
    const logout = document.createElement('button');
    logout.className = 'btn btn-outline btn-sm';
    logout.textContent = 'Logout';
    logout.addEventListener('click', async () => {
      window.alert('Logging out ' + name + '...');
      await fetch('/djangoapp/logout', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'X-CSRFToken': csrfToken() },
      });
      window.location.href = '/';
    });
    slot.append(user, logout);
  }

  fetch('/djangoapp/me', { credentials: 'same-origin' })
    .then((r) => r.json())
    .then((me) => (me.isAuthenticated ? renderUser(me.userName) : renderGuest()))
    .catch(renderGuest);
})();
