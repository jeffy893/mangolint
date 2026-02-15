/**
 * Mangolint - Real-time Cultural Linting with Tooltips
 */

const textEditor = document.getElementById('textEditor');
const highlightLayer = document.getElementById('highlightLayer');
const charCount = document.getElementById('charCount');
const wordCount = document.getElementById('wordCount');
const entityCount = document.getElementById('entityCount');
const analyzeBtn = document.getElementById('analyzeBtn');
const brandStatementSection = document.getElementById('brandStatementSection');
const brandStatementContent = document.getElementById('brandStatementContent');
const copyBrandBtn = document.getElementById('copyBrandBtn');
const entitiesSummary = document.getElementById('entitiesSummary');
const summaryCount = document.getElementById('summaryCount');
const summaryGrid = document.getElementById('summaryGrid');
const tooltip = document.getElementById('tooltip');

// Store current entities for reference
let currentEntities = [];
let debounceTimer = null;
let lastAnalyzedText = '';
let isAnalyzing = false;
let currentBrandStatement = '';

/**
 * Debounce function
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
 * Update character, word, and entity count
 */
function updateCounts() {
    const text = textEditor.value;
    const chars = text.length;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    
    charCount.textContent = `${chars} character${chars !== 1 ? 's' : ''}`;
    wordCount.textContent = `${words} word${words !== 1 ? 's' : ''}`;
    entityCount.textContent = `${currentEntities.length} entit${currentEntities.length !== 1 ? 'ies' : 'y'}`;
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
 * Show tooltip on hover
 */
function showTooltip(event, entity) {
    const tooltipTerm = tooltip.querySelector('.tooltip-term');
    const tooltipCategory = tooltip.querySelector('.tooltip-category');
    const tooltipDescription = tooltip.querySelector('.tooltip-description');
    const tooltipSynonyms = tooltip.querySelector('.tooltip-synonyms');
    
    // Set content
    tooltipTerm.textContent = entity.text;
    tooltipCategory.textContent = entity.category || 'ingredient';
    tooltipDescription.textContent = entity.description || 'No description available';
    
    // Set synonyms (show first 2 for tooltip brevity)
    const synonyms = entity.indigenous_synonyms || [];
    tooltipSynonyms.innerHTML = synonyms.slice(0, 2).map(syn => `
        <div class="tooltip-synonym">
            <span class="tooltip-synonym-term">${escapeHtml(syn.term)}</span>
            <span class="tooltip-synonym-lang">${escapeHtml(syn.language)}</span>
            <div class="tooltip-synonym-culture">${escapeHtml(syn.culture)}</div>
        </div>
    `).join('') + (synonyms.length > 2 ? `<div style="text-align: center; color: var(--text-muted); font-size: 0.8rem; margin-top: 8px;">+${synonyms.length - 2} more below</div>` : '');
    
    // Position tooltip
    const rect = event.target.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();
    
    let left = rect.left + (rect.width / 2) - (tooltipRect.width / 2);
    let top = rect.bottom + 10;
    
    // Keep tooltip on screen
    if (left < 10) left = 10;
    if (left + tooltipRect.width > window.innerWidth - 10) {
        left = window.innerWidth - tooltipRect.width - 10;
    }
    
    // If tooltip would go off bottom, show above
    if (top + tooltipRect.height > window.innerHeight - 10) {
        top = rect.top - tooltipRect.height - 10;
    }
    
    tooltip.style.left = `${left}px`;
    tooltip.style.top = `${top}px`;
    tooltip.style.display = 'block';
}

/**
 * Hide tooltip
 */
function hideTooltip() {
    tooltip.style.display = 'none';
}

/**
 * Create highlighted overlay with hover tooltips
 */
function createHighlightOverlay(text, entities) {
    // Always show the text in the highlight layer
    if (!entities || entities.length === 0) {
        highlightLayer.innerHTML = escapeHtml(text);
        highlightLayer.style.color = 'var(--text-primary)';
        return;
    }
    
    highlightLayer.style.color = 'var(--text-primary)';
    
    // Sort entities by their position in text
    const sortedEntities = entities.map(entity => {
        const index = text.toLowerCase().indexOf(entity.text.toLowerCase());
        return { ...entity, index };
    }).filter(e => e.index !== -1)
      .sort((a, b) => a.index - b.index);
    
    let highlightedText = '';
    let lastIndex = 0;
    
    // Track highlighted ranges
    const highlightedRanges = [];
    
    sortedEntities.forEach(entity => {
        const regex = new RegExp(`\\b${entity.text}\\b`, 'gi');
        let match;
        
        while ((match = regex.exec(text)) !== null) {
            const start = match.index;
            const end = start + match[0].length;
            
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
        if (lastIndex < range.start) {
            highlightedText += escapeHtml(text.substring(lastIndex, range.start));
        }
        
        const entityData = JSON.stringify(range.entity).replace(/"/g, '&quot;');
        highlightedText += `<span class="highlighted-text type-${range.entity.type}" data-entity='${entityData}'>${escapeHtml(range.matchText)}</span>`;
        
        lastIndex = range.end;
    });
    
    if (lastIndex < text.length) {
        highlightedText += escapeHtml(text.substring(lastIndex));
    }
    
    highlightLayer.innerHTML = highlightedText;
    
    // Add hover handlers
    document.querySelectorAll('.highlighted-text').forEach(span => {
        span.addEventListener('mouseenter', (e) => {
            const entityData = JSON.parse(e.target.getAttribute('data-entity'));
            showTooltip(e, entityData);
        });
        
        span.addEventListener('mouseleave', hideTooltip);
        
        span.addEventListener('click', (e) => {
            const entityText = JSON.parse(e.target.getAttribute('data-entity')).text;
            scrollToEntity(entityText);
        });
    });
}

/**
 * Scroll to entity in summary
 */
function scrollToEntity(entityText) {
    const entityCards = document.querySelectorAll('.entity-card');
    entityCards.forEach(card => {
        const cardText = card.querySelector('.entity-name')?.textContent;
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
 * Display entities in summary grid
 */
function displayEntitiesSummary(entities) {
    if (!entities || entities.length === 0) {
        entitiesSummary.style.display = 'none';
        return;
    }
    
    entitiesSummary.style.display = 'block';
    summaryCount.textContent = `${entities.length} ingredient${entities.length !== 1 ? 's' : ''} found`;
    
    summaryGrid.innerHTML = entities.map(entity => {
        const synonyms = entity.indigenous_synonyms || [];
        
        // Build synonyms section with full details
        const synonymsHtml = synonyms.length > 0 ? `
            <div class="card-section">
                <h4 class="card-section-title">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                    Indigenous Synonyms
                </h4>
                <div class="synonyms-list">
                    ${synonyms.map(syn => `
                        <div class="synonym-item">
                            <div class="synonym-header">
                                <span class="synonym-term">${escapeHtml(syn.term)}</span>
                                <span class="synonym-lang">${escapeHtml(syn.language)}</span>
                            </div>
                            <div class="synonym-culture">${escapeHtml(syn.culture)}</div>
                            <div class="synonym-definition">${escapeHtml(syn.definition)}</div>
                            ${syn.context ? `<div class="synonym-context"><strong>Context:</strong> ${escapeHtml(syn.context)}</div>` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        ` : '';
        
        // Brand insights section
        const brandInsightsHtml = entity.brand_insights ? `
            <div class="card-section">
                <h4 class="card-section-title">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path>
                    </svg>
                    Brand Insights
                </h4>
                <p class="card-text">${escapeHtml(entity.brand_insights)}</p>
            </div>
        ` : '';
        
        // Traditional uses section
        const traditionalUsesHtml = entity.traditional_uses ? `
            <div class="card-section">
                <h4 class="card-section-title">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                        <path d="M2 17l10 5 10-5"/>
                        <path d="M2 12l10 5 10-5"/>
                    </svg>
                    Traditional Uses
                </h4>
                <p class="card-text">${escapeHtml(entity.traditional_uses)}</p>
            </div>
        ` : '';
        
        // Authenticity markers section
        const authenticityHtml = entity.authenticity_markers && entity.authenticity_markers.length > 0 ? `
            <div class="card-section">
                <h4 class="card-section-title">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    Authenticity Markers
                </h4>
                <ul class="authenticity-list">
                    ${entity.authenticity_markers.map(marker => `<li>${escapeHtml(marker)}</li>`).join('')}
                </ul>
            </div>
        ` : '';
        
        return `
            <div class="entity-card">
                <div class="entity-card-header">
                    <span class="entity-name">${escapeHtml(entity.text)}</span>
                    <span class="entity-badge">${escapeHtml(entity.category || 'ingredient')}</span>
                </div>
                <p class="entity-description">${escapeHtml(entity.description || 'No description available')}</p>
                ${synonymsHtml}
                ${brandInsightsHtml}
                ${traditionalUsesHtml}
                ${authenticityHtml}
            </div>
        `;
    }).join('');
}

/**
 * Generate brand statement
 */
async function generateBrandStatement(text, entities) {
    if (!entities || entities.length === 0) {
        brandStatementSection.style.display = 'none';
        return;
    }
    
    brandStatementSection.style.display = 'block';
    brandStatementContent.innerHTML = '<p class="loading">Generating enhanced description...</p>';
    
    try {
        const response = await fetch('/generate-brand-statement', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text, entities })
        });
        
        if (!response.ok) {
            console.error('Brand statement generation failed:', response.statusText);
            brandStatementContent.innerHTML = '<p class="loading">Unable to generate brand statement</p>';
            return;
        }
        
        const data = await response.json();
        
        if (data.success && data.brand_statement) {
            currentBrandStatement = data.brand_statement;
            brandStatementContent.innerHTML = `<p class="enhanced-text">${escapeHtml(data.brand_statement)}</p>`;
            
            if (data.cached) {
                console.log('✓ Brand statement from cache');
            } else {
                console.log('→ Fresh brand statement generated');
            }
        } else {
            brandStatementContent.innerHTML = '<p class="loading">Unable to generate brand statement</p>';
        }
        
    } catch (error) {
        console.error('Brand statement generation error:', error);
        brandStatementContent.innerHTML = '<p class="loading">Error generating brand statement</p>';
    }
}

/**
 * Copy brand statement to clipboard
 */
copyBrandBtn.addEventListener('click', async () => {
    if (!currentBrandStatement) return;
    
    try {
        await navigator.clipboard.writeText(currentBrandStatement);
        
        const originalHTML = copyBrandBtn.innerHTML;
        copyBrandBtn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            Copied!
        `;
        
        setTimeout(() => {
            copyBrandBtn.innerHTML = originalHTML;
        }, 2000);
        
    } catch (error) {
        console.error('Failed to copy:', error);
    }
});

/**
 * Lint text
 */
async function lintText(text) {
    if (!text || text.trim().length < 3) {
        currentEntities = [];
        highlightLayer.innerHTML = escapeHtml(text);
        displayEntitiesSummary([]);
        brandStatementSection.style.display = 'none';
        lastAnalyzedText = text;
        updateCounts();
        return;
    }
    
    if (isAnalyzing || text === lastAnalyzedText) {
        return;
    }
    
    isAnalyzing = true;
    lastAnalyzedText = text;
    
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
            displayEntitiesSummary(data.entities);
            updateCounts();
            
            // Generate brand statement
            generateBrandStatement(text, data.entities);
            
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
        analyzeBtn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
            </svg>
            Analyze Text
        `;
        analyzeBtn.disabled = false;
    }
}

/**
 * Debounced lint function
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
    
    // Always update the highlight layer to show the text (without highlights)
    highlightLayer.innerHTML = escapeHtml(text);
    
    // Don't auto-analyze - wait for button click
});

/**
 * Analyze button handler
 */
analyzeBtn.addEventListener('click', async () => {
    const text = textEditor.value.trim();
    
    if (!text) {
        return;
    }
    
    // Clear any pending debounced calls
    clearTimeout(debounceTimer);
    
    // Reset last analyzed text to force new analysis
    lastAnalyzedText = '';
    
    await lintText(text);
});

// Initialize
updateCounts();

console.log('Mangolint loaded - Hover over highlighted words for cultural insights');
