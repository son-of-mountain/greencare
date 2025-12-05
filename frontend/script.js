const API_URL = '/api';

// Charger les actions
async function loadActions() {
    const container = document.getElementById('actions-list');
    if(!container) return;

    // Récupérer les actions triées par score
    const res = await fetch(`${API_URL}/actions?sort=score`);
    const actions = await res.json();

    container.innerHTML = actions.map(action => `
        <div class="card instagram-card">
            ${action.image_url ? `
                <div class="instagram-image" style="background-image: url('${action.image_url}');"></div>
            ` : `
                <div class="instagram-image no-image">
                    <div class="placeholder-icon">🏥</div>
                </div>
            `}
            <div class="instagram-content">
                <div class="instagram-header">
                    <div class="action-title-section">
                        <h3 class="action-title">${action.title}</h3>
                        <span class="badge">${action.category}</span>
                    </div>
                    <span class="service-tag">📍 ${action.service_id}</span>
                </div>
                
                <p class="action-description">${action.description}</p>
                
                <div class="instagram-stats">
                    <div class="stat-item">
                        <span class="stat-icon">⚡</span>
                        <span class="stat-value">${action.gain_kwh || 0} kWh</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-icon">💰</span>
                        <span class="stat-value">${action.gain_euro || 0} €</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-icon">🌍</span>
                        <span class="stat-value">${action.gain_co2 || 0} kg CO2</span>
                    </div>
                </div>
                
                <div class="instagram-footer">
                    <div class="score-display">
                        <span class="score-label">Score:</span>
                        <span class="score-value">${action.score.toFixed(1)}</span>
                    </div>
                    <div class="vote-buttons">
                        <button class="vote-btn vote-for" onclick="vote(${action.id}, 1)">
                            <span class="vote-icon">👍</span>
                            <span class="vote-text">Pour</span>
                        </button>
                        <button class="vote-btn vote-against" onclick="vote(${action.id}, -1)">
                            <span class="vote-icon">👎</span>
                            <span class="vote-text">Contre</span>
                        </button>
                    </div>
                </div>
            </div>
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
    
    // Gérer l'image
    let imageUrl = document.getElementById('image-url').value;
    const imageFile = document.getElementById('image').files[0];
    
    // Si un fichier est uploadé, le convertir en base64
    if (imageFile && !imageUrl) {
        imageUrl = await convertImageToBase64(imageFile);
    }
    
    const data = {
        title: document.getElementById('title').value,
        description: document.getElementById('desc').value,
        service_id: document.getElementById('service').value,
        category: document.getElementById('cat').value,
        image_url: imageUrl || null
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

// Convertir image en base64
function convertImageToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Preview de l'image
if (document.getElementById('image')) {
    document.getElementById('image').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const preview = document.getElementById('image-preview');
                const img = document.getElementById('preview-img');
                img.src = event.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });
    
    document.getElementById('image-url').addEventListener('input', function(e) {
        const url = e.target.value;
        if (url) {
            const preview = document.getElementById('image-preview');
            const img = document.getElementById('preview-img');
            img.src = url;
            preview.style.display = 'block';
        }
    });
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
