// ---- Config: base URL of the backend API ----
// When frontend is served BY FastAPI (same origin), '' works fine.
// If you ever host frontend separately, set this to e.g. 'https://api.puredispose.in'
const API_BASE = '';

function filterCards(cat, btn) {
  document.querySelectorAll('.ftab').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.prod-card').forEach(c => {
    c.style.display = (cat === 'all' || c.dataset.cat === cat) ? '' : 'none';
  });
}

// Sends an enquiry event to the backend (best-effort, non-blocking for the UI)
async function addToCart(name) {
  showToast('✓ ' + name + ' added to enquiry list!');
  try {
    await fetch(`${API_BASE}/api/enquiries`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_name: name })
    });
  } catch (err) {
    console.warn('Enquiry log failed (non-critical):', err);
  }
}

// Submits the "Get a Quote" phone number to the backend, saved in Postgres
async function submitOrder() {
  const phoneInput = document.getElementById('phone');
  const ph = phoneInput.value.trim();

  if (!/^\d{10}$/.test(ph)) {
    showToast('Please enter a valid 10-digit number.');
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone: ph })
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Request failed');
    }

    showToast("✓ Request received! We'll call you shortly.");
    phoneInput.value = '';
  } catch (err) {
    console.error(err);
    showToast('Something went wrong. Please try again.');
  }
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

const observer = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.style.opacity = '1'; });
}, { threshold: 0.1 });

document.querySelectorAll('.prod-card, .why-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transition = 'opacity .5s ease, transform .3s ease, box-shadow .3s ease';
  observer.observe(el);
});
