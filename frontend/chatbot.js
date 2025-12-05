// Chatbot Vert - Assistant RSE Symbolique

const CHATBOT_RESPONSES = {
    "rse": "La RSE (Responsabilité Sociétale des Entreprises) dans les hôpitaux englobe les actions pour réduire l'impact environnemental : sobriété énergétique, gestion des déchets, réduction CO2, et bien-être des agents. 🌱",
    
    "energie": "Les hôpitaux consomment énormément d'énergie ! Des actions simples peuvent faire la différence : extinction des équipements en veille, optimisation du chauffage, LED, panneaux solaires... ⚡",
    
    "dechets": "Les hôpitaux produisent différents types de déchets : DASRI (Déchets d'Activités de Soins à Risques Infectieux), déchets ménagers, recyclables. Un tri rigoureux peut réduire les coûts et l'impact environnemental ! ♻️",
    
    "vote": "Le système de vote pondéré de GreenCare permet à chaque agent de prioriser les actions. Les soignants ont un coefficient x1.5, les cadres x1.0, et la direction x0.8 pour refléter leur connaissance du terrain. 🗳️",
    
    "impact": "GreenCare mesure l'impact en kWh économisés, euros économisés et kg de CO2 évités. Chaque action votée contribue à améliorer le score global de l'établissement ! 📊",
    
    "proposer": "Vous pouvez proposer de nouvelles actions RSE ! Décrivez votre idée, le service concerné, et la catégorie. La communauté votera ensuite pour prioriser les meilleures initiatives. 💡",
    
    "numih": "Numih France est l'acteur public du numérique en santé. GreenCare est conçu 'by design' pour s'intégrer nativement dans dh, leur futur ERP hospitalier souverain. 🏥",
    
    "souverainete": "GreenCare respecte les standards de souveraineté : HDS (Hébergement de Données de Santé), SecNumCloud, et les référentiels Métamorph'OSE et LUCIE 26000. 🔒",
    
    "actions": "Les actions sont classées par score. Plus une action reçoit de votes (surtout des soignants), plus son score augmente. Consultez la page Actions pour voir les priorités ! 🎯",
    
    "dashboard": "Le dashboard Impact affiche les KPIs globaux : économies d'énergie, réduction CO2, économies financières. Ces données sont exportables en CSV pour le pilotage. 📈",
    
    "bonjour": "Bonjour ! 👋 Je suis Vert, votre assistant RSE. Je peux répondre à vos questions sur la RSE hospitalière, GreenCare, les actions, les votes... N'hésitez pas !",
    
    "merci": "De rien ! C'est un plaisir de vous aider. Ensemble pour une santé durable ! 🌿💚",
    
    "aide": "Je peux vous parler de : RSE hospitalière, gestion énergie/déchets, système de vote, impact environnemental, Numih, souveraineté, actions prioritaires... Posez-moi vos questions ! 🤔"
};

const SUGGESTIONS = [
    "Qu'est-ce que la RSE ?",
    "Comment voter ?",
    "Gestion des déchets",
    "Économies d'énergie",
    "C'est quoi Numih ?"
];

let chatbotOpen = false;
let chatMessages = [];

function initChatbot() {
    // Message de bienvenue
    addBotMessage("Bonjour ! 👋 Je suis Vert, votre assistant RSE. Comment puis-je vous aider aujourd'hui ?");
    updateSuggestions();
}

function toggleChatbot() {
    chatbotOpen = !chatbotOpen;
    const window = document.getElementById('chatbotWindow');
    const toggle = document.getElementById('chatbotToggle');
    
    if (chatbotOpen) {
        window.classList.add('active');
        toggle.textContent = '✕';
    } else {
        window.classList.remove('active');
        toggle.textContent = '🌱';
    }
}

function addBotMessage(text) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message bot';
    messageDiv.innerHTML = `
        <div class="message-avatar">🌱</div>
        <div class="message-bubble">${text}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addUserMessage(text) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message user';
    messageDiv.innerHTML = `
        <div class="message-bubble">${text}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message bot';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">🌱</div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    scrollToBottom();
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

function getBotResponse(userMessage) {
    const lowerMessage = userMessage.toLowerCase();
    
    // Chercher une correspondance dans les réponses
    for (const [keyword, response] of Object.entries(CHATBOT_RESPONSES)) {
        if (lowerMessage.includes(keyword)) {
            return response;
        }
    }
    
    // Réponse par défaut
    return "Je ne suis pas sûr de comprendre votre question. Essayez de me demander : Qu'est-ce que la RSE ? Comment voter ? Gestion des déchets ? 🤔";
}

function handleUserInput() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Afficher le message utilisateur
    addUserMessage(message);
    input.value = '';
    
    // Afficher l'indicateur de frappe
    showTypingIndicator();
    
    // Simuler un délai de réponse
    setTimeout(() => {
        removeTypingIndicator();
        const response = getBotResponse(message);
        addBotMessage(response);
        updateSuggestions();
    }, 1000 + Math.random() * 1000);
}

function handleSuggestion(text) {
    addUserMessage(text);
    showTypingIndicator();
    
    setTimeout(() => {
        removeTypingIndicator();
        const response = getBotResponse(text);
        addBotMessage(response);
        updateSuggestions();
    }, 800);
}

function updateSuggestions() {
    const container = document.getElementById('chatSuggestions');
    container.innerHTML = SUGGESTIONS.map(s => 
        `<button class="suggestion-btn" onclick="handleSuggestion('${s}')">${s}</button>`
    ).join('');
}

function scrollToBottom() {
    const container = document.getElementById('chatMessages');
    container.scrollTop = container.scrollHeight;
}

// Gérer l'entrée avec la touche Enter
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('chatInput');
    if (input) {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                handleUserInput();
            }
        });
    }
});
