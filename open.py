# app.py
import os
import random
import json
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'ai-story-generator-secret-key-2023'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Prevent caching
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app)  # Enable CORS for all routes

# Story templates for different genres
STORY_TEMPLATES = {
    "fantasy": [
        {
            "title": "The Enchanted {item}",
            "scenes": [
                {
                    "title": "The Discovery",
                    "text": "In the heart of the {place}, {character} stumbled upon a mysterious {item} that seemed to glow with an otherworldly light. Little did {character} know, this was no ordinary {item} - it held the key to a hidden realm that had been forgotten for centuries.",
                    "image_prompt": "{character} discovering a glowing {item} in a {place}, fantasy style"
                },
                {
                    "title": "The Gateway",
                    "text": "As {character} touched the {item}, a shimmering portal materialized before {character}. Through the swirling mist, {character} could see a world of {fantasy_elements}. With a deep breath, {character} stepped through, leaving the familiar world behind.",
                    "image_prompt": "A magical portal opening in a {place} with {fantasy_elements} visible through it, fantasy art"
                },
                {
                    "title": "The Challenge",
                    "text": "In this new realm, {character} encountered a {magical_creature} who explained that the {item} was actually the {important_artifact} needed to {important_task}. But first, {character} had to prove worthy by {challenge_description}.",
                    "image_prompt": "{character} facing a {magical_creature} in a magical realm, fantasy illustration"
                },
                {
                    "title": "The Triumph",
                    "text": "After successfully {challenge_completion}, {character} used the {item} to {successful_action}, restoring balance to the magical realm. The {magical_creature} granted {character} a gift - the ability to travel between worlds whenever needed.",
                    "image_prompt": "{character} triumphantly holding the {item} with magical energy swirling around, epic fantasy art"
                }
            ]
        }
    ],
    "sci-fi": [
        {
            "title": "The {tech_device} Incident",
            "scenes": [
                {
                    "title": "The Anomaly",
                    "text": "While conducting routine experiments with the {tech_device}, {character} noticed strange readings that defied all known physics. The device was detecting {sci_fi_phenomenon} from a distant sector of space - something that should be impossible according to current scientific understanding.",
                    "image_prompt": "{character} observing strange readings on a {tech_device} display, sci-fi style"
                },
                {
                    "title": "First Contact",
                    "text": "Following the anomalous signals, {character} and the team embarked on a journey to the source. What they found was beyond anything they could have imagined - a {alien_species} whose technology operated on principles humanity had yet to discover.",
                    "image_prompt": "First contact with a {alien_species} in a spaceship or alien environment, science fiction art"
                },
                {
                    "title": "The Revelation",
                    "text": "The {alien_species} revealed that the {tech_device} was actually a key to preventing an impending {cosmic_threat}. They needed humanity's help because only human DNA could interface with the ancient technology designed to {solution_action}.",
                    "image_prompt": "{alien_species} explaining a {cosmic_threat} to {character} and team, sci-fi illustration"
                },
                {
                    "title": "The Solution",
                    "text": "Working together with the {alien_species}, {character} used the modified {tech_device} to {successful_solution}, averting disaster and opening a new chapter in human-alien relations. The experience changed humanity's understanding of its place in the universe forever.",
                    "image_prompt": "{character} operating a advanced device with alien technology to save the day, epic sci-fi art"
                }
            ]
        }
    ],
    "mystery": [
        {
            "title": "The Case of the {mysterious_object}",
            "scenes": [
                {
                    "title": "The Discovery",
                    "text": "When {character} found the {mysterious_object} in the {location}, little did {character} know it would lead to the unraveling of a decades-old mystery. The object contained clues that connected to the unsolved case of the {famous_mystery}.",
                    "image_prompt": "{character} discovering a {mysterious_object} in a {location}, mysterious atmosphere"
                },
                {
                    "title": "The Investigation",
                    "text": "Following the clues from the {mysterious_object}, {character} began investigating the {historical_location} and uncovered evidence that suggested the original investigation had missed crucial details. Witness accounts from the time period didn't match the official story.",
                    "image_prompt": "{character} investigating clues and examining evidence in a {historical_location}, noir style"
                },
                {
                    "title": "The Breakthrough",
                    "text": "A hidden message in the {mysterious_object} led {character} to a secret {hidden_place} where the truth had been concealed all along. There, {character} found proof that {shocking_revelation}.",
                    "image_prompt": "{character} finding hidden evidence in a secret {hidden_place}, dramatic lighting"
                },
                {
                    "title": "The Resolution",
                    "text": "With the mystery finally solved, {character} was able to bring closure to those affected by the events. The {mysterious_object} was placed in a museum as a testament to the importance of perseverance in seeking truth.",
                    "image_prompt": "{character} presenting the solved mystery and the {mysterious_object} in a museum or public setting, satisfying resolution"
                }
            ]
        }
    ]
}

# Word banks for different categories
WORD_BANKS = {
    "character": ["young girl", "curious boy", "brave explorer", "retired detective", "scientist", "student", "artist", "writer"],
    "place": ["ancient forest", "abandoned factory", "grandmother's attic", "old library", "seaside cliff", "mountain cave", "city museum"],
    "item": ["necklace", "book", "compass", "key", "crystal", "watch", "locket", "ring"],
    "fantasy_elements": ["floating islands", "talking animals", "enchanted trees", "magical streams", "mythical creatures"],
    "magical_creature": ["wise dragon", "ancient tree spirit", "mischievous fairy", "noble unicorn", "helpful gnome"],
    "important_artifact": ["Heart of the Forest", "Star Crystal", "Moon Amulet", "Sun Stone", "Key of Ages"],
    "important_task": ["restore the fading magic", "heal the wounded land", "awaken the sleeping guardians", "banish the spreading darkness"],
    "challenge_description": ["retrieving the lost artifact from the treacherous mountains", "solving the riddles of the ancient temple", "earning the trust of the wary forest creatures"],
    "challenge_completion": ["retrieving the artifact", "solving the riddles", "earning their trust"],
    "successful_action": ["channel the ancient energies", "awaken the guardians", "heal the land"],
    "tech_device": ["quantum resonator", "tachyon scanner", "dimensional gateway", "chronal stabilizer"],
    "sci_fi_phenomenon": ["temporal distortions", "gravitational anomalies", "energy signatures", "dimensional rifts"],
    "alien_species": ["crystalline beings", "energy-based lifeforms", "telepathic hive mind", "shape-shifting species"],
    "cosmic_threat": ["dimensional collapse", "time paradox", "black hole emergence", "reality unraveling"],
    "solution_action": ["stabilize the space-time continuum", "prevent the cosmic catastrophe", "seal the dimensional breach"],
    "successful_solution": ["redirect the destructive energy", "stabilize the anomaly", "close the rift"],
    "mysterious_object": ["old diary", "strange device", "cryptic painting", "ancient coin", "weathered photograph"],
    "location": ["antique shop", "family estate", "old hotel", "university archive", "beach house"],
    "famous_mystery": ["Vanishing Heiress", "Phantom Writer", "Silent Symphony", "Missing Inventor"],
    "historical_location": ["old mansion", "abandoned hospital", "historic theater", "former factory"],
    "hidden_place": ["secret room", "underground tunnel", "hidden compartment", "forgotten archive"],
    "shocking_revelation": ["the supposed victim was actually the mastermind", "there were two identical objects switched at the critical moment", "the key witness had been misleading everyone intentionally"]
}

# Art style modifiers
ART_STYLES = {
    "realistic": "photorealistic, detailed, realistic",
    "cartoon": "cartoon style, vibrant colors, animated",
    "anime": "anime style, Japanese animation, vibrant",
    "watercolor": "watercolor painting, soft edges, artistic",
    "digital art": "digital art, concept art, dramatic lighting",
    "oil painting": "oil painting, classic art, textured"
}

def generate_image_url(prompt, art_style="realistic"):
    """Generate a placeholder image based on a keyword and art style"""
    style_modifier = ART_STYLES.get(art_style, ART_STYLES["realistic"])
    full_prompt = f"{prompt}, {style_modifier}"
    image_id = abs(hash(full_prompt)) % 1000
    return f"https://picsum.photos/512/512?random={image_id}"

def generate_story(idea, genre, tone, audience, art_style):
    """Generate a story based on the input parameters"""
    
    # Select appropriate template based on genre
    if genre not in STORY_TEMPLATES:
        genre = "fantasy"  # Default to fantasy
    
    template = random.choice(STORY_TEMPLATES[genre])
    
    # Extract keywords from the idea
    keywords = extract_keywords(idea)
    
    # Fill in the template with appropriate words
    story = {
        "title": fill_template(template["title"], keywords, genre, tone, audience),
        "scenes": [],
        "idea": idea,
        "art_style": art_style,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    for scene_template in template["scenes"]:
        filled_scene = {
            "title": fill_template(scene_template["title"], keywords, genre, tone, audience),
            "text": fill_template(scene_template["text"], keywords, genre, tone, audience),
            "image_prompt": fill_template(scene_template["image_prompt"], keywords, genre, tone, audience)
        }
        filled_scene['image_url'] = generate_image_url(filled_scene['image_prompt'], art_style)
        story["scenes"].append(filled_scene)
    
    return story

def extract_keywords(idea):
    """Extract potential keywords from the story idea"""
    keywords = {
        "character": random.choice(WORD_BANKS["character"]),
        "item": random.choice(WORD_BANKS["item"]),
        "place": random.choice(WORD_BANKS["place"])
    }
    
    idea_lower = idea.lower()
    
    # Try to extract a character from the idea
    if "girl" in idea_lower:
        keywords["character"] = "young girl"
    elif "boy" in idea_lower:
        keywords["character"] = "curious boy"
    elif "man" in idea_lower:
        keywords["character"] = "old man"
    elif "woman" in idea_lower:
        keywords["character"] = "wise woman"
    elif "robot" in idea_lower:
        keywords["character"] = "lonely robot"
    elif "detective" in idea_lower:
        keywords["character"] = "retired detective"
    
    # Try to extract an item from the idea
    for item in WORD_BANKS["item"]:
        if item in idea_lower:
            keywords["item"] = item
            break
    
    # Try to extract a place from the idea
    for place in WORD_BANKS["place"]:
        if place in idea_lower:
            keywords["place"] = place
            break
    
    return keywords

def fill_template(template, keywords, genre, tone, audience):
    """Fill in a template with appropriate words"""
    result = template
    
    # Replace known keywords
    for key, value in keywords.items():
        result = result.replace("{" + key + "}", value)
    
    # Replace other placeholders with appropriate words from the word bank
    while "{" in result and "}" in result:
        start = result.find("{")
        end = result.find("}")
        if start != -1 and end != -1:
            placeholder = result[start+1:end]
            if placeholder in WORD_BANKS:
                replacement = random.choice(WORD_BANKS[placeholder])
                result = result.replace("{" + placeholder + "}", replacement)
            else:
                # If we don't have this placeholder, just remove it
                result = result.replace("{" + placeholder + "}", "")
    
    # Adjust tone based on the selected tone
    if tone == "dark":
        result = make_darker(result)
    elif tone == "humorous":
        result = make_funnier(result)
    elif tone == "epic":
        result = make_epic(result)
    elif tone == "mysterious":
        result = make_mysterious(result)
    
    # Adjust for audience
    if audience == "kids":
        result = simplify_language(result)
    
    return result

def make_darker(text):
    """Make the text darker in tone"""
    dark_words = ["sinister", "foreboding", "ominous", "shadowy", "eerie", "chilling"]
    replacements = {
        "mysterious": random.choice(dark_words),
        "strange": "ominous",
        "interesting": "disturbing",
        "beautiful": "macabre"
    }
    
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    
    return text

def make_funnier(text):
    """Make the text more humorous"""
    funny_words = ["hilarious", "comical", "absurd", "ridiculous", "ludicrous"]
    replacements = {
        "strange": random.choice(funny_words),
        "interesting": "hilarious",
        "mysterious": "absurd",
        "serious": "comical"
    }
    
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    
    return text

def make_epic(text):
    """Make the text more epic"""
    epic_words = ["legendary", "monumental", "colossal", "astounding", "breathtaking"]
    replacements = {
        "great": random.choice(epic_words),
        "big": "colossal",
        "important": "monumental",
        "interesting": "astounding"
    }
    
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    
    return text

def make_mysterious(text):
    """Make the text more mysterious"""
    mystery_words = ["enigmatic", "cryptic", "perplexing", "inscrutable", "puzzling"]
    replacements = {
        "mysterious": random.choice(mystery_words),
        "strange": "enigmatic",
        "interesting": "perplexing",
        "secret": "inscrutable"
    }
    
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    
    return text

def simplify_language(text):
    """Simplify language for children"""
    replacements = {
        "discovered": "found",
        "encountered": "met",
        "investigating": "looking into",
        "ancient": "very old",
        "mysterious": "strange",
        "artifact": "special object",
        "revelation": "big surprise",
        "resolution": "ending",
        "challenge": "test",
        "triumph": "happy ending"
    }
    
    for complex_word, simple_word in replacements.items():
        text = text.replace(complex_word, simple_word)
    
    return text

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_story_route():
    # Get form data
    story_idea = request.form.get('story_idea', '')
    genre = request.form.get('genre', 'fantasy')
    tone = request.form.get('tone', 'lighthearted')
    audience = request.form.get('audience', 'teens')
    art_style = request.form.get('art_style', 'realistic')
    
    # Store in session for later use
    session['story_data'] = {
        'idea': story_idea,
        'genre': genre,
        'tone': tone,
        'audience': audience,
        'art_style': art_style
    }
    
    # Generate the story
    story = generate_story(story_idea, genre, tone, audience, art_style)
    
    # Store the complete story in session
    session['generated_story'] = story
    
    return redirect(url_for('view_story'))

@app.route('/story')
def view_story():
    story = session.get('generated_story')
    if not story:
        return redirect(url_for('index'))
    
    return render_template('story.html', story=story)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint for generating stories"""
    data = request.get_json(force=True)
    
    story_idea = data.get('story_idea', 'A mysterious story')
    genre = data.get('genre', 'fantasy')
    tone = data.get('tone', 'lighthearted')
    audience = data.get('audience', 'teens')
    art_style = data.get('art_style', 'realistic')
    
    story = generate_story(story_idea, genre, tone, audience, art_style)
    
    return jsonify(story)

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')