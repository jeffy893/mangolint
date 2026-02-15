const textEditor = document.getElementById('textEditor');
const charCount = document.getElementById('charCount');
const wordCount = document.getElementById('wordCount');
const analyzeBtn = document.getElementById('analyzeBtn');
const entitiesPanel = document.getElementById('entitiesPanel');

// Update character and word count
function updateCounts() {
    const text = textEditor.value;
    const chars = text.length;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    
    charCount.textContent = `${chars} character${chars !== 1 ? 's' : ''}`;
    wordCount.textContent = `${words} word${words !== 1 ? 's' : ''}`;
}

textEditor.addEventListener('input', updateCounts);

// Analyze button handler
analyzeBtn.addEventListener('click', async () => {
    const text = textEditor.value.trim();
    
    if (!text) {
        alert('Please enter some text to analyze');
        return;
    }
    
    analyzeBtn.textContent = 'Analyzing...';
    analyzeBtn.disabled = true;
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        displayEntities(data.entities);
        
    } catch (error) {
        console.error('Analysis error:', error);
        alert('Error analyzing text. Please try again.');
    } finally {
        analyzeBtn.textContent = 'Analyze Text';
        analyzeBtn.disabled = false;
    }
});

// Display detected entities
function displayEntities(entities) {
    if (!entities || entities.length === 0) {
        entitiesPanel.innerHTML = `
            <div class="empty-state">
                <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                    <path d="M2 17l10 5 10-5"/>
                    <path d="M2 12l10 5 10-5"/>
                </svg>
                <p>No cultural entities detected</p>
            </div>
        `;
        return;
    }
    
    entitiesPanel.innerHTML = entities.map(entity => {
        const synonymsHtml = entity.indigenous_synonyms && entity.indigenous_synonyms.length > 0
            ? `
                <div class="synonyms-section">
                    <strong>Indigenous Synonyms:</strong>
                    ${entity.indigenous_synonyms.map(syn => `
                        <div class="synonym-item">
                            <div class="synonym-header">
                                <span class="synonym-term">${syn.term}</span>
                                <span class="synonym-language">${syn.language}</span>
                            </div>
                            <span class="synonym-culture">${syn.culture}</span>
                            <p class="synonym-definition">${syn.definition}</p>
                            ${syn.context ? `<p class="synonym-context"><em>Context:</em> ${syn.context}</p>` : ''}
                        </div>
                    `).join('')}
                </div>
            `
            : '';
        
        const brandInsightsHtml = entity.brand_insights
            ? `
                <div class="insights-section">
                    <strong>Brand Insights:</strong>
                    <p>${entity.brand_insights}</p>
                </div>
            `
            : '';
        
        const traditionalUsesHtml = entity.traditional_uses
            ? `
                <div class="traditional-section">
                    <strong>Traditional Uses:</strong>
                    <p>${entity.traditional_uses}</p>
                </div>
            `
            : '';
        
        const authenticityHtml = entity.authenticity_markers && entity.authenticity_markers.length > 0
            ? `
                <div class="authenticity-section">
                    <strong>Authenticity Markers:</strong>
                    <ul class="authenticity-list">
                        ${entity.authenticity_markers.map(marker => `<li>${marker}</li>`).join('')}
                    </ul>
                </div>
            `
            : '';
        
        return `
            <div class="entity-card">
                <div class="entity-header">
                    <span class="entity-text">${entity.text}</span>
                    <span class="entity-badge type-${entity.type}">${entity.category || entity.type}</span>
                </div>
                <div class="entity-description">${entity.description || 'No description available'}</div>
                ${synonymsHtml}
                ${brandInsightsHtml}
                ${traditionalUsesHtml}
                ${authenticityHtml}
            </div>
        `;
    }).join('');
}

console.log('Mangolint loaded');
