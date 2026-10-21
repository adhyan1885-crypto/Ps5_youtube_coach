import streamlit as st
from urllib.parse import quote_plus
from datetime import date, timedelta

st.set_page_config(page_title="PS5 YouTube Coach", page_icon="🎮", layout="wide")

# PS5 YouTube Coach — rebuilt around one shared game value so every section
# (plan, scripts, research, music, SEO and discovery) follows the user's input.

PRESETS = [
    "Ghost of Tsushima", "Grand Theft Auto V", "Grand Theft Auto VI", "Call of Duty",
    "Call of Duty: Modern Warfare", "Minecraft", "Forza Horizon 5", "Forza Horizon 6",
    "The Last of Us Part I", "The Last of Us Part II", "God of War (2018)",
    "God of War Ragnarök", "Fortnite", "Valorant", "EA SPORTS FC", Other / future game"
]
GENRES = ["Auto / not sure", "Action-adventure", "Open world", "FPS / shooter", "RPG",
          "Racing", "Survival / horror", "Sandbox / building", "Sports", "Fighting",
          "Strategy", "Simulation", "Indie / casual", "Story-driven", "Other"]
STYLES = ["Cinematic", "Funny / entertaining", "Competitive / high-skill", "Educational / tutorial",
          "Challenge / experiment", "Chill / story-driven"]
FORMATS = ["Shorts (vertical)", "Long-form (horizontal)", "Both: Shorts + long-form"]
GOALS = ["More views / discovery", "Improve click-through rate (CTR)", "Improve retention / watch time",
         "Gain subscribers / community", "Monetize safely", "Post consistently / improve skills"]
PLATFORMS = ["PlayStation 5", "Xbox Series X/S", "PC / laptop", "Nintendo Switch", "Mobile"]

st.title("🎮 PS5 YouTube Coach")
st.caption("A rebuilt, game-agnostic planning assistant for gaming creators.")
st.info("This version generates detailed plans from templates and creates search links. It does not automatically read YouTube analytics/comments or verify live trends, prices, game facts, music licences, or frame rates. Check linked sources before relying on current information.")

with st.sidebar:
    st.header("1. Your game")
    preset = st.selectbox("Quick-select a game", PRESETS, index=0, key="preset_game")
    game_input = st.text_input("Custom game name (optional; overrides preset)", placeholder="e.g. Call of Duty: Modern Warfare 4", key="game_name_input")
    # Single canonical game variable; custom input overrides the preset, and every section uses it.
    game = game_input.strip() or ("your selected game" if preset == "Other / future game" else preset)
    genre = st.selectbox("Game category / genre", GENRES, key="genre")
    platform = st.selectbox("Your gaming platform", PLATFORMS, key="platform")
    st.header("2. Your video")
    video_format = st.selectbox("Format", FORMATS, key="video_format")
    style = st.selectbox("Video style", STYLES, key="video_style")
    goal = st.selectbox("Main goal", GOALS, key="goal")
    language = st.selectbox("Video language", ["English", "Hindi", "Gujarati", "Hinglish", "Other / no dialogue"], key="language")
    audience = st.selectbox("Intended audience", ["General gaming audience", "Beginners", "Fans of this game", "Competitive players", "Story / lore fans", "Casual viewers"], key="audience")
    st.header("3. Creative categories")
    script_angle = st.selectbox("Script / story angle", ["Funny moments", "Scary / suspense", "Cinematic story", "Beginner guide", "Challenge / experiment", "Competitive highlights", "Secrets / discoveries", "Honest review", "Relaxing gameplay", "Reaction / commentary"], key="script_angle")
    edit_vibe = st.selectbox("Editing style", ["Fast meme cuts", "Cinematic slow build", "Horror suspense", "Clean tutorial", "Competitive montage", "Story documentary", "Cozy / relaxing", "High-energy Shorts", "Minimal raw gameplay"], key="edit_vibe")
    music_mood = st.selectbox("Music mood", ["Cinematic orchestral", "Funny / quirky", "Dark horror ambience", "High-energy electronic", "Emotional piano", "Chill lo-fi", "Epic action percussion", "No music / game audio only"], key="music_mood")
    title_style = st.selectbox("Title style", ["Curiosity", "Funny", "Scary", "Cinematic", "Tutorial / searchable", "Challenge", "Review / opinion"], key="title_style")
    description_tone = st.selectbox("Description tone", ["Friendly creator", "Cinematic / story", "Helpful tutorial", "Funny / casual", "Competitive / direct"], key="description_tone")
    tag_focus = st.selectbox("Tag strategy", ["Game + gameplay", "Tutorial / tips", "Funny moments", "Horror / reactions", "Cinematic / story", "Challenge", "Competitive / ranked"], key="tag_focus")
    st.caption("Tip: choose ‘Keep my typed game’ and enter any game name, or select a preset to fill it in. Check the game name displayed below the inputs.")

# One canonical URL builder: every search query is derived from the same game value.
def search_url(base, query):
    return base + quote_plus(query)

web_search = search_url("https://www.google.com/search?q=", f"{game} {genre if genre != 'Auto / not sure' else ''} gameplay tips latest news")
youtube_search = search_url("https://www.youtube.com/results?search_query=", f"{game} {style} gameplay")
official_search = search_url("https://www.google.com/search?q=", f"{game} official website publisher news patch notes")
trend_search = search_url("https://www.google.com/search?q=", f"gaming trends {game} YouTube videos {date.today().year}")

style_data = {
    "Cinematic": {
        "hook": "Open on the strongest visual, dramatic reveal, close call, or beautiful shot. Put context after the hook; skip a long intro.",
        "music": "Cinematic orchestral, emotional piano, atmospheric strings, or restrained tension build.",
        "keywords": "cinematic, orchestral, emotional piano, atmospheric, tension build, epic instrumental",
        "edit": "Use intentional cuts, let important shots breathe, add only a few motivated slow-motion moments, and preserve ambience and dialogue."
    },
    "Funny / entertaining": {
        "hook": "Start with the funniest fail, unexpected event, or reaction; explain only the context viewers need.",
        "music": "Playful pizzicato, quirky percussion, light funk, or short comedic stings.",
        "keywords": "comedy, playful, quirky, pizzicato, light funk, comedic instrumental",
        "edit": "Trim pauses, time cuts around the punchline, keep reactions clear, use occasional punch-in zooms/captions, and avoid sound-effect overload."
    },
    "Competitive / high-skill": {
        "hook": "Show the clutch, cleanest play, rank, or result immediately; quickly explain the stakes.",
        "music": "Driving electronic beats, energetic percussion, dark synth, or restrained action rock.",
        "keywords": "high energy, electronic, driving percussion, dark synth, action instrumental, intense",
        "edit": "Keep action readable, cut downtime, preserve key gameplay sounds, briefly label loadouts/strategies, and avoid effects that hide the play."
    },
    "Educational / tutorial": {
        "hook": "Show the problem and promised result first, then teach one clear method.",
        "music": "Low-volume neutral electronic, light lo-fi, or unobtrusive ambient instrumental.",
        "keywords": "minimal electronic, light lo-fi, calm background, tutorial, unobtrusive instrumental",
        "edit": "Use numbered steps, zooms only where needed, readable captions, before/after examples, and pauses long enough for viewers to follow."
    },
    "Challenge / experiment": {
        "hook": "State the rule and stakes in one sentence, then show a quick preview of the attempt.",
        "music": "Building percussion, playful suspense, or energetic electronic instrumental.",
        "keywords": "building tension, energetic electronic, suspense instrumental, challenge, percussion",
        "edit": "Show the rules on screen, remove repetitive attempts, keep meaningful failures, add progress markers, and make the final outcome clear."
    },
    "Chill / story-driven": {
        "hook": "Begin with a compelling story beat, discovery, atmosphere, or question without spoiling more than intended.",
        "music": "Ambient piano, gentle strings, atmospheric pads, or soft instrumental textures.",
        "keywords": "ambient piano, atmospheric, gentle strings, emotional instrumental, exploration",
        "edit": "Use longer shots when atmosphere matters, preserve dialogue, add subtle captions when useful, and avoid unnecessary transitions."
    }
}
selected_style = style_data[style]

# Dynamic content generated on each Streamlit rerun from the current input.
st.subheader("Current project")
st.markdown(f"**Game:** {game}  ·  **Platform:** {platform}  ·  **Category:** {genre}  ·  **Format:** {video_format}")
st.markdown(f"**Style:** {style}  ·  **Goal:** {goal}  ·  **Audience:** {audience}  ·  **Language:** {language}  ·  **Script angle:** {script_angle}")
st.caption(f"Creative direction: editing = {edit_vibe} · music = {music_mood} · title = {title_style} · description = {description_tone} · tags = {tag_focus}")

plan_tab, edit_tab, music_tab, research_tab, discovery_tab, publish_tab = st.tabs([
    "🎬 Video plan & script", "✂️ Editing step-by-step", "🎵 Music & licensing",
    "🔎 Game research", "🧭 Audience & game finder", "📅 Publish & measure"
])

with plan_tab:
    st.header(f"Video plan for {game}")
    st.write(f"**Concept:** Make a {style.lower()} video about one specific moment, question, challenge, discovery, or result in **{game}**. Avoid a generic montage unless the clips have a clear theme.")
    st.write("**Opening hook:** " + selected_style["hook"])
    if "Shorts" in video_format:
        st.subheader("Shorts structure (adapt to the idea; don't pad it)")
        st.markdown("- **0–2 seconds:** strongest moment or clear question.\n- **2–6 seconds:** minimum context viewers need.\n- **6–25 seconds:** action, explanation, escalation, or payoff.\n- **Final seconds:** result/reaction and a natural next-video prompt if relevant.")
    if "Long-form" in video_format or "Both" in video_format:
        st.subheader("Long-form structure")
        st.markdown("- **0:00–0:15:** cold open showing the promise of the video.\n- **0:15–0:45:** explain the goal, challenge, or question.\n- **Main section:** progress through 3–5 clear beats; remove repetitive dead time.\n- **Payoff:** show the result and what changed.\n- **Ending:** concise conclusion and relevant next-video suggestion; avoid a long outro.")
    angle_prompts = {
        "Funny moments": "Set up the situation quickly, leave room for the reaction, and land the punchline without over-explaining.",
        "Scary / suspense": "Build a question or threat, preserve important quiet audio, and delay the reveal until the footage earns it.",
        "Cinematic story": "Use a visual opening, establish the emotional or story context, and let key shots breathe.",
        "Beginner guide": "State the problem and result first, then explain each step in plain language.",
        "Challenge / experiment": "State the rule, stakes, and success condition before showing attempts.",
        "Competitive highlights": "Show the high-skill moment first, then explain the stakes and key decision.",
        "Secrets / discoveries": "Present a specific question, show how you tested it, and distinguish confirmed facts from guesses.",
        "Honest review": "Explain what you tested, what worked, what did not, and who may enjoy it.",
        "Relaxing gameplay": "Keep the pacing calm, preserve ambience, and avoid loud edits that break the mood.",
        "Reaction / commentary": "Use your genuine reaction and add context that makes the moment understandable to a new viewer."
    }
    st.subheader(f"Script starter — {script_angle}")
    st.write("**Direction:** " + angle_prompts[script_angle])
    script = f"""[HOOK — {script_angle}: show the strongest real moment from {game}]\n\nVOICE / CAPTION: “Today in {game}, I'm trying to [specific goal or question].”\n\n[CONTEXT] Explain the rule, mission, location, build, or problem in one or two sentences.\n\n[BEAT 1] Show the first meaningful attempt or discovery. Add a caption only if it improves understanding.\n\n[BEAT 2] Show escalation, a useful tip, a mistake, or a surprising turn.\n\n[PAYOFF] Show the actual result. Don't claim a win, secret, record, or discovery unless the footage proves it.\n\n[ENDING] “Would you try this in {game}? What should I test next?” (Use only if it fits your audience.)"""
    st.text_area("Copy and customize this script", value=script, height=300, key="script_output")
    st.subheader("Title ideas")
    title_templates = {
        "Curiosity": [f"I Didn't Expect This in {game}", f"What Happens If You Try This in {game}?", f"The Detail I Nearly Missed in {game}"],
        "Funny": [f"{game} Went Completely Wrong", f"My Funniest {game} Moment Yet", f"I Thought This Would Work in {game}"],
        "Scary": [f"The Creepiest Moment I Found in {game}", f"I Was Not Ready for This in {game}", f"Playing {game} With the Lights Off"],
        "Cinematic": [f"A Cinematic Moment in {game}", f"{game} Looks Unreal in This Scene", f"A Quiet, Beautiful Moment in {game}"],
        "Tutorial / searchable": [f"{game}: Beginner Tips to Know First", f"How to Improve at {game}", f"{game} Guide: A Simple Way to Start"],
        "Challenge": [f"Can I Beat This Challenge in {game}?", f"I Tried {game} With One Rule", f"Can This Strategy Work in {game}?"],
        "Review / opinion": [f"Is {game} Worth Playing? My Honest Take", f"What {game} Does Well — and What It Doesn't", f"Who Should Play {game}?"]
    }
    title_ideas = title_templates[title_style]
    for t in title_ideas:
        st.markdown(f"- {t}")
    st.caption("Treat titles as drafts. Keep only claims your actual footage proves; don't use fake urgency or misleading promises.")
    st.subheader(f"Description and tags — {description_tone} / {tag_focus}")
    tone_openers = {
        "Friendly creator": f"Hey everyone! In this video, we're playing {game} and exploring the moment shown in the footage.",
        "Cinematic / story": f"A cinematic gameplay moment from {game}, focused on atmosphere, story, and the scene itself.",
        "Helpful tutorial": f"This video covers a practical {game} tip. Check the steps below and adapt them to your version of the game.",
        "Funny / casual": f"Things did not go exactly to plan in {game}. Here's the moment and how it played out.",
        "Competitive / direct": f"A focused {game} gameplay session highlighting decisions, mechanics, and the final result."
    }
    description = f"{tone_openers[description_tone]}\n\nWhat happens: [write a short, accurate summary of this actual video].\n\nPlatform: {platform}\nGame: {game}\nFormat: {video_format}\nStyle: {style}\n\nMusic: [add track credit here if required by the licence].\n\nSubscribe or comment with a relevant suggestion if you want to see more."
    st.text_area("Description template (customize before uploading)", value=description, height=180, key="description_template")
    tag_templates = {
        "Game + gameplay": [game, f"{game} gameplay", f"{game} {platform}", f"{game} walkthrough", f"{game} highlights"],
        "Tutorial / tips": [game, f"{game} tips", f"{game} beginner guide", f"how to play {game}", f"{game} tutorial"],
        "Funny moments": [game, f"{game} funny moments", f"funny {game} gameplay", f"{game} fails", f"gaming funny moments"],
        "Horror / reactions": [game, f"{game} horror gameplay", f"{game} scary moments", f"{game} reaction", f"scary gaming"],
        "Cinematic / story": [game, f"{game} cinematic", f"{game} story", f"{game} cutscenes", f"cinematic gameplay"],
        "Challenge": [game, f"{game} challenge", f"{game} challenge run", f"{game} experiment", f"gaming challenge"],
        "Competitive / ranked": [game, f"{game} ranked", f"{game} competitive gameplay", f"{game} best plays", f"{game} tips"]
    }
    st.text_input("Relevant tag ideas (remove anything that doesn't match)", value=", ".join(tag_templates[tag_focus]), key="tag_ideas")
    st.caption("Tags are secondary to an accurate title, thumbnail, topic, and viewer response. Do not add unrelated trending terms.")

with edit_tab:
    st.header("Editing coach — detailed workflow")
    device = st.radio("Where will you edit?", ["Mobile phone / tablet", "PC / laptop"], horizontal=True, key="edit_device")
    if device.startswith("Mobile"):
        editor = st.selectbox("Editing app", ["CapCut", "VN", "InShot", "YouTube Create", "Other mobile editor"], key="mobile_editor")
        st.write(f"**Workflow for {editor}:**")
        steps = [
            "Create a new project and select the target aspect ratio before trimming.",
            "Import the original gameplay recording; duplicate the project if making both vertical and horizontal versions.",
            "Put the strongest moment first. Remove loading screens, repeated attempts, long pauses, and unrelated clips.",
            "Arrange the clips into a clear beginning, development, and payoff. Keep enough context that viewers understand what happened.",
            "Add captions or short labels for dialogue, tips, rules, loadouts, or locations. Check spelling and phone-safe margins.",
            "Adjust crop/reframe for vertical video; keep the important character, action, UI, and subtitles visible.",
            "Balance gameplay/dialogue first, music lower underneath, and sound effects only where they help. Listen with headphones.",
            "Use transitions and effects sparingly. Add color correction only if it improves clarity and consistency.",
            "Export, watch the entire file, check black frames/audio/captions, then upload."
        ]
    else:
        editor = st.selectbox("Editing app", ["DaVinci Resolve", "Adobe Premiere Pro", "CapCut Desktop", "Other PC editor"], key="pc_editor")
        st.write(f"**Workflow for {editor}:**")
        steps = [
            "Create a project, set the timeline to the intended resolution/frame rate, and organize gameplay, audio, and music tracks.",
            "Import and review footage; mark the best moments before assembling the timeline.",
            "Build a rough cut around one idea. Remove dead time, repetitive attempts, and clips that don't advance the story.",
            "Refine pacing and audio continuity; use J/L cuts only where they help the story or commentary.",
            "Add readable captions, labels, chapters, or callouts. Keep text within safe margins and avoid covering important UI.",
            "Reframe a duplicate sequence for vertical Shorts rather than blindly cropping a horizontal master.",
            "Balance dialogue/gameplay, music, and effects. Listen on headphones and phone speakers if possible.",
            "Apply restrained color correction and effects; prioritize readable gameplay and stable playback.",
            "Export a high-quality H.264 MP4 preset as a starting point, then watch the full export before uploading."
        ]
    for i, step in enumerate(steps, 1):
        st.markdown(f"**Step {i}.** {step}")
    st.subheader("Export starting points")
    st.markdown("- **Shorts:** vertical 9:16, commonly 1080 × 1920.\n- **Long-form:** horizontal 16:9, commonly 1920 × 1080 if your source supports it.\n- **Frame rate:** normally match the source (often 30 or 60 fps); exporting 30 fps footage at 60 fps doesn't create extra captured detail.\n- **Format:** high-quality H.264 MP4 is a practical starting point. Exact options differ by app/device.")
    st.subheader(f"Editing direction — {edit_vibe}")
    edit_vibe_guidance = {
        "Fast meme cuts": "Keep only setup, reaction, and payoff. Use quick punch-ins sparingly, subtitle the key joke, and avoid stacking too many sounds at once.",
        "Cinematic slow build": "Open with a striking shot, use longer shots, subtle speed changes only where justified, restrained color grading, and music that builds into the payoff.",
        "Horror suspense": "Preserve quiet ambience, lower music under important game sounds, cut before/after tension deliberately, and avoid spoiling the scare in the opening.",
        "Clean tutorial": "Use numbered steps, zooms on the relevant UI, clear captions, before/after proof, and remove any step that doesn't help the viewer.",
        "Competitive montage": "Synchronize cuts to meaningful plays, keep HUD/action visible, use speed ramps sparingly, and preserve enough lead-in to understand each play.",
        "Story documentary": "Organize clips chronologically or by argument, use voice-over to bridge gaps, and avoid music over essential dialogue.",
        "Cozy / relaxing": "Use gentle cuts, preserve ambient sound, keep music quiet, and avoid unnecessary overlays or sudden volume jumps.",
        "High-energy Shorts": "Show the payoff immediately, use readable captions, reframe to vertical safely, and keep each beat moving toward one clear outcome.",
        "Minimal raw gameplay": "Trim dead time, keep authentic game audio, add only essential labels, and avoid effects that make the gameplay harder to read."
    }
    st.write(edit_vibe_guidance[edit_vibe])
    st.write("**Style baseline:** " + selected_style["edit"])
    st.subheader("Editing timeline")
    if "Shorts" in video_format:
        timeline = ["0–2 s: show the strongest moment or question; no logo intro.", "2–6 s: add only the context needed to understand the moment.", "6–20 s: develop the action, joke, tip, or tension; remove pauses.", "20 s to payoff: deliver the result and end cleanly; use only the length the idea needs."]
    else:
        timeline = ["Opening: show the promised outcome or an intriguing moment before greetings.", "Setup: explain the goal, rules, or question in a few sentences.", "Middle: build 3–5 distinct beats; cut repetition and label useful context.", "Payoff: show the actual outcome and explain what it means.", "Ending: brief conclusion and a relevant next-video invitation, if natural."]
    for i, beat in enumerate(timeline, 1):
        st.markdown(f"**Timeline {i}.** {beat}")
    st.checkbox("Aspect ratio and resolution checked", key="check_aspect")
    st.checkbox("Frame rate matches source where practical", key="check_fps")
    st.checkbox("Gameplay/dialogue is clear and music doesn't drown it out", key="check_audio")
    st.checkbox("Captions and export checked from start to finish", key="check_export")

with music_tab:
    st.header(f"Music mood and licensing for {game}")
    music_catalog = {
        "Cinematic orchestral": ("orchestral build, cinematic tension, epic instrumental, strings, trailer percussion", "Use a gradual build; let the strongest visual land with the musical rise."),
        "Funny / quirky": ("playful pizzicato, quirky percussion, light funk, comedic instrumental, cartoon pluck", "Use short accents around the joke; keep them lower than dialogue and game audio."),
        "Dark horror ambience": ("dark ambient drone, suspense texture, eerie piano, tension pulse, horror atmosphere", "Leave quiet gaps so footsteps, warnings, and game ambience remain audible."),
        "High-energy electronic": ("high energy electronic, driving beat, synth bass, action instrumental", "Match beat changes to meaningful gameplay moments, not every cut."),
        "Emotional piano": ("emotional piano, reflective instrumental, gentle strings, melancholic ambient", "Use softer music under story scenes and avoid masking dialogue."),
        "Chill lo-fi": ("lo-fi instrumental, mellow beat, warm ambient, relaxed background music", "Keep the beat steady and low so gameplay remains the focus."),
        "Epic action percussion": ("epic percussion, cinematic drums, action rhythm, energetic instrumental", "Use the biggest hits for actual stakes or payoff; avoid constant loudness."),
        "No music / game audio only": ("no music, original game audio, ambience, gameplay sound", "Prioritize clean game audio and voice; check the game's own music/copyright settings.")
    }
    music_terms, music_edit_tip = music_catalog[music_mood]
    st.write(f"**Chosen music category:** {music_mood}")
    st.write(f"**Direction for {style.lower()} gameplay:** {selected_style['music']}")
    st.write("**Search keywords for YouTube Audio Library:** " + music_terms)
    st.write("**Mixing tip:** " + music_edit_tip)
    st.write("**Additional style keywords:** " + selected_style["keywords"])
    st.markdown("[Open YouTube Audio Library](https://youtube.com/audiolibrary)")
    st.markdown("[Read YouTube's official Audio Library guidance](https://support.google.com/youtube/answer/3376882)")
    st.warning("This app recommends music moods and search terms; it does not select or verify an individual track. Check that specific track's licence, commercial/monetization terms, platform use, and attribution requirements. YouTube Audio Library is the safer starting point; third-party ‘no copyright’ labels alone are not proof of permission.")
    st.subheader("Before using a track")
    st.checkbox("I found the track in YouTube Audio Library or have clear permission", key="music_permission")
    st.checkbox("I checked this track's exact terms for monetization and use", key="music_terms")
    st.checkbox("I copied required attribution exactly into the description", key="music_credit")
    st.checkbox("I confirmed the track suits this video format and length", key="music_format")

with research_tab:
    st.header(f"Research: {game}")
    st.success(f"All search links below are generated from your current game name: **{game}**")
    st.write("These buttons open external search pages. Review dates, platforms, editions, sources, and results yourself; this app does not automatically read or verify the pages.")
    st.link_button(f"Search YouTube for {game} videos", youtube_search, use_container_width=True)
    st.link_button(f"Search the web for {game} tips and news", web_search, use_container_width=True)
    st.link_button(f"Find official {game} / publisher information", official_search, use_container_width=True)
    st.link_button(f"Research trends related to {game}", trend_search, use_container_width=True)
    st.subheader("Research questions")
    st.markdown(f"- What are viewers asking about **{game}** right now?\n- Which recent videos about **{game}** are getting discussion, and what is genuinely different about them?\n- Are updates, releases, modes, or platform versions current?\n- Can you make an original video based on your own gameplay rather than copying another creator?")
    custom_query = st.text_input("Add a specific research question", placeholder=f"e.g. best beginner settings for {game}", key="research_question")
    if custom_query.strip():
        st.link_button("Search this question", search_url("https://www.google.com/search?q=", f"{game} {custom_query.strip()}"), use_container_width=True)

with discovery_tab:
    st.header("Audience & Game Finder")
    st.write("Use this to shortlist games that fit your audience, platform, category, and spending limit. It uses searches and the information you provide; it does not automatically retrieve live trends or comments.")
    col1, col2 = st.columns(2)
    with col1:
        finder_platform = st.selectbox("Platform you can play on", PLATFORMS, key="finder_platform")
        finder_category = st.selectbox("Category to explore", ["Any category"] + GENRES[1:], key="finder_category")
        budget = st.selectbox("Maximum game budget", ["Free-to-play only", "₹500", "₹1,000", "₹2,000", "₹5,000", "No fixed budget"], key="finder_budget")
    with col2:
        pc_cpu = st.text_input("PC CPU (PC only)", placeholder="e.g. Intel Core i5-7500", key="pc_cpu")
        pc_gpu = st.text_input("PC GPU (PC only)", placeholder="e.g. Intel HD Graphics 630", key="pc_gpu")
        pc_ram = st.selectbox("PC RAM (PC only)", ["Not applicable / unsure", "4 GB", "8 GB", "16 GB", "32 GB or more"], key="pc_ram")
    audience_notes = st.text_area("Audience clues (optional)", placeholder="What do viewers ask for? What are your top videos about?", key="audience_notes")
    comment_text = st.text_area("Paste viewer comments (optional)", placeholder="Paste comments you are allowed to use. Remove personal details.", key="comment_text")
    if st.button("Build game discovery searches", type="primary", key="discover_games"):
        cat = "" if finder_category == "Any category" else finder_category
        queries = [
            f"best trending {cat} games {finder_platform} {date.today().year}",
            f"new and upcoming {cat} games {finder_platform} {date.today().year}",
            f"popular {cat} games on YouTube {finder_platform} {date.today().year}"
        ]
        if budget != "No fixed budget":
            queries = [q + (" free" if budget == "Free-to-play only" else f" under {budget}") for q in queries]
        if finder_platform == "PC / laptop" and pc_gpu.strip():
            queries.append(f"games playable on {pc_gpu} {pc_cpu} {pc_ram} RAM minimum requirements")
        st.subheader("Three research routes")
        for i, q in enumerate(queries[:3], 1):
            st.markdown(f"**Research route {i}:** {q}")
            st.link_button(f"Open search {i}", search_url("https://www.google.com/search?q=", q), key=f"discover_link_{i}")
        st.caption("Compare at least two sources, confirm the exact platform/edition and current price, and don't treat search ranking alone as proof that a game is trending.")
        if finder_platform == "PC / laptop":
            st.info("PC compatibility requires checking the exact CPU, GPU, RAM, OS, storage, and the game's minimum/recommended requirements. Search results are not a benchmark; frame rate cannot be guaranteed from these fields alone.")
        if audience_notes.strip() or comment_text.strip():
            st.subheader("Audience clues you supplied")
            combined = (audience_notes + " " + comment_text).lower()
            # Lightweight keyword counts, clearly labelled as simple text clues rather than AI sentiment.
            terms = ["game", "story", "horror", "racing", "multiplayer", "tutorial", "tips", "challenge", "minecraft", "call of duty", "gta", "fortnite", "price", "free"]
            found = [(term, combined.count(term)) for term in terms if combined.count(term) > 0]
            if found:
                st.write("Repeated keyword clues: " + ", ".join(f"{term} ({count})" for term, count in sorted(found, key=lambda x: x[1], reverse=True)))
            else:
                st.write("No keywords from the simple built-in list were detected. Review the comments manually for requests and questions.")
            st.caption("This is basic keyword counting, not sentiment analysis, demographic analysis, or a direct connection to YouTube comments.")

with publish_tab:
    st.header("Publishing plan & what to measure")
    upload_date = st.date_input("Planned upload date", value=date.today() + timedelta(days=1), key="upload_date")
    time_window = st.selectbox("Posting window to test (local time)", ["Morning", "Afternoon", "Evening", "Late evening"], index=2, key="posting_window")
    cadence = st.selectbox("Sustainable cadence", ["One video a week", "Two videos a week", "Three Shorts a week", "One Short + one long video a week", "Flexible / learning first"], key="cadence")
    st.write(f"**Plan:** {cadence}; target date **{upload_date.strftime('%d %b %Y')}**; test the **{time_window.lower()}** window.")
    st.warning("There is no universal best posting time. Treat this as a test window, then use YouTube Studio → Analytics → Audience and your own performance data to adjust. This app cannot see your audience activity automatically.")
    st.subheader("After publishing, review")
    st.markdown("- **Reach:** impressions and traffic sources.\n- **Packaging:** click-through rate (CTR), compared with your own channel's usual results and traffic source.\n- **Retention:** first 30 seconds for long-form, and viewed-versus-swiped-away/retention for Shorts where available.\n- **Engagement:** meaningful comments, likes, shares, and returning viewers.\n- **Next experiment:** change one thing at a time—hook, topic, thumbnail/title, or pacing.")
    st.markdown("[Open YouTube Studio](https://studio.youtube.com/)")
    st.checkbox("Recording backed up and edit/export checked", key="pub_backup")
    st.checkbox("Title and thumbnail accurately match the video", key="pub_title")
    st.checkbox("Description, relevant tags, and music permissions checked", key="pub_description")
    st.checkbox("Visibility, audience setting, and restrictions checked after upload", key="pub_visibility")

st.divider()
st.caption("PS5 YouTube Coach • Free planning starter • No automatic YouTube account access, live trend verification, licence verification, upload scheduling, or guaranteed growth in this version.")
import streamlit as st
from urllib.parse import quote_plus
from datetime import date, timedelta

st.set_page_config(page_title="PS5 YouTube Coach", page_icon="🎮", layout="wide")

# PS5 YouTube Coach — rebuilt around one shared game value so every section
# (plan, scripts, research, music, SEO and discovery) follows the user's input.

PRESETS = [
    "Ghost of Tsushima", "Grand Theft Auto V", "Grand Theft Auto VI", "Call of Duty",
    "Call of Duty: Modern Warfare", "Minecraft", "Forza Horizon 5", "Forza Horizon 6",
    "The Last of Us Part I", "The Last of Us Part II", "God of War (2018)",
    "God of War Ragnarök", "Fortnite", "Valorant", "EA SPORTS FC", "Other / future game"
]
GENRES = ["Auto / not sure", "Action-adventure", "Open world", "FPS / shooter", "RPG",
          "Racing", "Survival / horror", "Sandbox / building", "Sports", "Fighting",
          "Strategy", "Simulation", "Indie / casual", "Story-driven", "Other"]
STYLES = ["Cinematic", "Funny / entertaining", "Competitive / high-skill", "Educational / tutorial",
          "Challenge / experiment", "Chill / story-driven"]
FORMATS = ["Shorts (vertical)", "Long-form (horizontal)", "Both: Shorts + long-form"]
GOALS = ["More views / discovery", "Improve click-through rate (CTR)", "Improve retention / watch time",
         "Gain subscribers / community", "Monetize safely", "Post consistently / improve skills"]
PLATFORMS = ["PlayStation 5", "Xbox Series X/S", "PC / laptop", "Nintendo Switch", "Mobile"]

st.title("🎮 PS5 YouTube Coach")
st.caption("A rebuilt, game-agnostic planning assistant for gaming creators.")
st.info("This version generates detailed plans from templates and creates search links. It does not automatically read YouTube analytics/comments or verify live trends, prices, game facts, music licences, or frame rates. Check linked sources before relying on current information.")

with st.sidebar:
    st.header("1. Your game")
    preset = st.selectbox("Quick-select a game", PRESETS, index=0, key="preset_game")
    game_input = st.text_input("Custom game name (optional; overrides preset)", placeholder="e.g. Call of Duty: Modern Warfare 4", key="game_name_input")
    # Single canonical game variable; custom input overrides the preset, and every section uses it.
    game = game_input.strip() or ("your selected game" if preset == "Other / future game" else preset)
    genre = st.selectbox("Game category / genre", GENRES, key="genre")
    platform = st.selectbox("Your gaming platform", PLATFORMS, key="platform")
    st.header("2. Your video")
    video_format = st.selectbox("Format", FORMATS, key="video_format")
    style = st.selectbox("Video style", STYLES, key="video_style")
    goal = st.selectbox("Main goal", GOALS, key="goal")
    language = st.selectbox("Video language", ["English", "Hindi", "Gujarati", "Hinglish", "Other / no dialogue"], key="language")
    audience = st.selectbox("Intended audience", ["General gaming audience", "Beginners", "Fans of this game", "Competitive players", "Story / lore fans", "Casual viewers"], key="audience")
    st.header("3. Creative categories")
    script_angle = st.selectbox("Script / story angle", ["Funny moments", "Scary / suspense", "Cinematic story", "Beginner guide", "Challenge / experiment", "Competitive highlights", "Secrets / discoveries", "Honest review", "Relaxing gameplay", "Reaction / commentary"], key="script_angle")
    edit_vibe = st.selectbox("Editing style", ["Fast meme cuts", "Cinematic slow build", "Horror suspense", "Clean tutorial", "Competitive montage", "Story documentary", "Cozy / relaxing", "High-energy Shorts", "Minimal raw gameplay"], key="edit_vibe")
    music_mood = st.selectbox("Music mood", ["Cinematic orchestral", "Funny / quirky", "Dark horror ambience", "High-energy electronic", "Emotional piano", "Chill lo-fi", "Epic action percussion", "No music / game audio only"], key="music_mood")
    title_style = st.selectbox("Title style", ["Curiosity", "Funny", "Scary", "Cinematic", "Tutorial / searchable", "Challenge", "Review / opinion"], key="title_style")
    description_tone = st.selectbox("Description tone", ["Friendly creator", "Cinematic / story", "Helpful tutorial", "Funny / casual", "Competitive / direct"], key="description_tone")
    tag_focus = st.selectbox("Tag strategy", ["Game + gameplay", "Tutorial / tips", "Funny moments", "Horror / reactions", "Cinematic / story", "Challenge", "Competitive / ranked"], key="tag_focus")
    st.caption("Tip: choose ‘Keep my typed game’ and enter any game name, or select a preset to fill it in. Check the game name displayed below the inputs.")

# One canonical URL builder: every search query is derived from the same game value.
def search_url(base, query):
    return base + quote_plus(query)

web_search = search_url("https://www.google.com/search?q=", f"{game} {genre if genre != 'Auto / not sure' else ''} gameplay tips latest news")
youtube_search = search_url("https://www.youtube.com/results?search_query=", f"{game} {style} gameplay")
official_search = search_url("https://www.google.com/search?q=", f"{game} official website publisher news patch notes")
trend_search = search_url("https://www.google.com/search?q=", f"gaming trends {game} YouTube videos {date.today().year}")

style_data = {
    "Cinematic": {
        "hook": "Open on the strongest visual, dramatic reveal, close call, or beautiful shot. Put context after the hook; skip a long intro.",
        "music": "Cinematic orchestral, emotional piano, atmospheric strings, or restrained tension build.",
        "keywords": "cinematic, orchestral, emotional piano, atmospheric, tension build, epic instrumental",
        "edit": "Use intentional cuts, let important shots breathe, add only a few motivated slow-motion moments, and preserve ambience and dialogue."
    },
    "Funny / entertaining": {
        "hook": "Start with the funniest fail, unexpected event, or reaction; explain only the context viewers need.",
        "music": "Playful pizzicato, quirky percussion, light funk, or short comedic stings.",
        "keywords": "comedy, playful, quirky, pizzicato, light funk, comedic instrumental",
        "edit": "Trim pauses, time cuts around the punchline, keep reactions clear, use occasional punch-in zooms/captions, and avoid sound-effect overload."
    },
    "Competitive / high-skill": {
        "hook": "Show the clutch, cleanest play, rank, or result immediately; quickly explain the stakes.",
        "music": "Driving electronic beats, energetic percussion, dark synth, or restrained action rock.",
        "keywords": "high energy, electronic, driving percussion, dark synth, action instrumental, intense",
        "edit": "Keep action readable, cut downtime, preserve key gameplay sounds, briefly label loadouts/strategies, and avoid effects that hide the play."
    },
    "Educational / tutorial": {
        "hook": "Show the problem and promised result first, then teach one clear method.",
        "music": "Low-volume neutral electronic, light lo-fi, or unobtrusive ambient instrumental.",
        "keywords": "minimal electronic, light lo-fi, calm background, tutorial, unobtrusive instrumental",
        "edit": "Use numbered steps, zooms only where needed, readable captions, before/after examples, and pauses long enough for viewers to follow."
    },
    "Challenge / experiment": {
        "hook": "State the rule and stakes in one sentence, then show a quick preview of the attempt.",
        "music": "Building percussion, playful suspense, or energetic electronic instrumental.",
        "keywords": "building tension, energetic electronic, suspense instrumental, challenge, percussion",
        "edit": "Show the rules on screen, remove repetitive attempts, keep meaningful failures, add progress markers, and make the final outcome clear."
    },
    "Chill / story-driven": {
        "hook": "Begin with a compelling story beat, discovery, atmosphere, or question without spoiling more than intended.",
        "music": "Ambient piano, gentle strings, atmospheric pads, or soft instrumental textures.",
        "keywords": "ambient piano, atmospheric, gentle strings, emotional instrumental, exploration",
        "edit": "Use longer shots when atmosphere matters, preserve dialogue, add subtle captions when useful, and avoid unnecessary transitions."
    }
}
selected_style = style_data[style]

# Dynamic content generated on each Streamlit rerun from the current input.
st.subheader("Current project")
st.markdown(f"**Game:** {game}  ·  **Platform:** {platform}  ·  **Category:** {genre}  ·  **Format:** {video_format}")
st.markdown(f"**Style:** {style}  ·  **Goal:** {goal}  ·  **Audience:** {audience}  ·  **Language:** {language}  ·  **Script angle:** {script_angle}")
st.caption(f"Creative direction: editing = {edit_vibe} · music = {music_mood} · title = {title_style} · description = {description_tone} · tags = {tag_focus}")

plan_tab, edit_tab, music_tab, research_tab, discovery_tab, publish_tab = st.tabs([
    "🎬 Video plan & script", "✂️ Editing step-by-step", "🎵 Music & licensing",
    "🔎 Game research", "🧭 Audience & game finder", "📅 Publish & measure"
])

with plan_tab:
    st.header(f"Video plan for {game}")
    st.write(f"**Concept:** Make a {style.lower()} video about one specific moment, question, challenge, discovery, or result in **{game}**. Avoid a generic montage unless the clips have a clear theme.")
    st.write("**Opening hook:** " + selected_style["hook"])
    if "Shorts" in video_format:
        st.subheader("Shorts structure (adapt to the idea; don't pad it)")
        st.markdown("- **0–2 seconds:** strongest moment or clear question.\n- **2–6 seconds:** minimum context viewers need.\n- **6–25 seconds:** action, explanation, escalation, or payoff.\n- **Final seconds:** result/reaction and a natural next-video prompt if relevant.")
    if "Long-form" in video_format or "Both" in video_format:
        st.subheader("Long-form structure")
        st.markdown("- **0:00–0:15:** cold open showing the promise of the video.\n- **0:15–0:45:** explain the goal, challenge, or question.\n- **Main section:** progress through 3–5 clear beats; remove repetitive dead time.\n- **Payoff:** show the result and what changed.\n- **Ending:** concise conclusion and relevant next-video suggestion; avoid a long outro.")
    angle_prompts = {
        "Funny moments": "Set up the situation quickly, leave room for the reaction, and land the punchline without over-explaining.",
        "Scary / suspense": "Build a question or threat, preserve important quiet audio, and delay the reveal until the footage earns it.",
        "Cinematic story": "Use a visual opening, establish the emotional or story context, and let key shots breathe.",
        "Beginner guide": "State the problem and result first, then explain each step in plain language.",
        "Challenge / experiment": "State the rule, stakes, and success condition before showing attempts.",
        "Competitive highlights": "Show the high-skill moment first, then explain the stakes and key decision.",
        "Secrets / discoveries": "Present a specific question, show how you tested it, and distinguish confirmed facts from guesses.",
        "Honest review": "Explain what you tested, what worked, what did not, and who may enjoy it.",
        "Relaxing gameplay": "Keep the pacing calm, preserve ambience, and avoid loud edits that break the mood.",
        "Reaction / commentary": "Use your genuine reaction and add context that makes the moment understandable to a new viewer."
    }
    st.subheader(f"Script starter — {script_angle}")
    st.write("**Direction:** " + angle_prompts[script_angle])
    script = f"""[HOOK — {script_angle}: show the strongest real moment from {game}]\n\nVOICE / CAPTION: “Today in {game}, I'm trying to [specific goal or question].”\n\n[CONTEXT] Explain the rule, mission, location, build, or problem in one or two sentences.\n\n[BEAT 1] Show the first meaningful attempt or discovery. Add a caption only if it improves understanding.\n\n[BEAT 2] Show escalation, a useful tip, a mistake, or a surprising turn.\n\n[PAYOFF] Show the actual result. Don't claim a win, secret, record, or discovery unless the footage proves it.\n\n[ENDING] “Would you try this in {game}? What should I test next?” (Use only if it fits your audience.)"""
    st.text_area("Copy and customize this script", value=script, height=300, key="script_output")
    st.subheader("Title ideas")
    title_templates = {
        "Curiosity": [f"I Didn't Expect This in {game}", f"What Happens If You Try This in {game}?", f"The Detail I Nearly Missed in {game}"],
        "Funny": [f"{game} Went Completely Wrong", f"My Funniest {game} Moment Yet", f"I Thought This Would Work in {game}"],
        "Scary": [f"The Creepiest Moment I Found in {game}", f"I Was Not Ready for This in {game}", f"Playing {game} With the Lights Off"],
        "Cinematic": [f"A Cinematic Moment in {game}", f"{game} Looks Unreal in This Scene", f"A Quiet, Beautiful Moment in {game}"],
        "Tutorial / searchable": [f"{game}: Beginner Tips to Know First", f"How to Improve at {game}", f"{game} Guide: A Simple Way to Start"],
        "Challenge": [f"Can I Beat This Challenge in {game}?", f"I Tried {game} With One Rule", f"Can This Strategy Work in {game}?"],
        "Review / opinion": [f"Is {game} Worth Playing? My Honest Take", f"What {game} Does Well — and What It Doesn't", f"Who Should Play {game}?"]
    }
    title_ideas = title_templates[title_style]
    for t in title_ideas:
        st.markdown(f"- {t}")
    st.caption("Treat titles as drafts. Keep only claims your actual footage proves; don't use fake urgency or misleading promises.")
    st.subheader(f"Description and tags — {description_tone} / {tag_focus}")
    tone_openers = {
        "Friendly creator": f"Hey everyone! In this video, we're playing {game} and exploring the moment shown in the footage.",
        "Cinematic / story": f"A cinematic gameplay moment from {game}, focused on atmosphere, story, and the scene itself.",
        "Helpful tutorial": f"This video covers a practical {game} tip. Check the steps below and adapt them to your version of the game.",
        "Funny / casual": f"Things did not go exactly to plan in {game}. Here's the moment and how it played out.",
        "Competitive / direct": f"A focused {game} gameplay session highlighting decisions, mechanics, and the final result."
    }
    description = f"{tone_openers[description_tone]}\n\nWhat happens: [write a short, accurate summary of this actual video].\n\nPlatform: {platform}\nGame: {game}\nFormat: {video_format}\nStyle: {style}\n\nMusic: [add track credit here if required by the licence].\n\nSubscribe or comment with a relevant suggestion if you want to see more."
    st.text_area("Description template (customize before uploading)", value=description, height=180, key="description_template")
    tag_templates = {
        "Game + gameplay": [game, f"{game} gameplay", f"{game} {platform}", f"{game} walkthrough", f"{game} highlights"],
        "Tutorial / tips": [game, f"{game} tips", f"{game} beginner guide", f"how to play {game}", f"{game} tutorial"],
        "Funny moments": [game, f"{game} funny moments", f"funny {game} gameplay", f"{game} fails", f"gaming funny moments"],
        "Horror / reactions": [game, f"{game} horror gameplay", f"{game} scary moments", f"{game} reaction", f"scary gaming"],
        "Cinematic / story": [game, f"{game} cinematic", f"{game} story", f"{game} cutscenes", f"cinematic gameplay"],
        "Challenge": [game, f"{game} challenge", f"{game} challenge run", f"{game} experiment", f"gaming challenge"],
        "Competitive / ranked": [game, f"{game} ranked", f"{game} competitive gameplay", f"{game} best plays", f"{game} tips"]
    }
    st.text_input("Relevant tag ideas (remove anything that doesn't match)", value=", ".join(tag_templates[tag_focus]), key="tag_ideas")
    st.caption("Tags are secondary to an accurate title, thumbnail, topic, and viewer response. Do not add unrelated trending terms.")

with edit_tab:
    st.header("Editing coach — detailed workflow")
    device = st.radio("Where will you edit?", ["Mobile phone / tablet", "PC / laptop"], horizontal=True, key="edit_device")
    if device.startswith("Mobile"):
        editor = st.selectbox("Editing app", ["CapCut", "VN", "InShot", "YouTube Create", "Other mobile editor"], key="mobile_editor")
        st.write(f"**Workflow for {editor}:**")
        steps = [
            "Create a new project and select the target aspect ratio before trimming.",
            "Import the original gameplay recording; duplicate the project if making both vertical and horizontal versions.",
            "Put the strongest moment first. Remove loading screens, repeated attempts, long pauses, and unrelated clips.",
            "Arrange the clips into a clear beginning, development, and payoff. Keep enough context that viewers understand what happened.",
            "Add captions or short labels for dialogue, tips, rules, loadouts, or locations. Check spelling and phone-safe margins.",
            "Adjust crop/reframe for vertical video; keep the important character, action, UI, and subtitles visible.",
            "Balance gameplay/dialogue first, music lower underneath, and sound effects only where they help. Listen with headphones.",
            "Use transitions and effects sparingly. Add color correction only if it improves clarity and consistency.",
            "Export, watch the entire file, check black frames/audio/captions, then upload."
        ]
    else:
        editor = st.selectbox("Editing app", ["DaVinci Resolve", "Adobe Premiere Pro", "CapCut Desktop", "Other PC editor"], key="pc_editor")
        st.write(f"**Workflow for {editor}:**")
        steps = [
            "Create a project, set the timeline to the intended resolution/frame rate, and organize gameplay, audio, and music tracks.",
            "Import and review footage; mark the best moments before assembling the timeline.",
            "Build a rough cut around one idea. Remove dead time, repetitive attempts, and clips that don't advance the story.",
            "Refine pacing and audio continuity; use J/L cuts only where they help the story or commentary.",
            "Add readable captions, labels, chapters, or callouts. Keep text within safe margins and avoid covering important UI.",
            "Reframe a duplicate sequence for vertical Shorts rather than blindly cropping a horizontal master.",
            "Balance dialogue/gameplay, music, and effects. Listen on headphones and phone speakers if possible.",
            "Apply restrained color correction and effects; prioritize readable gameplay and stable playback.",
            "Export a high-quality H.264 MP4 preset as a starting point, then watch the full export before uploading."
        ]
    for i, step in enumerate(steps, 1):
        st.markdown(f"**Step {i}.** {step}")
    st.subheader("Export starting points")
    st.markdown("- **Shorts:** vertical 9:16, commonly 1080 × 1920.\n- **Long-form:** horizontal 16:9, commonly 1920 × 1080 if your source supports it.\n- **Frame rate:** normally match the source (often 30 or 60 fps); exporting 30 fps footage at 60 fps doesn't create extra captured detail.\n- **Format:** high-quality H.264 MP4 is a practical starting point. Exact options differ by app/device.")
    st.subheader(f"Editing direction — {edit_vibe}")
    edit_vibe_guidance = {
        "Fast meme cuts": "Keep only setup, reaction, and payoff. Use quick punch-ins sparingly, subtitle the key joke, and avoid stacking too many sounds at once.",
        "Cinematic slow build": "Open with a striking shot, use longer shots, subtle speed changes only where justified, restrained color grading, and music that builds into the payoff.",
        "Horror suspense": "Preserve quiet ambience, lower music under important game sounds, cut before/after tension deliberately, and avoid spoiling the scare in the opening.",
        "Clean tutorial": "Use numbered steps, zooms on the relevant UI, clear captions, before/after proof, and remove any step that doesn't help the viewer.",
        "Competitive montage": "Synchronize cuts to meaningful plays, keep HUD/action visible, use speed ramps sparingly, and preserve enough lead-in to understand each play.",
        "Story documentary": "Organize clips chronologically or by argument, use voice-over to bridge gaps, and avoid music over essential dialogue.",
        "Cozy / relaxing": "Use gentle cuts, preserve ambient sound, keep music quiet, and avoid unnecessary overlays or sudden volume jumps.",
        "High-energy Shorts": "Show the payoff immediately, use readable captions, reframe to vertical safely, and keep each beat moving toward one clear outcome.",
        "Minimal raw gameplay": "Trim dead time, keep authentic game audio, add only essential labels, and avoid effects that make the gameplay harder to read."
    }
    st.write(edit_vibe_guidance[edit_vibe])
    st.write("**Style baseline:** " + selected_style["edit"])
    st.subheader("Editing timeline")
    if "Shorts" in video_format:
        timeline = ["0–2 s: show the strongest moment or question; no logo intro.", "2–6 s: add only the context needed to understand the moment.", "6–20 s: develop the action, joke, tip, or tension; remove pauses.", "20 s to payoff: deliver the result and end cleanly; use only the length the idea needs."]
    else:
        timeline = ["Opening: show the promised outcome or an intriguing moment before greetings.", "Setup: explain the goal, rules, or question in a few sentences.", "Middle: build 3–5 distinct beats; cut repetition and label useful context.", "Payoff: show the actual outcome and explain what it means.", "Ending: brief conclusion and a relevant next-video invitation, if natural."]
    for i, beat in enumerate(timeline, 1):
        st.markdown(f"**Timeline {i}.** {beat}")
    st.checkbox("Aspect ratio and resolution checked", key="check_aspect")
    st.checkbox("Frame rate matches source where practical", key="check_fps")
    st.checkbox("Gameplay/dialogue is clear and music doesn't drown it out", key="check_audio")
    st.checkbox("Captions and export checked from start to finish", key="check_export")

with music_tab:
    st.header(f"Music mood and licensing for {game}")
    music_catalog = {
        "Cinematic orchestral": ("orchestral build, cinematic tension, epic instrumental, strings, trailer percussion", "Use a gradual build; let the strongest visual land with the musical rise."),
        "Funny / quirky": ("playful pizzicato, quirky percussion, light funk, comedic instrumental, cartoon pluck", "Use short accents around the joke; keep them lower than dialogue and game audio."),
        "Dark horror ambience": ("dark ambient drone, suspense texture, eerie piano, tension pulse, horror atmosphere", "Leave quiet gaps so footsteps, warnings, and game ambience remain audible."),
        "High-energy electronic": ("high energy electronic, driving beat, synth bass, action instrumental", "Match beat changes to meaningful gameplay moments, not every cut."),
        "Emotional piano": ("emotional piano, reflective instrumental, gentle strings, melancholic ambient", "Use softer music under story scenes and avoid masking dialogue."),
        "Chill lo-fi": ("lo-fi instrumental, mellow beat, warm ambient, relaxed background music", "Keep the beat steady and low so gameplay remains the focus."),
        "Epic action percussion": ("epic percussion, cinematic drums, action rhythm, energetic instrumental", "Use the biggest hits for actual stakes or payoff; avoid constant loudness."),
        "No music / game audio only": ("no music, original game audio, ambience, gameplay sound", "Prioritize clean game audio and voice; check the game's own music/copyright settings.")
    }
    music_terms, music_edit_tip = music_catalog[music_mood]
    st.write(f"**Chosen music category:** {music_mood}")
    st.write(f"**Direction for {style.lower()} gameplay:** {selected_style['music']}")
    st.write("**Search keywords for YouTube Audio Library:** " + music_terms)
    st.write("**Mixing tip:** " + music_edit_tip)
    st.write("**Additional style keywords:** " + selected_style["keywords"])
    st.markdown("[Open YouTube Audio Library](https://youtube.com/audiolibrary)")
    st.markdown("[Read YouTube's official Audio Library guidance](https://support.google.com/youtube/answer/3376882)")
    st.warning("This app recommends music moods and search terms; it does not select or verify an individual track. Check that specific track's licence, commercial/monetization terms, platform use, and attribution requirements. YouTube Audio Library is the safer starting point; third-party ‘no copyright’ labels alone are not proof of permission.")
    st.subheader("Before using a track")
    st.checkbox("I found the track in YouTube Audio Library or have clear permission", key="music_permission")
    st.checkbox("I checked this track's exact terms for monetization and use", key="music_terms")
    st.checkbox("I copied required attribution exactly into the description", key="music_credit")
    st.checkbox("I confirmed the track suits this video format and length", key="music_format")

with research_tab:
    st.header(f"Research: {game}")
    st.success(f"All search links below are generated from your current game name: **{game}**")
    st.write("These buttons open external search pages. Review dates, platforms, editions, sources, and results yourself; this app does not automatically read or verify the pages.")
    st.link_button(f"Search YouTube for {game} videos", youtube_search, use_container_width=True)
    st.link_button(f"Search the web for {game} tips and news", web_search, use_container_width=True)
    st.link_button(f"Find official {game} / publisher information", official_search, use_container_width=True)
    st.link_button(f"Research trends related to {game}", trend_search, use_container_width=True)
    st.subheader("Research questions")
    st.markdown(f"- What are viewers asking about **{game}** right now?\n- Which recent videos about **{game}** are getting discussion, and what is genuinely different about them?\n- Are updates, releases, modes, or platform versions current?\n- Can you make an original video based on your own gameplay rather than copying another creator?")
    custom_query = st.text_input("Add a specific research question", placeholder=f"e.g. best beginner settings for {game}", key="research_question")
    if custom_query.strip():
        st.link_button("Search this question", search_url("https://www.google.com/search?q=", f"{game} {custom_query.strip()}"), use_container_width=True)

with discovery_tab:
    st.header("Audience & Game Finder")
    st.write("Use this to shortlist games that fit your audience, platform, category, and spending limit. It uses searches and the information you provide; it does not automatically retrieve live trends or comments.")
    col1, col2 = st.columns(2)
    with col1:
        finder_platform = st.selectbox("Platform you can play on", PLATFORMS, key="finder_platform")
        finder_category = st.selectbox("Category to explore", ["Any category"] + GENRES[1:], key="finder_category")
        budget = st.selectbox("Maximum game budget", ["Free-to-play only", "₹500", "₹1,000", "₹2,000", "₹5,000", "No fixed budget"], key="finder_budget")
    with col2:
        pc_cpu = st.text_input("PC CPU (PC only)", placeholder="e.g. Intel Core i5-7500", key="pc_cpu")
        pc_gpu = st.text_input("PC GPU (PC only)", placeholder="e.g. Intel HD Graphics 630", key="pc_gpu")
        pc_ram = st.selectbox("PC RAM (PC only)", ["Not applicable / unsure", "4 GB", "8 GB", "16 GB", "32 GB or more"], key="pc_ram")
    audience_notes = st.text_area("Audience clues (optional)", placeholder="What do viewers ask for? What are your top videos about?", key="audience_notes")
    comment_text = st.text_area("Paste viewer comments (optional)", placeholder="Paste comments you are allowed to use. Remove personal details.", key="comment_text")
    if st.button("Build game discovery searches", type="primary", key="discover_games"):
        cat = "" if finder_category == "Any category" else finder_category
        queries = [
            f"best trending {cat} games {finder_platform} {date.today().year}",
            f"new and upcoming {cat} games {finder_platform} {date.today().year}",
            f"popular {cat} games on YouTube {finder_platform} {date.today().year}"
        ]
        if budget != "No fixed budget":
            queries = [q + (" free" if budget == "Free-to-play only" else f" under {budget}") for q in queries]
        if finder_platform == "PC / laptop" and pc_gpu.strip():
            queries.append(f"games playable on {pc_gpu} {pc_cpu} {pc_ram} RAM minimum requirements")
        st.subheader("Three research routes")
        for i, q in enumerate(queries[:3], 1):
            st.markdown(f"**Research route {i}:** {q}")
            st.link_button(f"Open search {i}", search_url("https://www.google.com/search?q=", q), key=f"discover_link_{i}")
        st.caption("Compare at least two sources, confirm the exact platform/edition and current price, and don't treat search ranking alone as proof that a game is trending.")
        if finder_platform == "PC / laptop":
            st.info("PC compatibility requires checking the exact CPU, GPU, RAM, OS, storage, and the game's minimum/recommended requirements. Search results are not a benchmark; frame rate cannot be guaranteed from these fields alone.")
        if audience_notes.strip() or comment_text.strip():
            st.subheader("Audience clues you supplied")
            combined = (audience_notes + " " + comment_text).lower()
            # Lightweight keyword counts, clearly labelled as simple text clues rather than AI sentiment.
            terms = ["game", "story", "horror", "racing", "multiplayer", "tutorial", "tips", "challenge", "minecraft", "call of duty", "gta", "fortnite", "price", "free"]
            found = [(term, combined.count(term)) for term in terms if combined.count(term) > 0]
            if found:
                st.write("Repeated keyword clues: " + ", ".join(f"{term} ({count})" for term, count in sorted(found, key=lambda x: x[1], reverse=True)))
            else:
                st.write("No keywords from the simple built-in list were detected. Review the comments manually for requests and questions.")
            st.caption("This is basic keyword counting, not sentiment analysis, demographic analysis, or a direct connection to YouTube comments.")

with publish_tab:
    st.header("Publishing plan & what to measure")
    upload_date = st.date_input("Planned upload date", value=date.today() + timedelta(days=1), key="upload_date")
    time_window = st.selectbox("Posting window to test (local time)", ["Morning", "Afternoon", "Evening", "Late evening"], index=2, key="posting_window")
    cadence = st.selectbox("Sustainable cadence", ["One video a week", "Two videos a week", "Three Shorts a week", "One Short + one long video a week", "Flexible / learning first"], key="cadence")
    st.write(f"**Plan:** {cadence}; target date **{upload_date.strftime('%d %b %Y')}**; test the **{time_window.lower()}** window.")
    st.warning("There is no universal best posting time. Treat this as a test window, then use YouTube Studio → Analytics → Audience and your own performance data to adjust. This app cannot see your audience activity automatically.")
    st.subheader("After publishing, review")
    st.markdown("- **Reach:** impressions and traffic sources.\n- **Packaging:** click-through rate (CTR), compared with your own channel's usual results and traffic source.\n- **Retention:** first 30 seconds for long-form, and viewed-versus-swiped-away/retention for Shorts where available.\n- **Engagement:** meaningful comments, likes, shares, and returning viewers.\n- **Next experiment:** change one thing at a time—hook, topic, thumbnail/title, or pacing.")
    st.markdown("[Open YouTube Studio](https://studio.youtube.com/)")
    st.checkbox("Recording backed up and edit/export checked", key="pub_backup")
    st.checkbox("Title and thumbnail accurately match the video", key="pub_title")
    st.checkbox("Description, relevant tags, and music permissions checked", key="pub_description")
    st.checkbox("Visibility, audience setting, and restrictions checked after upload", key="pub_visibility")

st.divider()
st.caption("PS5 YouTube Coach • Free planning starter • No automatic YouTube account access, live trend verification, licence verification, upload scheduling, or guaranteed growth in this version.")
