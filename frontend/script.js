const API_URL = '/api';

// Charger les actions
async function loadActions() {
    const container = document.getElementById('actions-list');
    if(!container) return;

    // Récupérer les actions triées par score
    const res = await fetch(`${API_URL}/actions?sort=score`);
    const actions = await res.json();

    container.innerHTML = actions.map(action => `
        <div class="card">
            <div class="card-header">
                <h3>${action.title}</h3>
                <span class="badge">${action.category}</span>
            </div>
            <p>${action.description}</p>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
                <span class="score">Score: ${action.score.toFixed(1)}</span>
                <div>
                    <button class="vote-btn" onclick="vote(${action.id}, 1)">👍 Pour</button>
                    <button class="vote-btn" onclick="vote(${action.id}, -1)">👎 Contre</button>
                </div>
            </div>
            <small style="opacity:0.7">Service: ${action.service_id}</small>
        </div>
    `).join('');
}

// Voter
async function vote(id, val) {
    // Simulation d'un utilisateur connecté (Pour POC)
    const role = document.getElementById('user-role').value;
    const agentId = "USER_" + Math.floor(Math.random() * 1000); 

    const res = await fetch(`${API_URL}/actions/${id}/vote`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ agent_id: agentId, role: role, value: val })
    });

    if(res.ok) {
        loadActions(); // Recharger pour voir le nouveau score
    } else {
        alert("Erreur lors du vote");
    }
}

// Proposer une action
async function submitAction(e) {
    e.preventDefault();
    const data = {
        title: document.getElementById('title').value,
        description: document.getElementById('desc').value,
        service_id: document.getElementById('service').value,
        category: document.getElementById('cat').value
    };

    const res = await fetch(`${API_URL}/actions`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });

    if(res.ok) {
        window.location.href = 'index.html';
    } else {
        alert("Erreur formulaire");
    }
}

// ... (code existant loadActions, vote, submitAction) ...

// Charger les KPIs pour le dashboard
async function loadDashboard() {
    const kwhEl = document.getElementById('kpi-kwh');
    if(!kwhEl) return; // Pas sur la page dashboard

    try {
        const res = await fetch(`${API_URL}/kpis`);
        const data = await res.json();

        // Animation simple des chiffres ou affichage direct
        document.getElementById('kpi-kwh').textContent = data.total_kwh.toLocaleString();
        document.getElementById('kpi-euro').textContent = data.total_euro.toLocaleString() + ' €';
        document.getElementById('kpi-co2').textContent = data.total_co2.toLocaleString();
        document.getElementById('kpi-count').textContent = data.actions_count;
    } catch(e) {
        console.error("Erreur chargement KPIs", e);
    }
}

// Télécharger le CSV
function downloadCSV() {
    window.location.href = `${API_URL}/exports/kpis.csv`;
}
