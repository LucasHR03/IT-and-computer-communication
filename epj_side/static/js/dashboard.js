// ------------------------------
//   DATA & INITIALISERING
// ------------------------------
let patients = [];
let journalNotes = [];
let diagnoses = [];
let allergies = [];
let medications = [];
let auditLog = [];

const currentUser = {
  name: "Dr. Hansen",
  role: "Læge",
  id: "user001"
};

// ------------------------------
//   AUDIT LOG
// ------------------------------
function logAudit(action, details = '') {
  const entry = {
    timestamp: new Date().toLocaleString('da-DK'),
    user: currentUser.name,
    role: currentUser.role,
    action,
    details
  };
  auditLog.push(entry);
  renderAuditLog();
}

function renderAuditLog() {
  const container = document.getElementById('audit-list');
  if (!container) return;
  container.innerHTML = auditLog.slice(-50).reverse().map(entry => `
    <li class="audit-entry">
      <strong>${entry.timestamp}</strong> - ${entry.user} (${entry.role})<br>
      <strong>Handling:</strong> ${entry.action}
      ${entry.details ? `<br><strong>Detaljer:</strong> ${entry.details}` : ''}
    </li>
  `).join('');
}

function clearAuditLog() {
  if (confirm("Er du sikker på, at du vil rydde auditloggen?")) {
    auditLog = [];
    renderAuditLog();
    alert("Auditlog er ryddet.");
  }
}

// ------------------------------
//   CPR VALIDATION
// ------------------------------
function validateCPR(cpr) {
  return /^\d{6}-\d{4}$/.test(cpr);
}

function formatCPR(input) {
  let value = input.value.replace(/\D/g, '');
  if (value.length > 6) value = value.substring(0, 6) + '-' + value.substring(6, 10);
  input.value = value;
}

// ------------------------------
//   NAVIGATION
// ------------------------------
function showSection(sectionName) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const section = document.getElementById(sectionName);
  if (section) section.classList.add('active');
  const btn = document.querySelector(`.nav-btn[data-section="${sectionName}"]`);
  if (btn) btn.classList.add('active');
  logAudit(`Åbnede sektion: ${sectionName}`);
}

// ------------------------------
//   PATIENTER
// ------------------------------
function addPatient(e) {
  e.preventDefault();
  const cpr = document.getElementById('cpr').value;
  const errorDiv = document.getElementById('cpr-error');

  if (!validateCPR(cpr)) {
    errorDiv.textContent = 'CPR skal være i formatet 123456-7890';
    return;
  }

  if (patients.find(p => p.cpr === cpr)) {
    errorDiv.textContent = 'Patient med dette CPR findes allerede';
    return;
  }

  errorDiv.textContent = '';

  const patient = {
    id: Date.now(),
    cpr,
    navn: document.getElementById('navn').value,
    kontakt: document.getElementById('kontakt').value,
    paarorende: document.getElementById('paarorende').value,
    samtykke: document.getElementById('samtykke').value,
    created: new Date().toLocaleString('da-DK')
  };

  patients.push(patient);
  renderPatients();
  document.getElementById('patient-form').reset();
  logAudit('Patient tilføjet', `CPR: ${cpr}, Navn: ${patient.navn}`);
}

function withdrawConsent(id) {
  const patient = patients.find(p => p.id === id);
  if (!patient) return;
  patient.samtykke = 'tilbagetrukket';
  patient.consentWithdrawn = new Date().toLocaleString('da-DK');
  renderPatients();
  logAudit('Samtykke tilbagetrukket', `Patient: ${patient.navn} (${patient.cpr})`);
}

function renderPatients() {
  const container = document.getElementById('patient-list');
  if (!container) return;
  container.innerHTML = patients.map(p => `
    <li>
      <strong>${p.navn}</strong> (CPR: ${p.cpr})<br>
      <strong>Kontakt:</strong> ${p.kontakt} | <strong>Pårørende:</strong> ${p.paarorende || 'Ikke angivet'}<br>
      <strong>Samtykke:</strong> <span class="status-${p.samtykke}">${p.samtykke}</span>
      ${p.samtykke === 'ja' ? `<button class="withdraw-btn" onclick="withdrawConsent(${p.id})">Tilbagetræk samtykke</button>` : ''}
      <br><small>Oprettet: ${p.created}</small>
      ${p.consentWithdrawn ? `<br><small>Tilbagetrukket: ${p.consentWithdrawn}</small>` : ''}
    </li>
  `).join('');
}

// ------------------------------
//   EVENT LISTENERS
// ------------------------------
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('patient-form');
  if (form) form.addEventListener('submit', addPatient);

  document.querySelectorAll('input[maxlength="11"]').forEach(i => 
    i.addEventListener('input', () => formatCPR(i))
  );

  document.querySelectorAll('.nav-btn').forEach(b => 
    b.addEventListener('click', () => showSection(b.dataset.section))
  );

 const clearBtn = document.getElementById('clear-audit');
  if (clearBtn) clearBtn.addEventListener('click', clearAuditLog);

  logAudit('System startet', 'Bruger loggede ind');
  renderAuditLog();
});
