import streamlit as st
from urllib.parse import quote_plus
from datetime import date

st.set_page_config(page_title="PS5 YouTube Coach", page_icon="🎮", layout="wide")

st.title("🎮 PS5 YouTube Coach")
st.caption("A practical planning coach for gaming creators — built to work with any game, including future releases.")
st.info("This free version uses structured coaching rules and templates. It does not use a live AI model, automatically inspect your YouTube channel, verify current game facts, upload videos, or guarantee views/monetization. It creates a plan immediately and gives you research links to check game-specific details when you want them.")

with st.sidebar:
    st.header("Your video")
    game_choice = st.selectbox("Choose a game or enter your own", [
        "Ghost of Tsushima", "Grand Theft Auto V", "Grand Theft Auto VI", "Minecraft",
        "Forza Horizon 6", "The Last of Us Part I", "The Last of Us Part II",
        "God of War (2018)", "God of War Ragnarök", "Other / future game"
    ])
    custom_game = st.text_input("Game name (for Other, or to specify a different game)", placeholder="e.g. an upcoming game")
    game = custom_game.strip() if custom_game.strip() else game_choice
    genre = st.selectbox("Game genre (optional but helpful)", [
        "Auto / not sure", "Action-adventure", "Open-world", "RPG", "Racing", "Shooter / FPS",
        "Survival / horror", "Sandbox / building", "Sports / fighting", "Story-driven", "Other"
    ])
    format_choice = st.selectbox("Video format", ["Shorts", "Long-form video", "Both (Short + long video)"])
    style = st.selectbox("Video style", [
        "Cinematic", "Funny / entertaining", "Competitive / high-skill", "Educational / tutorial",
        "Challenge / experiment", "Chill / story-driven"
    ])
    goal = st.selectbox("Main goal", [
        "More views / discovery", "Improve click-through rate (CTR)", "Improve retention / watch time",
        "Gain subscribers / community", "Monetize safely", "Post consistently / improve skills"
    ])
    audience = st.selectbox("Target audience", ["General gaming audience", "Beginners", "Fans of the game", "Competitive players", "Story / lore fans"])
    creator_language = st.selectbox("Video language", ["English", "Hindi", "Gujarati", "Hinglish", "Other / no dialogue"])
    create = st.button("Build my coaching plan", type="primary", use_container_width=True)

if not game.strip():
    game = "your selected game"

styles = {
    "Cinematic": {
        "hook": "Open with your most visually striking moment, a surprising reveal, or a dramatic near-failure. Avoid a long logo intro.",
        "edit": "Use deliberate pacing, clean cuts, a few motivated slow-motion moments, restrained color correction, and game audio under the music.",
        "music": "Cinematic orchestral build, emotional piano, atmospheric strings, or subtle tension pulses.",
        "keywords": "cinematic, orchestral, emotional piano, epic build, atmospheric, tension",
        "thumb": "Choose one dramatic frame with a clear subject and readable silhouette; keep text short (2–4 words) and contrast strong."
    },
    "Funny / entertaining": {
        "hook": "Start with the funniest failure, unexpected NPC moment, or punchline; set up context only after the hook.",
        "edit": "Trim pauses aggressively, keep reaction audio understandable, use occasional zooms or captions for punchlines, and don't overuse sound effects.",
        "music": "Playful pizzicato, quirky percussion, light funk, or short comedic stings.",
        "keywords": "playful, quirky, comedy, pizzicato, light funk, comedic",
        "thumb": "Use a clear reaction or absurd in-game moment; one expressive focal point and a short curiosity-building phrase."
    },
    "Competitive / high-skill": {
        "hook": "Show the clutch, cleanest play, record, or result in the first seconds, then quickly explain the stakes.",
        "edit": "Keep gameplay readable, cut downtime, preserve key game sounds, use brief labels for loadout/strategy, and avoid effects that hide the action.",
        "music": "Driving electronic beats, energetic percussion, dark synth, or restrained high-energy rock.",
        "keywords": "high energy, electronic, driving percussion, dark synth, action, intense",
        "thumb": "Make the key play or result obvious at phone size; use one focal subject and a short result/claim you can prove."
    },
    "Educational / tutorial": {
        "hook": "State the exact problem and the result viewers will learn in one sentence; show a quick preview of the outcome.",
        "edit": "Use numbered steps, readable captions, close-ups of menus when needed, and remove repeated explanations. Verify every tip in-game.",
        "music": "Soft electronic, light lo-fi, or unobtrusive instrumental music kept well below speech.",
        "keywords": "light electronic, lo-fi instrumental, focus, minimal, tutorial background",
        "thumb": "Show the problem and result together if possible; use a specific phrase such as '3 EASY TIPS' rather than vague clickbait."
    },
    "Challenge / experiment": {
        "hook": "State the rule, restriction, or question and the stakes immediately; tease the outcome without spoiling everything.",
        "edit": "Make the rules easy to follow, show meaningful attempts, build tension toward the result, and cut repetitive failures unless they add comedy.",
        "music": "Rhythmic build, playful tension, adventure percussion, or energetic instrumental cues.",
        "keywords": "challenge, tension build, adventure, rhythmic percussion, playful suspense",
        "thumb": "Show the challenge visually and communicate the restriction with only a few words; don't imply a result that didn't happen."
    },
    "Chill / story-driven": {
        "hook": "Open on an intriguing story beat, beautiful environment, or thoughtful question; make the mood clear.",
        "edit": "Keep dialogue and story context intact, use gentle transitions sparingly, balance music beneath speech, and avoid spoilers in titles/thumbnails.",
        "music": "Ambient pads, gentle piano, atmospheric instrumental, or calm exploration music.",
        "keywords": "ambient, atmospheric, gentle piano, exploration, calm instrumental, cinematic ambient",
        "thumb": "Use a strong environment or character composition; if the video contains spoilers, avoid revealing them in the thumbnail."
    }
}

# Genre-aware guidance that does not pretend to know a game's current details.
def genre_note(g):
    notes = {
        "Action-adventure": "Prioritize clear combat, traversal, and story context; avoid cutting so fast that viewers lose track of the action.",
        "Open-world": "Build around a specific discovery, mission, location, or experiment rather than a generic 'gameplay' upload.",
        "RPG": "Make the build, choice, quest, or outcome explicit; explain any jargon needed by new viewers.",
        "Racing": "Show the car/event/settings or challenge early; keep speed readable and mix engine audio with music carefully.",
        "Shooter / FPS": "Make the objective and stakes clear; keep HUD and important audio readable and don't obscure aiming/action.",
        "Survival / horror": "Use suspenseful pacing, preserve important ambience, and clearly label spoilers if discussing story events.",
        "Sandbox / building": "Show the final build/result early, then the process; use progress markers or before/after comparisons.",
        "Sports / fighting": "Show the matchup, goal, or key technique; keep score/UI visible and explain rules when helpful.",
        "Story-driven": "Protect narrative context and avoid spoiler thumbnails/titles unless the video is explicitly spoiler-marked.",
        "Other": "Pick one clear viewer promise and explain the game-specific context instead of assuming everyone knows it."
    }
    return notes.get(g, "Choose one specific moment, problem, discovery, or result to make the video distinct.")

st.divider()
tabs = st.tabs(["🎬 Video Planner", "✂️ Editing Coach", "🎵 Music & Licensing", "🖼️ Thumbnail + SEO", "📈 Channel Fixes", "📅 Upload Planner", "🔎 Game Research"])

with tabs[0]:
    st.subheader("Your starter plan")
    st.write(f"**Game:** {game}  ·  **Format:** {format_choice}  ·  **Style:** {style}")
    st.write(f"**Goal:** {goal}  ·  **Audience:** {audience}  ·  **Language:** {creator_language}")
    st.markdown("#### Video concept")
    if style == "Cinematic":
        concept = f"A cinematic highlight/story sequence from {game}, built around one memorable encounter, location, or turning point."
    elif style == "Funny / entertaining":
        concept = f"The most unexpected, funny, or chaotic moments from {game}, edited into a compact story with a clear punchline."
    elif style == "Competitive / high-skill":
        concept = f"A skill-focused {game} run, clutch, race, fight, or challenge where the result is easy to understand."
    elif style == "Educational / tutorial":
        concept = f"A beginner-friendly {game} guide that solves one specific problem and demonstrates the result."
    elif style == "Challenge / experiment":
        concept = f"A {game} challenge with one clear rule, escalating attempts, and a satisfying final result."
    else:
        concept = f"A relaxed, story-focused or exploration-led {game} episode with clear context and a consistent mood."
    st.write(concept)
    st.markdown("#### Hook and structure")
    st.write("**Opening hook:** " + styles[style]["hook"])
    st.write("**Genre-aware note:** " + genre_note(genre))
    if format_choice in ["Shorts", "Both (Short + long video)"]:
        st.markdown("**Shorts structure (roughly 20–45 seconds):**")
        st.write("0–2s: strongest moment or question → 2–7s: essential context → 7–30s: payoff/escalation → final seconds: result, reaction, or a natural reason to watch another clip. Adjust length to the idea; don't pad it.")
    if format_choice in ["Long-form video", "Both (Short + long video)"]:
        st.markdown("**Long-form structure (adapt to the footage):**")
        st.write("0–15s: promise + preview → early section: context and stakes → middle: meaningful progress, turns, or useful steps → final section: result/payoff → brief ending that points to a related video. Remove dead time; don't force a length.")
    st.markdown("#### Title ideas")
    title_templates = [
        f"I Didn't Expect This in {game}",
        f"The Best Moment I Captured in {game}",
        f"{game}: One Challenge, One Rule, Can I Do It?",
        f"{game} Tips I Wish I Knew Earlier"
    ]
    if style == "Cinematic": title_templates[0] = f"A Cinematic Moment in {game} That Feels Unreal"
    if style == "Funny / entertaining": title_templates[0] = f"{game} Went Completely Wrong 😂"
    if style == "Competitive / high-skill": title_templates[0] = f"My Cleanest {game} Play Yet"
    if style == "Educational / tutorial": title_templates[0] = f"How to Get Better at {game}: A Simple Guide"
    if style == "Challenge / experiment": title_templates[0] = f"I Tried a Nearly Impossible {game} Challenge"
    if style == "Chill / story-driven": title_templates[0] = f"A Quiet, Cinematic Journey Through {game}"
    for t in title_templates: st.write("- " + t)
    st.caption("Treat these as drafts. Keep only claims that your actual footage proves; avoid fake urgency or misleading titles.")
    st.markdown("#### Retention checklist")
    for item in ["Start with the promised moment; skip long greetings and logos.", "Make the video about one main idea, not unrelated clips.", "Remove loading screens, repeated attempts, and silence unless they matter.", "Use captions or on-screen labels where context is easy to miss.", "Deliver the result promised by the title and thumbnail.", "Review audience-retention dips after publishing and use them to improve the next edit."]:
        st.checkbox(item, key="plan_" + item)

with tabs[1]:
    st.subheader("Editing coach — mobile and PC")
    device = st.radio("Where will you edit?", ["Mobile phone / tablet", "PC / laptop"], horizontal=True)
    app_options = ["CapCut", "VN Video Editor", "InShot", "YouTube Create", "DaVinci Resolve", "Adobe Premiere Pro", "Other / not chosen"]
    editor = st.selectbox("Editing app", app_options)
    skill = st.select_slider("Editing experience", options=["Beginner", "Some experience", "Confident"])
    source_fps = st.selectbox("Gameplay recording frame rate (if known)", ["Not sure", "30 fps", "60 fps", "120 fps"])
    target_format = st.selectbox("Editing output", ["Vertical 9:16 (Shorts)", "Horizontal 16:9 (long-form)", "Both versions"])
    if device.startswith("Mobile"):
        st.markdown("**Mobile workflow**")
        st.write(f"In {editor}, create a project and set the canvas to the intended format before editing. Import clips, duplicate the project before making a second format, trim dead time, arrange the story, add readable captions, then balance audio and export.")
        st.write("If the app offers it: use 1080 × 1920 for vertical Shorts and 1920 × 1080 for horizontal videos. Export at the same frame rate as the source when practical (often 30 or 60 fps). Avoid exporting 60 fps from 30 fps footage expecting extra detail.")
        st.write("Phone tips: keep enough free storage, close heavy apps if preview stutters, use headphones for audio checks, and watch the exported file once before uploading.")
    else:
        st.markdown("**PC workflow**")
        st.write(f"In {editor}, create a timeline matching the intended aspect ratio and source frame rate. Organize clips, mark selects, build the story, tighten pacing, add captions/graphics, mix audio, apply restrained color correction, and export a review copy before the final render.")
        st.write("Common starting point: 1920 × 1080 for horizontal or 1080 × 1920 for vertical; 30 or 60 fps to match source footage. Use the editor's H.264 MP4 preset and a high-quality/target-bitrate setting. Exact bitrate options vary by app and source; don't upscale low-resolution footage just to inflate the numbers.")
    st.markdown("**Export and edit checklist**")
    checklist = [
        "Aspect ratio matches the upload destination (9:16 vertical or 16:9 horizontal).",
        "Resolution matches the footage where possible; avoid unnecessary upscaling.",
        "Frame rate matches the recording unless there is a deliberate reason to change it.",
        "Gameplay/dialogue is clear; music does not drown out speech or important game audio.",
        "Captions are spelled correctly and stay inside safe margins on a phone screen.",
        "Transitions and effects support the moment instead of hiding gameplay.",
        "Exported file plays from start to finish, with no black frames or accidental mute sections.",
        "Thumbnail/title do not reveal story spoilers unless intended and clearly labelled."
    ]
    for i, item in enumerate(checklist): st.checkbox(item, key=f"editcheck_{i}")
    st.markdown("**Simple pacing guide**")
    if style in ["Competitive / high-skill", "Funny / entertaining"]:
        st.write("Try tighter cuts and faster context, but leave enough frames for viewers to understand the play or joke. Cut pauses, not clarity.")
    elif style in ["Cinematic", "Chill / story-driven"]:
        st.write("Let important shots and story beats breathe; use fewer, more intentional transitions and preserve ambience/dialogue.")
    else:
        st.write("Use a clear step-by-step progression and remove repetition while keeping enough context to follow each step.")
    st.caption("Export controls and exact bitrate labels differ between apps and device versions; use the app's high-quality H.264 MP4 preset as a starting point.")

with tabs[2]:
    st.subheader("Music mood and licensing check")
    st.write(f"**Suggested direction for {style.lower()} {game} video:** {styles[style]['music']}")
    st.write("**Search keywords for YouTube Audio Library:** " + styles[style]["keywords"])
    st.link_button("Open YouTube Audio Library", "https://youtube.com/audiolibrary")
    st.link_button("Read YouTube's official Audio Library licensing guidance", "https://support.google.com/youtube/answer/3376882?hl=en-GB")
    st.markdown("#### Before you use a track")
    music_checks = [
        "I found the track in YouTube Studio's Audio Library or have a clear licence/permission for this use.",
        "I checked the specific track's terms for monetization, platform, territory, and any other restrictions.",
        "If attribution is required, I copied the exact attribution text and added it to the description.",
        "I did not assume that a track is safe just because a video or website calls it 'no copyright' or 'royalty-free'.",
        "I checked whether the track is suitable for this video's length and format; Shorts music permissions may differ from long-form use."
    ]
    for i, item in enumerate(music_checks): st.checkbox(item, key=f"music_{i}")
    st.warning("This is a checklist, not a live track-by-track licence verification. YouTube says Audio Library tracks are its known copyright-safe source; third-party 'royalty-free' labels alone are not a guarantee. See the official guidance above.")

with tabs[3]:
    st.subheader("Thumbnail, title, description and tags")
    st.write("**Thumbnail direction:** " + styles[style]["thumb"])
    st.write("Aim for one main subject, strong contrast, uncluttered composition, and text readable at small phone size. Check that the thumbnail accurately represents the actual video.")
    uploaded_image = st.file_uploader("Optional: upload a thumbnail screenshot for your own reference", type=["png", "jpg", "jpeg", "webp"])
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded reference image", use_container_width=True)
        st.info("This version can display your image, but it does not automatically understand or diagnose the image. Use the manual checks below for feedback.")
    issue = st.selectbox("What do you want to improve?", ["Thumbnail looks cluttered", "Text hard to read", "Low CTR", "Title unclear", "Not sure"])
    if issue == "Thumbnail looks cluttered": st.write("Try removing secondary subjects and reducing text to one short phrase. Zoom out to phone size and check whether the main idea is still obvious.")
    elif issue == "Text hard to read": st.write("Use fewer words, larger type, strong contrast, and safe margins. Avoid thin fonts over busy backgrounds.")
    elif issue == "Low CTR": st.write("Compare the promise in title and thumbnail with the actual opening. Test one meaningful change at a time after enough impressions; CTR varies by traffic source and audience.")
    elif issue == "Title unclear": st.write("Name the game or topic and the specific payoff, challenge, or question. Avoid vague titles that could describe thousands of videos.")
    else: st.write("Ask someone to glance at the thumbnail for two seconds, then say what they expect the video to show. If their answer is wrong, simplify the visual promise.")
    st.markdown("**Description template**")
    description = f"In this video, I play {game} in a {style.lower()} style.\n\nWhat happens: [brief, accurate summary]\n\n🎮 Game: {game}\n🎬 Format: {format_choice}\n\n[Add your own channel links, chapters, and any required music attribution here.]"
    st.text_area("Copy and customize this description", value=description, height=170)
    st.markdown("**Tag ideas (use only relevant tags)**")
    tags = [game, game + " gameplay", game + " highlights", game + " tips", "PS5 gameplay", "gaming", style.lower() + " gaming"]
    st.code(", ".join(tags), language=None)
    st.caption("Tags have a limited discovery role compared with the video's actual topic, title, thumbnail, and viewer response. Don't add unrelated trending tags.")

with tabs[4]:
    st.subheader("Channel troubleshooting")
    problem = st.selectbox("What is happening?", [
        "Almost zero views", "Impressions but low CTR", "People leave early / low retention",
        "Copyright claim", "Limited ads / monetization concern", "Video stuck processing or not visible",
        "Not gaining subscribers", "I am not sure"
    ])
    if problem == "Almost zero views":
        advice = ["Check that the video is Public and processing is complete.", "Confirm the title clearly names the actual topic/game and the opening delivers that promise.", "Give a new upload time to gather data; don't repeatedly delete and re-upload without a reason.", "Check impressions, traffic sources, and restrictions in YouTube Studio before changing everything."]
    elif problem == "Impressions but low CTR":
        advice = ["Check whether the thumbnail is readable at phone size and the title gives a specific reason to click.", "Compare CTR by traffic source and impressions; numbers vary by audience and surface.", "Change one meaningful element at a time and avoid misleading promises."]
    elif problem == "People leave early / low retention":
        advice = ["Open on the payoff, problem, or strongest moment instead of a long intro.", "Use the retention graph to locate drop-offs, then check what happens at those timestamps.", "Remove repeated footage and deliver the title's promise earlier."]
    elif problem == "Copyright claim":
        advice = ["Open YouTube Studio > Content > Restrictions/Copyright details to identify the claimed material.", "Check the claimant, timestamps, and the actual licence before disputing.", "If appropriate, replace/mute/trim the claimed segment using available Studio tools; do not dispute unless you have a valid basis.", "Giving credit or writing 'no copyright intended' does not by itself grant permission."]
    elif problem == "Limited ads / monetization concern":
        advice = ["Review the exact notice in YouTube Studio and the current monetization policies.", "Check for reused content, third-party assets, graphic content, or metadata that may be relevant to the notice.", "The app cannot determine eligibility or overturn a decision; use the official appeal/review flow if available."]
    elif problem == "Video stuck processing or not visible":
        advice = ["Check YouTube Studio for processing status, restrictions, visibility, and any error message.", "Verify the exported file plays locally and is in a supported format such as MP4/H.264.", "If processing remains stuck, consult YouTube Help for the current status and error-specific steps."]
    elif problem == "Not gaining subscribers":
        advice = ["Build a repeatable series so viewers know what to expect next.", "Make the channel's topic and value clear; invite a subscription naturally after delivering value.", "Review which videos bring returning viewers and create related follow-ups."]
    else:
        advice = ["Open YouTube Studio and identify the first measurable symptom: impressions, CTR, retention, restrictions, or returning viewers.", "Change one variable at a time and write down what you changed and when.", "Use the official help links below for account-specific notices."]
    for item in advice: st.markdown(f"- {item}")
    st.link_button("Open YouTube Studio", "https://studio.youtube.com/")
    st.link_button("YouTube Help: copyright and music", "https://support.google.com/youtube/topic/2676339")
    st.link_button("YouTube monetization policies", "https://support.google.com/youtube/answer/1311392")

with tabs[5]:
    st.subheader("Simple upload planner")
    planned_date = st.date_input("Planned upload date", value=date.today())
    planned_time = st.selectbox("Preferred time (your local time)", ["Morning", "Afternoon", "Evening", "No preference"])
    cadence = st.selectbox("Realistic posting cadence", ["One video a week", "Two videos a week", "Three Shorts a week", "One Short + one long video a week", "Flexible / when ready"])
    st.write(f"**Plan:** {cadence}; target date **{planned_date.strftime('%d %b %Y')}**; preferred time **{planned_time}**.")
    st.write("Use your YouTube Studio audience data when available. There is no universal best upload time, and a consistent sustainable schedule is more useful than burning out.")
    for i, item in enumerate(["Recording captured and backed up", "Edit and export reviewed", "Title and thumbnail accurately match the video", "Description, chapters, and relevant tags prepared", "Music permissions/attribution checked", "Visibility, audience setting, and restrictions checked after upload"]):
        st.checkbox(item, key=f"upload_{i}")

with tabs[6]:
    st.subheader("Research this game when details matter")
    st.write("Your plan above is available immediately. This research section opens search pages so you can check current, game-specific details; this starter app does not automatically fetch or verify those pages for you.")
    query = st.text_input("Research question", value=f"{game} PS5 gameplay ideas tips latest updates")
    st.link_button("Search the web for this game", "https://www.google.com/search?q=" + quote_plus(query))
    st.link_button("Search YouTube for videos about this game", "https://www.youtube.com/results?search_query=" + quote_plus(game + " PS5 gameplay"))
    st.link_button("Search official game / publisher information", "https://www.google.com/search?q=" + quote_plus(game + " official website news"))
    st.markdown("**Research checklist**")
    for i, item in enumerate(["Check publication date and platform/version before using a tip.", "Prefer official publisher/game sources for release dates and patch notes.", "Confirm a claim in more than one reliable source when it matters.", "Do not copy another creator's script, thumbnail, or footage; use research to inform your own original video."]):
        st.checkbox(item, key=f"research_{i}")

st.divider()
st.caption("PS5 YouTube Coach • Free planning assistant • No account sign-in, automatic channel audit, automatic upload/scheduling, live AI image analysis, or guaranteed growth in this version.")
