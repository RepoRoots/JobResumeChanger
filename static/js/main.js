/**
 * Resume Optimizer - Main JavaScript
 */

// State management
const state = {
    sessionId: null,
    resumeSections: [],
    missingPoints: [],
    matchedPoints: [],
    selectedEnhancements: [],
    currentSearchTerm: null,
    searchResults: []
};

// DOM Elements
const elements = {
    // Forms and sections
    analyzeForm: document.getElementById('analyze-form'),
    uploadSection: document.getElementById('upload-section'),
    resultsSection: document.getElementById('results-section'),
    enhanceSection: document.getElementById('enhance-section'),
    downloadSection: document.getElementById('download-section'),

    // Inputs
    resumeInput: document.getElementById('resume'),
    jobDescInput: document.getElementById('job_description'),
    fileLabel: document.getElementById('file-label'),

    // Buttons
    analyzeBtn: document.getElementById('analyze-btn'),
    enhanceBtn: document.getElementById('enhance-btn'),
    searchInfoBtn: document.getElementById('search-info-btn'),
    applyChangesBtn: document.getElementById('apply-changes-btn'),
    startOverBtn: document.getElementById('start-over-btn'),

    // Results display
    matchScore: document.getElementById('match-score'),
    matchedList: document.getElementById('matched-list'),
    missingList: document.getElementById('missing-list'),
    enhancementForm: document.getElementById('enhancement-form'),
    newScoreText: document.getElementById('new-score-text'),

    // Modal
    searchModal: document.getElementById('search-modal'),
    searchTerm: document.getElementById('search-term'),
    searchResults: document.getElementById('search-results'),
    closeModal: document.getElementById('close-modal'),
    closeModalBtn: document.getElementById('close-modal-btn'),
    useSuggestionBtn: document.getElementById('use-suggestion-btn'),

    // Loading
    loadingOverlay: document.getElementById('loading-overlay'),
    loadingText: document.getElementById('loading-text')
};

// Initialize event listeners
function init() {
    // File input change
    elements.resumeInput.addEventListener('change', handleFileSelect);

    // Form submission
    elements.analyzeForm.addEventListener('submit', handleAnalyze);

    // Enhance button
    elements.enhanceBtn.addEventListener('click', showEnhanceSection);

    // Search info button
    elements.searchInfoBtn.addEventListener('click', searchForInfo);

    // Apply changes button
    elements.applyChangesBtn.addEventListener('click', applyChanges);

    // Start over button
    elements.startOverBtn.addEventListener('click', startOver);

    // Modal close buttons
    elements.closeModal.addEventListener('click', closeModal);
    elements.closeModalBtn.addEventListener('click', closeModal);
    elements.useSuggestionBtn.addEventListener('click', useSuggestion);

    // Close modal on outside click
    elements.searchModal.addEventListener('click', (e) => {
        if (e.target === elements.searchModal) {
            closeModal();
        }
    });
}

// Handle file selection
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        elements.fileLabel.textContent = file.name;
        elements.fileLabel.classList.add('has-file');
    } else {
        elements.fileLabel.textContent = 'Choose a file...';
        elements.fileLabel.classList.remove('has-file');
    }
}

// Show loading overlay
function showLoading(message = 'Processing...') {
    elements.loadingText.textContent = message;
    elements.loadingOverlay.classList.remove('hidden');
}

// Hide loading overlay
function hideLoading() {
    elements.loadingOverlay.classList.add('hidden');
}

// Handle analyze form submission
async function handleAnalyze(e) {
    e.preventDefault();

    const formData = new FormData(elements.analyzeForm);

    showLoading('Analyzing your resume...');

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }

        // Store results in state
        state.sessionId = data.session_id;
        state.resumeSections = data.resume_sections;
        state.missingPoints = data.missing_points;
        state.matchedPoints = data.matched_points;

        // Display results
        displayResults(data);

    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Display analysis results
function displayResults(data) {
    // Update score
    animateScore(data.match_score);

    // Display matched points
    elements.matchedList.innerHTML = '';
    data.matched_points.forEach(point => {
        const li = document.createElement('li');
        li.innerHTML = `
            ${point.keyword}
            <span class="category-badge ${point.category}">${point.category}</span>
        `;
        elements.matchedList.appendChild(li);
    });

    // Display missing points
    elements.missingList.innerHTML = '';
    data.missing_points.forEach(point => {
        const li = document.createElement('li');
        li.className = point.importance === 'required' ? 'importance-required' : 'importance-preferred';
        li.innerHTML = `
            ${point.keyword}
            <span class="category-badge ${point.category}">${point.category}</span>
            ${point.importance === 'required' ? ' *' : ''}
        `;
        elements.missingList.appendChild(li);
    });

    // Show results section
    elements.resultsSection.classList.remove('hidden');

    // Scroll to results
    elements.resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Animate score counter
function animateScore(targetScore) {
    let current = 0;
    const increment = targetScore / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= targetScore) {
            current = targetScore;
            clearInterval(timer);
        }
        elements.matchScore.textContent = Math.round(current);
    }, 20);
}

// Show enhancement section
function showEnhanceSection() {
    // Create enhancement form items
    elements.enhancementForm.innerHTML = '';

    state.missingPoints.forEach((point, index) => {
        const div = document.createElement('div');
        div.className = 'enhancement-item';
        div.dataset.index = index;

        // Create section options based on resume sections
        const sectionOptions = state.resumeSections.map(section =>
            `<option value="${section}" ${point.suggested_sections.includes(section) ? 'selected' : ''}>${section}</option>`
        ).join('');

        div.innerHTML = `
            <div class="enhancement-checkbox">
                <input type="checkbox" id="enhance-${index}" checked>
                <label for="enhance-${index}">
                    <h4>${point.keyword}</h4>
                </label>
                <span class="category-badge ${point.category}">${point.category}</span>
            </div>

            <div class="enhancement-controls">
                <div>
                    <label>Add to section:</label>
                    <select id="section-${index}" class="section-select">
                        ${sectionOptions}
                        <option value="skills">Skills</option>
                        <option value="experience">Experience</option>
                        <option value="projects">Projects</option>
                    </select>
                </div>

                <div>
                    <label>Project/Context (optional):</label>
                    <input type="text" id="context-${index}" placeholder="e.g., E-commerce Platform, API Gateway">
                    <button class="btn btn-secondary search-btn" onclick="searchSinglePoint(${index})">
                        Search Info
                    </button>
                </div>
            </div>

            <div class="suggested-content" id="suggestion-${index}">
                <label>Generated content:</label>
                <textarea id="content-${index}" placeholder="Content will be generated...">${getDefaultContent(point)}</textarea>
            </div>
        `;

        elements.enhancementForm.appendChild(div);
    });

    // Show enhancement section
    elements.enhanceSection.classList.remove('hidden');
    elements.enhanceSection.scrollIntoView({ behavior: 'smooth' });
}

// Get default content for a missing point
function getDefaultContent(point) {
    const section = point.suggested_sections[0] || 'skills';

    if (section === 'skills') {
        return point.keyword;
    }

    return `Utilized ${point.keyword} to develop and implement solutions, improving efficiency and delivering results`;
}

// Search for info on a single point
async function searchSinglePoint(index) {
    const point = state.missingPoints[index];
    const context = document.getElementById(`context-${index}`).value;

    state.currentSearchTerm = point.keyword;
    state.currentSearchIndex = index;

    showLoading(`Searching for ${point.keyword}...`);

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                missing_point: point.keyword,
                context: context
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Search failed');
        }

        state.searchResults = data.results;
        displaySearchResults(data.results, point.keyword);

    } catch (error) {
        alert('Search error: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Search for info on all checked points
async function searchForInfo() {
    const checkedPoints = [];

    state.missingPoints.forEach((point, index) => {
        const checkbox = document.getElementById(`enhance-${index}`);
        if (checkbox && checkbox.checked) {
            checkedPoints.push({ point, index });
        }
    });

    if (checkedPoints.length === 0) {
        alert('Please select at least one point to search for.');
        return;
    }

    // Search for the first checked point (can be extended to batch search)
    const first = checkedPoints[0];
    await searchSinglePoint(first.index);
}

// Display search results in modal
function displaySearchResults(results, term) {
    elements.searchTerm.textContent = term;
    elements.searchResults.innerHTML = '';

    if (results.length === 0) {
        elements.searchResults.innerHTML = '<p>No results found. Using default suggestions.</p>';
    }

    results.forEach((result, index) => {
        const div = document.createElement('div');
        div.className = 'search-result-item';
        div.dataset.index = index;

        const bulletsHtml = result.suggested_bullets && result.suggested_bullets.length > 0
            ? `<ul class="suggested-bullets">${result.suggested_bullets.map(b => `<li>${b}</li>`).join('')}</ul>`
            : '';

        div.innerHTML = `
            <h4>${result.title}</h4>
            <p>${result.snippet}</p>
            ${bulletsHtml}
        `;

        div.addEventListener('click', () => selectSearchResult(div, index));
        elements.searchResults.appendChild(div);
    });

    // Show modal
    elements.searchModal.classList.remove('hidden');
}

// Select a search result
function selectSearchResult(element, index) {
    // Remove selection from others
    document.querySelectorAll('.search-result-item').forEach(el => {
        el.classList.remove('selected');
    });

    // Add selection to clicked
    element.classList.add('selected');
    state.selectedSearchResult = index;
}

// Close modal
function closeModal() {
    elements.searchModal.classList.add('hidden');
    state.selectedSearchResult = null;
}

// Use selected suggestion
function useSuggestion() {
    if (state.selectedSearchResult === undefined || state.selectedSearchResult === null) {
        alert('Please select a suggestion first.');
        return;
    }

    const result = state.searchResults[state.selectedSearchResult];
    const index = state.currentSearchIndex;

    // Get the section and context
    const section = document.getElementById(`section-${index}`).value;
    const context = document.getElementById(`context-${index}`).value;

    // Generate content based on suggestion
    let content = '';
    if (result.suggested_bullets && result.suggested_bullets.length > 0) {
        content = result.suggested_bullets[0];
    } else if (result.snippet) {
        content = `Utilized ${state.currentSearchTerm} to ${result.snippet.substring(0, 100)}...`;
    }

    // Add context if provided
    if (context && !content.includes(context)) {
        content = content.replace('to develop', `in ${context} to develop`);
    }

    // Update the content textarea
    const contentArea = document.getElementById(`content-${index}`);
    if (contentArea) {
        contentArea.value = content;
    }

    closeModal();
}

// Apply changes and generate modified resume
async function applyChanges() {
    const modifications = [];

    state.missingPoints.forEach((point, index) => {
        const checkbox = document.getElementById(`enhance-${index}`);
        if (checkbox && checkbox.checked) {
            const section = document.getElementById(`section-${index}`).value;
            const content = document.getElementById(`content-${index}`).value;

            if (content.trim()) {
                modifications.push({
                    keyword: point.keyword,
                    section: section,
                    content: content.trim(),
                    category: point.category
                });
            }
        }
    });

    if (modifications.length === 0) {
        alert('Please select and configure at least one enhancement.');
        return;
    }

    showLoading('Applying changes to your resume...');

    try {
        const response = await fetch('/modify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ modifications })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Modification failed');
        }

        // Show download section
        showDownloadSection(modifications.length);

    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Show download section
function showDownloadSection(enhancementCount) {
    // Calculate estimated new score
    const originalScore = parseFloat(elements.matchScore.textContent);
    const improvement = Math.min(enhancementCount * 5, 100 - originalScore);
    const newScore = Math.min(originalScore + improvement, 100);

    elements.newScoreText.textContent =
        `Your estimated new match score: ${newScore.toFixed(1)}% (improved from ${originalScore}%)`;

    elements.enhanceSection.classList.add('hidden');
    elements.downloadSection.classList.remove('hidden');
    elements.downloadSection.scrollIntoView({ behavior: 'smooth' });
}

// Start over
function startOver() {
    // Reset state
    state.sessionId = null;
    state.resumeSections = [];
    state.missingPoints = [];
    state.matchedPoints = [];
    state.selectedEnhancements = [];

    // Reset form
    elements.analyzeForm.reset();
    elements.fileLabel.textContent = 'Choose a file...';
    elements.fileLabel.classList.remove('has-file');

    // Hide all sections except upload
    elements.resultsSection.classList.add('hidden');
    elements.enhanceSection.classList.add('hidden');
    elements.downloadSection.classList.add('hidden');

    // Cleanup server-side
    fetch('/cleanup', { method: 'POST' }).catch(() => {});

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);
