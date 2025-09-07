// Frontend JavaScript for Story Generator

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const storyForm = document.getElementById('storyForm');
    if (storyForm) {
        storyForm.addEventListener('submit', function(e) {
            const storyIdea = document.getElementById('story_idea').value.trim();
            if (!storyIdea) {
                e.preventDefault();
                alert('Please enter a story idea!');
                document.getElementById('story_idea').focus();
            }
        });
    }
    
    // Example story idea buttons
    const exampleButtons = document.createElement('div');
    exampleButtons.innerHTML = `
        <div class="mt-3">
            <p class="mb-2"><strong>Try these examples:</strong></p>
            <button type="button" class="btn btn-outline-secondary btn-sm me-2 example-idea" data-idea="A young girl finds a secret door in her grandmother's attic">Fantasy</button>
            <button type="button" class="btn btn-outline-secondary btn-sm me-2 example-idea" data-idea="A robot discovers a flower in a post-apocalyptic city">Sci-Fi</button>
            <button type="button" class="btn btn-outline-secondary btn-sm example-idea" data-idea="A detective solves a mysterious case from 50 years ago">Mystery</button>
        </div>
    `;
    
    const storyIdeaField = document.getElementById('story_idea');
    if (storyIdeaField) {
        storyIdeaField.parentNode.appendChild(exampleButtons);
        
        // Add event listeners to example buttons
        const exampleIdeaButtons = document.querySelectorAll('.example-idea');
        exampleIdeaButtons.forEach(button => {
            button.addEventListener('click', function() {
                storyIdeaField.value = this.getAttribute('data-idea');
            });
        });
    }
    
    // Add fade-in animation to story scenes
    const sceneCards = document.querySelectorAll('.scene-card');
    sceneCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * index);
    });
});