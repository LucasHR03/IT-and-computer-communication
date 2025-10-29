function openModal(id) {
  document.getElementById(id).classList.remove('hidden');
}

function closeModals() {
  document.querySelectorAll('.modal').forEach(m => m.classList.add('hidden'));
}

document.addEventListener('DOMContentLoaded', () => {
  const loginBtn = document.getElementById('btn-login');
  const registerBtn = document.getElementById('btn-register');
  const loginCancel = document.getElementById('login-cancel');
  const registerCancel = document.getElementById('register-cancel');

  // Åbn modaler
  loginBtn.addEventListener('click', () => openModal('modal-login'));
  registerBtn.addEventListener('click', () => openModal('modal-register'));

  // Luk modaler
  loginCancel.addEventListener('click', closeModals);
  registerCancel.addEventListener('click', closeModals);
});
