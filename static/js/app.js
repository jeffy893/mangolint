/**
 * Mangolint - Real-time Cultural Linting
 * Debounced text analysis with visual overlays
 */

const textEditor = document.getElementById('textEditor');
const highlightLayer = document.getElementById('highlightLayer');
const charCount = document.getElementById('charCount');
const wordCount = document.getElementById('wordCount');
const analyzeBtn = document.getElementById('analyzeBtn');
const entitiesPanel = document.getElementById('entitiesPanel');

// Store current entities for reference
let currentEntities = [];
let debounceTimer = null;
let lastAnalyzedText = ''; // Cache last analyzed text to avoid duplicate calls
let isAnalyzing = false; // Prevent concurrent API calls

/**
 * Debounce function - delays execution until after wait time
 */
function debounce(func, wait) {
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(debounceTimer);
            func(...args);
        };
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(later, wait);
    };
}

/**
 * Update character and word count
 */
function updateCounts() {
    const text = textEditor.value;
    const chars = text.length;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    
    charCount.textContent = `${chars} character${chars !== 1 ? 's' : ''}`;
    wordCount.textContent = `${words} word${words !== 1 ? 's' : ''}`;
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Create highlighted overlay with underlined suggestions
 */
function createHighlightOverlay(text, entities) {
    if (!entities || entities.length === 0) {
        highlightLayer.innerHTML = escapeHtml(text);
        return;
    }
    
    // Sort entities by their position in text (first occurrence)
    const sortedEntities = entities.map(entity => {
        const index = text.toLowerCase().indexOf(entity.text.toLowerCase());
        return { ...entity, index };
    }).filter(e => e.index !== -1)
      .sort((a, b) => a.index - b.index);
    
    let highlightedText = '';
    let lastIndex = 0;
    
    // Track which positions have been highlighted to avoid duplicates
    const highlightedRanges = [];
    
    sortedEntities.forEach(entity => {
        // Find all occurrences of this entity
        const regex = new RegExp(`\\b${entity.text}\\b`, 'gi');
        let match;
        
        while ((match = regex.exec(text)) !== null) {
            const start = match.index;
            const end = start + match[0].length;
            
            // Check if this range overlaps with already highlighted ranges
            const overlaps = highlightedRanges.some(range => 
                (start >= range.start && start < range.end) ||
                (end > range.start && end <= range.end)
            );
            
            if (!overlaps) {
                highlightedRanges.push({ start, end, entity, matchText: match[0] });
            }
        }
    });
    
    // Sort ranges by start position
    highlightedRanges.sort((a, b) => a.start - b.start);
    
    // Build the highlighted HTML
    highlightedRanges.forEach(range => {
        // Add text before the match
        if (lastIndex < range.start) {
            highlightedText += escapeHtml(text.substring(lastIndex, range.start));
        }
        
        // Add highlighted match with underline
        const synonymCount = range.entity.indigenous_synonyms?.length || 0;
        const title = `${synonymCount} indigenous synonym${synonymCount !== 1 ? 's' : ''} available`;
        
        highlightedText += `<span class="highlighted-text type-${range.entity.type}" title="${title}" data-entity="${escapeHtml(range.entity.text)}">${escapeHtml(range.matchText)}</span>`;
        
        lastIndex = range.end;
    });
    
    // Add remaining text
    if (lastIndex < text.length) {
        highlightedText += escapeHtml(text.substring(lastIndex));
    }
    
    highlightLayer.innerHTML = highlightedText;
    
    // Add click handlers to highlighted spans
    document.querySelectorAll('.highlighted-text').forEach(span => {
        span.addEventListener('click', (e) => {
            const entityText = e.target.getAttribute('data-entity');
            scrollToEntity(entityText);
        });
    });
}

/**
 * Scroll to entity in sidebar
 */
function scrollToEntity(entityText) {
    const entityCards = document.querySelectorAll('.entity-card');
    entityCards.forEach(card => {
        const cardText = card.querySelector('.entity-text')?.textContent;
        if (cardText && cardText.toLowerCase() === entityText.toLowerCase()) {
            card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            card.style.animation = 'pulse 0.5s ease-in-out';
            setTimeout(() => {
                card.style.animation = '';
            }, 500);
        }
    });
}

/**
 * Lint text by sending to /lint endpoint
 */
async function lintText(text) {
    if (!text || text.trim().length < 3) {
        currentEntities = [];
        highlightLayer.innerHTML = escapeHtml(text);
        displayEntities([]);
        lastAnalyzedText = text;
        return;
    }
    
    // Skip if already analyzing or text hasn't changed
    if (isAnalyzing || text === lastAnalyzedText) {
        return;
    }
    
    isAnalyzing = true;
    lastAnalyzedText = text;
    
    // Show analyzing indicator
    analyzeBtn.textContent = 'Analyzing...';
    analyzeBtn.disabled = true;
    
    try {
        const response = await fetch('/lint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text })
        });
        
        if (!response.ok) {
            console.error('Lint request failed:', response.statusText);
            return;
        }
        
        const data = await response.json();
        
        if (data.success && data.entities) {
            currentEntities = data.entities;
            createHighlightOverlay(text, data.entities);
            displayEntities(data.entities);
            
            // Log cache status for debugging
            if (data.cached) {
                console.log('✓ Result from cache');
            } else {
                console.log('→ Fresh analysis from Bedrock');
            }
        }
        
    } catch (error) {
        console.error('Linting error:', error);
    } finally {
        isAnalyzing = false;
        analyzeBtn.textContent = 'Analyze Text';
        analyzeBtn.disabled = false;
    }
}

/**
 * Debounced lint function (1500ms delay - increased for better performance)
 */
const debouncedLint = debounce((text) => {
    lintText(text);
}, 1500);

/**
 * Handle text editor input
 */
textEditor.addEventListener('input', () => {
    const text = textEditor.value;
    updateCounts();
    
    // Keep existing highlights while typing (don't clear them)
    // Only update if we don't have highlights yet
    if (currentEntities.length === 0) {
        highlightLayer.innerHTML = escapeHtml(text);
    }
    
    // Trigger debounced lint
    debouncedLint(text);
});

/**
 * Handle text editor keyup for real-time linting
 */
textEditor.addEventListener('keyup', (e) => {
    // Skip if it's just navigation keys
    const navigationKeys = ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'];
    if (navigationKeys.includes(e.key)) {
        return;
    }
    
    const text = textEditor.value;
    debouncedLint(text);
});

/**
 * Analyze button handler (immediate analysis)
 */
analyzeBtn.addEventListener('click', async () => {
    const text = textEditor.value.trim();
    
    if (!text) {
        alert('Please enter some text to analyze');
        return;
    }
    
    analyzeBtn.textContent = 'Analyzing...';
    analyzeBtn.disabled = true;
    
    try {
        // Cancel any pending debounced calls
        clearTimeout(debounceTimer);
        
        await lintText(text);
        
    } catch (error) {
        console.error('Analysis error:', error);
        alert('Error analyzing text. Please try again.');
    } finally {
        analyzeBtn.textContent = 'Analyze Text';
        analyzeBtn.disabled = false;
    }
});

/**
 * Display detected entities in sidebar
 */
function displayEntities(entities) {
    if (!entities || entities.length === 0) {
        entitiesPanel.innerHTML = `
            <div class="empty-state">
                <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                    <path d="M2 17l10 5 10-5"/>
                    <path d="M2 12l10 5 10-5"/>
                </svg>
                <p>No entities detected yet</p>
                <p class="empty-hint">Type or paste text to see cultural insights</p>
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

// Initialize
updateCounts();

console.log('Mangolint app.js loaded - Real-time linting enabled');
