document.addEventListener('DOMContentLoaded', function() {
    // Attendre que la page soit complètement chargée
    setTimeout(fetchNews, 500);
});

function fetchNews() {
    const apiKey = '2a28af6c4ebc58d5beba1fc150c105eb'; // À remplacer par votre clé ou utiliser une variable d'environnement
    const url = `https://gnews.io/api/v4/top-headlines?token=${apiKey}&lang=fr&country=fr&max=4`;
    
    // Afficher un loader pendant le chargement
    const container = document.getElementById('news-results');
    if (container) {
        container.innerHTML = '<div class="text-center"><div class="spinner"></div></div>';
        
        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error('Erreur réseau');
                return response.json();
            })
            .then(data => {
                if (data.articles && data.articles.length > 0) {
                    displayNews(data.articles);
                } else {
                    container.innerHTML = '<p class="text-muted text-center">Aucune actualité disponible pour le moment.</p>';
                }
            })
            .catch(error => {
                console.error('Error fetching news:', error);
                container.innerHTML = '<p class="text-muted text-center">Impossible de charger les actualités.</p>';
            });
    }
}

function displayNews(articles) {
    const container = document.getElementById('news-results');
    if (!container) return;
    
    let html = '';
    articles.forEach(article => {
        const date = new Date(article.publishedAt);
        const formattedDate = date.toLocaleDateString('fr-FR', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
        
        html += `
        <div class="col-md-6 col-lg-3 mb-4">
            <div class="news-card h-100">
                <h3 class="h5"><a href="${article.url}" target="_blank" rel="noopener noreferrer">${article.title}</a></h3>
                ${article.image ? `<img src="${article.image}" alt="${article.title}" class="img-fluid mb-2" loading="lazy">` : ''}
                <p class="small">${article.description || ''}</p>
                <small class="text-muted">${formattedDate}</small>
            </div>
        </div>
        `;
    });
    
    container.innerHTML = html;
}
