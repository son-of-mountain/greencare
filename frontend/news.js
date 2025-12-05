// Gestion des actualités RSE
const API_URL = 'https://greencare-backend.onrender.com/api';

let allNews = [];
let currentFilter = 'all';

// Charger les actualités
async function loadNews(category = null) {
    try {
        const url = category && category !== 'all' 
            ? `${API_URL}/news?category=${category}` 
            : `${API_URL}/news`;
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('Erreur réseau');
        
        allNews = await response.json();
        displayNews(allNews);
    } catch (error) {
        console.error('Erreur:', error);
        document.getElementById('news-grid').innerHTML = 
            '<p style="text-align: center; color: #e74c3c;">Erreur de chargement des actualités</p>';
    }
}

// Afficher les actualités
function displayNews(newsArray) {
    const grid = document.getElementById('news-grid');
    
    if (newsArray.length === 0) {
        grid.innerHTML = '<p style="text-align: center; color: #666;">Aucune actualité disponible</p>';
        return;
    }
    
    grid.innerHTML = newsArray.map(news => `
        <div class="news-card" onclick="window.open('${news.image_url}', '_blank')">
            <img src="${news.image_url || 'https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800'}" 
                 alt="${news.title}" 
                 class="news-image"
                 onerror="this.src='https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800'">
            <div class="news-content">
                <div class="news-meta">
                    <span class="news-category category-${news.category}">
                        ${getCategoryLabel(news.category)}
                    </span>
                    <span class="news-country">
                        ${getCountryFlag(news.country)} ${news.country}
                    </span>
                </div>
                <h3 class="news-title">${news.title}</h3>
                <p class="news-description">${news.description}</p>
                <div class="news-footer">
                    <span>${news.source || 'Source non spécifiée'}</span>
                    <span>${formatDate(news.date)}</span>
                </div>
            </div>
        </div>
    `).join('');
}

// Obtenir le label de catégorie
function getCategoryLabel(category) {
    const labels = {
        'energie': '⚡ Énergie',
        'dechets': '♻️ Déchets',
        'innovation': '💡 Innovation',
        'social': '👥 Social'
    };
    return labels[category] || category;
}

// Obtenir le drapeau du pays
function getCountryFlag(country) {
    const flags = {
        'France': '🇫🇷',
        'Singapour': '🇸🇬',
        'Danemark': '🇩🇰',
        'Royaume-Uni': '🇬🇧',
        'Japon': '🇯🇵',
        'Canada': '🇨🇦',
        'Allemagne': '🇩🇪',
        'Espagne': '🇪🇸'
    };
    return flags[country] || '🌍';
}

// Formater la date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', options);
}

// Gestion des filtres
document.addEventListener('DOMContentLoaded', () => {
    // Charger les actualités
    loadNews();
    
    // Initialiser les données si nécessaire
    initializeNewsData();
    
    // Gérer les filtres
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Retirer la classe active de tous les boutons
            filterButtons.forEach(b => b.classList.remove('active'));
            
            // Ajouter la classe active au bouton cliqué
            btn.classList.add('active');
            
            // Filtrer les actualités
            const category = btn.dataset.category;
            currentFilter = category;
            
            if (category === 'all') {
                displayNews(allNews);
            } else {
                const filtered = allNews.filter(news => news.category === category);
                displayNews(filtered);
            }
        });
    });
});

// Initialiser les données de démo
async function initializeNewsData() {
    try {
        const response = await fetch(`${API_URL}/news/init`, {
            method: 'POST'
        });
        const data = await response.json();
        console.log(data.message);
    } catch (error) {
        console.log('Données déjà initialisées ou erreur:', error);
    }
}
