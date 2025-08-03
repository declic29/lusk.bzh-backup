document.addEventListener('DOMContentLoaded', function() {
    fetchNews();
});

function fetchNews() {
    const apiKey = '2a28af6c4ebc58d5beba1fc150c105eb'; // Remplacez par votre clé
    const url = `https://gnews.io/api/v4/top-headlines?token=${apiKey}&lang=fr&country=fr&max=6`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => displayNews(data.articles))
        .catch(error => console.error('Error fetching news:', error));
}

function displayNews(articles) {
    const container = document.getElementById('news-results');
    
    if (!articles || articles.length === 0) {
        container.innerHTML = '<p>Aucune actualité disponible pour le moment.</p>';
        return;
    }
    
    let html = '';
    articles.forEach(article => {
        html += `
        <div class="col-md-6 col-lg-4">
            <div class="news-card">
                <h3><a href="${article.url}" target="_blank">${article.title}</a></h3>
                ${article.image ? `<img src="${article.image}" alt="${article.title}">` : ''}
                <p>${article.description}</p>
                <small>${new Date(article.publishedAt).toLocaleDateString()}</small>
            </div>
        </div>
        `;
    });
    
    container.innerHTML = html;
}
