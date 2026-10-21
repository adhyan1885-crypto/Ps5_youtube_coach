import streamlit as st
from datetime import datetime
import re

st.set_page_config(page_title="PS5 YouTube AI Coach", page_icon="🎮", layout="centered")

st.title("🎮 PS5 YouTube Coach")
st.caption("A mobile-friendly creator helper for gaming ideas, editing, thumbnails, publishing schedules, and channel troubleshooting.")

st.warning(
    "Free starter edition: this app uses rules and templates, not a live AI model. "
    "It does not sign into YouTube, inspect your channel automatically, guarantee views, "
    "or change monetization decisions. It gives you a practical checklist based on your answers."
)

GAMES = {
    "Ghost of Tsushima": {
        "ideas": ["Cinematic samurai montage", "Perfect parry and duel highlights", "Beautiful locations mini-film", "Stealth takedown compilation", "A one-minute challenge with a clear goal"],
        "editing": "Use slower cuts for scenery and faster cuts for duels. Match cuts to sword impacts; avoid overusing shake effects. Use restrained color grading.",
        "thumb": [
            ("The perfect parry", "Freeze-frame the sword clash; Jin on one side, enemy on the other; bright focal glow at the contact point; 2–4 words: “PERFECT PARRY”."),
            ("Cinematic Japan", "Use one striking landscape or silhouette; keep the character large enough to read on mobile; minimal text: “SAMURAI CINEMA”."),
            ("Duel challenge", "Show both fighters facing each other with clear contrast; use a simple question: “CAN I WIN?”")
        ]
    },
    "Marvel's Spider-Man 2": {
        "ideas": ["Cinematic combat montage", "Boss fight highlights", "Photo-mode locations", "Funny fails", "Suit showcase with matching music"],
        "editing": "Use short clips, speed ramps only on action beats, and cinematic grading. Keep combat readable.",
        "thumb": [
            ("Suit reveal", "Large character pose with a clean city background; use a close crop and short text: “BEST SUIT?”."),
            ("Boss moment", "Show the clearest action frame and one opposing threat; avoid clutter; text: “FINAL FIGHT”."),
            ("Insane movement", "Use a dramatic swing frame with visible city depth; text: “SO FAST”.")
        ]
    },
    "GTA V": {
        "ideas": ["Funny moments and fails", "Cinematic driving montage", "Challenge video", "Best police chase moments", "Story clip with a twist"],
        "editing": "For comedy, use quick cuts, punch-ins, and readable captions. For cinematic driving, use longer shots and music-synced transitions.",
        "thumb": [
            ("Police chase", "Show the car and police clearly; choose a frame with motion and a clear focal point; text: “NO ESCAPE”."),
            ("Unexpected fail", "Freeze the funniest instant; add one expressive crop or arrow only if it helps; text: “WHAT?!”."),
            ("Driving cinema", "Use a clean car shot with city lights; little or no text.")
        ]
    },
    "Fortnite": {
        "ideas": ["Best eliminations in a 20–40 second Short", "Clutch / comeback moment", "Funny squad moments", "Unusual loadout challenge", "Skill progression"],
        "editing": "Start with the payoff or a strong question. Keep eliminations visible, captions large, and cuts tight.",
        "thumb": [
            ("Clutch win", "Show the key fight or victory screen; make the player and threat large; text: “1 HP CLUTCH”."),
            ("Funny squad", "Use a clear funny frame with two focal subjects; short text: “WE SOLD”."),
            ("Loadout challenge", "Show the unusual item and the outcome; text: “ONLY THIS?”.")
        ]
    },
    "Call of Duty": {
        "ideas": ["Best kills / clean streak", "One-life clutch", "Funny squad moment", "Weapon build test", "Objective-play highlight"],
        "editing": "Cut on action and reloads, keep the HUD visible when useful, and use restrained impact sounds. Make the hook clear in the first 1–2 seconds.",
        "thumb": [
            ("Clean streak", "Use a sharp frame showing the weapon and target area; simple contrast; text: “CLEAN STREAK”."),
            ("One-life clutch", "Show the low-health or last-player context if visible; text: “1 VS 4”."),
            ("Weapon test", "Show the weapon prominently and use a short truthful label: “WORTH IT?”.")
        ]
    },
    "EA SPORTS FC": {
        "ideas": ["Last-minute winner", "Best goals montage", "Funny goalkeeper moments", "Squad/build challenge", "One-player highlights"],
        "editing": "Show the setup and goal, then replay only if it adds value. Use scoreline/context overlays without covering the ball.",
        "thumb": [
            ("Last-minute goal", "Show the player celebrating or the ball crossing the line; text: “90+ MIN!”."),
            ("Best goal", "Choose the clearest shot frame and keep the goal visible; text: “TOP CORNER”."),
            ("Squad challenge", "Show the key player/card and a clear outcome; text: “CAN IT WORK?”.")
        ]
    },
    "Minecraft": {
        "ideas": ["One build from start to reveal", "Survival challenge", "Unexpected moment", "Before-and-after transformation", "A useful tip demonstrated quickly"],
        "editing": "Use a clear before/after, speed up repetitive building, and add simple labels. Show the result early.",
        "thumb": [
            ("Build reveal", "Split the thumbnail between the empty area and finished build; text: “BEFORE → AFTER”."),
            ("Survival challenge", "Show the danger and your character; one clear question: “CAN I SURVIVE?”."),
            ("Secret tip", "Zoom in on the actual mechanic or result; text: “DID YOU KNOW?”.")
        ]
    },
    "Other / custom game": {
        "ideas": ["Best 3 moments from one session", "Beginner tip or hidden mechanic", "Challenge with a clear win condition", "Funny fail", "Cinematic highlight"],
        "editing": "Pick one clear idea per video. Open with the most interesting moment, remove dead time, and make the ending intentional.",
        "thumb": [
            ("Big moment", "Use the clearest action frame; make the main subject large; use 2–4 truthful words."),
            ("Challenge", "Show the goal and obstacle in one frame; phrase it as a simple question."),
            ("Before and after", "Show a clear visual change; keep the two halves uncluttered.")
        ]
    }
}

TOOLS = {
    "CapCut": "Use split/trim, keyframes, beat markers, and restrained effects. Check the current version for watermark/export limits.",
    "VN Video Editor": "Use precise trimming, keyframes, music markers, and manual text. Keep transitions simple.",
    "InShot": "Use clean trimming, crop/resize, text overlays, and music timing. Avoid stacking filters.",
    "DaVinci Resolve": "Use the Cut page for pacing, Fairlight for audio balance, and color tools lightly. A 9:16 timeline suits Shorts.",
    "ShareFactory Studio (PS5)": "Trim and arrange highlights directly on PS5; put the strongest moment first, use simple transitions, and balance game audio with music.",
    "Other / not decided": "Prioritize trimming dead time, a strong first 1–2 seconds, readable captions, balanced audio, and a clear ending."
}

with st.sidebar:
    st.header("Your setup")
    game = st.selectbox("PS5 game", list(GAMES.keys()))
    custom_game = st.text_input("Custom game name (optional)")
    editor = st.selectbox("Editing tool", list(TOOLS.keys()))
    format_type = st.radio("Video format", ["Short (vertical)", "Long-form (horizontal)"])
    audience = st.selectbox("Main audience", ["India", "United States", "United Kingdom", "Worldwide / unsure"])

actual_game = custom_game.strip() if game == "Other / custom game" and custom_game.strip() else game
g = GAMES[game]

tabs = st.tabs(["Video Planner", "Thumbnail Ideas", "Upload Schedule", "Fix Channel Problems"])

with tabs[0]:
    st.subheader("Video ideas")
    for i, idea in enumerate(g["ideas"], 1):
        st.write(f"**{i}. {idea}**")
    st.subheader("Editing advice")
    st.write(f"**For {editor}:** {TOOLS[editor]}")
    st.write(g["editing"])
    if format_type.startswith("Short"):
        st.markdown("**Suggested structure:** 0–2s hook → quick setup → strongest moment → satisfying ending or loop.")
        st.markdown("**Export target:** vertical 9:16, typically 1080 × 1920 if supported.")
    else:
        st.markdown("**Suggested structure:** strongest teaser → short context → main sections → concise ending. Remove loading screens and repeated downtime.")
        st.markdown("**Export target:** horizontal 16:9, typically 1920 × 1080 if supported.")
    st.subheader("Title, description and tags")
    vibe = st.selectbox("Video style", ["Cinematic", "Funny", "Skill / competitive", "Helpful tip", "Story / challenge"])
    clip = st.text_input("Describe the actual moment (optional)", placeholder="e.g. a perfect parry followed by a duel win")
    subject = clip.strip() or g["ideas"][0]
    title_map = {
        "Cinematic": [f"{actual_game}: A Cinematic Moment", f"This {actual_game} Moment Looks Unreal", f"{actual_game} — Cinematic Gameplay"],
        "Funny": [f"The Most Unexpected {actual_game} Moment", f"{actual_game} Had Me Laughing", f"I Did NOT Expect This in {actual_game}"],
        "Skill / competitive": [f"That Timing Was PERFECT | {actual_game}", f"{actual_game}: One Perfect Play", f"Cleanest {actual_game} Moment So Far"],
        "Helpful tip": [f"Try This in {actual_game}", f"{actual_game}: Quick Tip", f"One {actual_game} Tip to Try"],
        "Story / challenge": [f"I Tried This Challenge in {actual_game}", f"Can I Pull This Off in {actual_game}?", f"{actual_game}: One Goal, One Attempt"]
    }
    titles = title_map[vibe]
    if format_type.startswith("Short"):
        titles = [t + " #Shorts" for t in titles]
    st.markdown("**Title options**")
    for t in titles:
        st.code(t)
    description = f"{subject}\n\nGameplay from {actual_game}, edited in {editor}.\n\nIf you enjoyed it, like the video and subscribe for more gaming content."
    st.markdown("**Description draft**")
    st.code(description)
    tags = list(dict.fromkeys([actual_game.lower(), f"{actual_game.lower()} gameplay", "ps5 gameplay", "playstation 5", "gaming", "game highlights", "gaming clips", editor.lower()]))
    st.markdown("**Suggested tags**")
    st.code(", ".join(tags))
    st.caption("Use only titles and claims that accurately describe the video. Tags alone rarely rescue a weak topic or thumbnail.")

with tabs[1]:
    st.subheader(f"Thumbnail concepts for {actual_game}")
    st.write("Choose a frame from your own gameplay. These are design concepts, not guarantees of clicks.")
    for title, idea in g["thumb"]:
        with st.expander(title):
            st.write(idea)
            st.write("**Layout rules:** one focal subject, strong contrast, uncluttered background, large readable subject, and 0–4 words at most.")
    st.markdown("**General thumbnail checklist**")
    for item in [
        "Can someone understand the idea at phone size?",
        "Does the image show the actual video moment?",
        "Is there one obvious focal point?",
        "Does the text add information rather than repeat the title?",
        "Have I avoided fake reactions, misleading arrows, or promises the video does not deliver?"
    ]:
        st.checkbox(item, key="thumb_" + re.sub(r"[^a-z0-9]+", "_", item.lower()))
    st.info("For Shorts, a custom thumbnail may not be available in the same way as for long-form videos on every device/workflow. Check YouTube's current Shorts thumbnail options.")

with tabs[2]:
    st.subheader("Recommended upload schedule")
    st.write("This is a starting experiment, not a magic time. Your own YouTube Studio audience data is more useful once you have enough viewers.")
    st.markdown("**Starting test for an India-focused audience (IST):**")
    st.write("- Try 6:00–9:00 PM IST for 3 comparable uploads.")
    st.write("- Test 12:00–2:00 PM IST for another 3 comparable uploads.")
    st.write("- Compare impressions, click-through rate (long-form), viewed-vs-swiped-away (Shorts), average view duration, and views after 24 hours and 7 days.")
    st.write("**Suggested cadence:** choose a pace you can sustain, such as 2–3 quality uploads a week, rather than posting daily if quality drops.")
    st.markdown("**Schedule publishing:** You can prepare a video in YouTube Studio and use its scheduling option to publish at a chosen date/time. This app does not upload or schedule videos directly.")
    st.markdown("**If you want fully automatic upload later:** it needs YouTube authorization and API integration. Free API quota may be sufficient for light use, but quota and policy limits apply.")
    st.caption("Use the Audience tab in YouTube Studio to refine the time when enough audience data becomes available.")

with tabs[3]:
    st.subheader("Troubleshoot a YouTube problem")
    problem = st.selectbox("What is happening?", [
        "Almost zero views",
        "Views stopped / low views",
        "Good video but low click-through",
        "People click but leave quickly",
        "Yellow dollar / limited ads",
        "Copyright claim or blocked video",
        "Video not appearing / processing issue"
    ])
    is_short = st.radio("Video type", ["Short", "Long-form"], horizontal=True)
    age = st.selectbox("How long since publishing?", ["Less than 2 hours", "2–24 hours", "1–3 days", "4–7 days", "More than 7 days"])
    public = st.radio("Visibility", ["Public", "Unlisted", "Private", "Not sure"], horizontal=True)
    impressions = st.selectbox("Impressions status (if visible in Studio)", ["I don't know", "Almost none", "Some impressions", "Many impressions"])
    ctr = st.selectbox("Click-through rate (long-form only, if available)", ["Not available / Shorts", "Low compared with my usual videos", "About usual", "Higher than usual"])
    retention = st.selectbox("Audience retention / viewed-vs-swiped (if available)", ["Not available yet", "People leave early / swipe away", "About usual", "Better than usual"])
    restrictions = st.selectbox("Restrictions shown in YouTube Studio", ["None / not sure", "Yellow icon / limited ads", "Copyright claim", "Age restriction or other restriction"])
    submitted = st.button("Show troubleshooting steps", type="primary")
    if submitted:
        st.markdown("### Your action plan")
        if public != "Public":
            st.error("First check visibility. Private and unlisted videos generally won't be discovered like public videos. Confirm the video is Public if you want normal discovery.")
        if problem == "Almost zero views":
            st.write("1. Confirm the video is Public and fully processed; check YouTube Studio for restrictions or errors.")
            st.write("2. Check Reach/Content analytics: if impressions are near zero, wait a little and verify topic, audience, visibility, and restrictions. New videos can take time to receive distribution.")
            st.write("3. For Shorts, check whether it appears in the Shorts feed and review viewed-vs-swiped-away. For long-form, inspect impressions and click-through rate.")
            st.write("4. Share with a relevant audience without spam. Do not repeatedly delete and re-upload the same video just to force views.")
        elif problem == "Views stopped / low views":
            st.write("1. Compare the video with your own recent uploads, not a universal benchmark.")
            st.write("2. Check traffic sources, impressions, retention, and whether the topic has a clear audience.")
            st.write("3. Make the next upload more specific: one game, one promise, one clear payoff. Avoid misleading titles.")
        elif problem == "Good video but low click-through":
            st.write("1. For long-form, test a clearer title and a simpler thumbnail with one focal point.")
            st.write("2. Make the thumbnail promise match the opening and actual content.")
            st.write("3. Do not change many things at once; compare results over enough impressions.")
            if is_short == "Short":
                st.write("For Shorts, focus more on the opening frame and viewed-vs-swiped-away; the standard long-form thumbnail/CTR workflow may not apply the same way.")
        elif problem == "People click but leave quickly":
            st.write("1. Put the promised moment near the start; remove long logos, intros, and setup.")
            st.write("2. Make the first 1–3 seconds understandable without explanation.")
            st.write("3. Check the retention graph for the exact drop-off, then shorten or restructure the next edit.")
        elif problem == "Yellow dollar / limited ads":
            st.write("1. Open YouTube Studio → Content → select the video → Monetization / Restrictions and read the exact reason.")
            st.write("2. Review YouTube's advertiser-friendly content guidelines and the video's title, thumbnail, description, spoken words, and visuals.")
            st.write("3. If available and you believe the decision is wrong, request a human review through Studio. Do not repeatedly re-upload to evade the decision.")
            st.write("4. Removing a word or changing a thumbnail does not guarantee the yellow icon will change. This app cannot overturn monetization decisions.")
        elif problem == "Copyright claim or blocked video":
            st.write("1. Read the exact claim and identify the matched segment in Studio.")
            st.write("2. If you have rights, follow YouTube's dispute process with accurate evidence. Otherwise consider trimming, muting, or replacing the claimed material using Studio tools where available.")
            st.write("3. Do not dispute unless you have a valid basis; a claim is not automatically a copyright strike.")
        else:
            st.write("1. Confirm processing has finished and the video is Public.")
            st.write("2. Check Studio for upload errors, restrictions, or copyright notices.")
            st.write("3. If the issue persists, use YouTube Help and provide the exact error message.")
        if impressions == "Almost none":
            st.info("Low impressions means YouTube has shown the video to very few people so far; it does not by itself prove the video is bad. Check visibility/restrictions and allow time for data.")
        elif impressions == "Many impressions" and ctr == "Low compared with my usual videos":
            st.info("Many impressions with below-usual CTR suggests the title/thumbnail/topic packaging is worth reviewing.")
        if retention == "People leave early / swipe away":
            st.info("The opening may not deliver the promised payoff quickly enough. Start with the most compelling real moment.")
        if restrictions == "Yellow icon / limited ads" or problem == "Yellow dollar / limited ads":
            st.warning("Use the exact reason and official review process in YouTube Studio. No third-party app can guarantee monetization approval.")
        st.caption("These steps are diagnostic guidance. The app cannot access your channel or fix settings automatically without an authorized integration.")

with st.expander("Free tools and limitations"):
    st.markdown("""
    - No paid API key is required for this starter.
    - It does not connect to your YouTube account or fetch live analytics.
    - It cannot guarantee views, fix recommendations, or reverse yellow-dollar decisions.
    - A live AI model and automatic uploading would require additional integration and authorized access; zero-cost availability depends on the provider's current limits.
    - Keep API secrets out of source code and use the host's secrets settings if you add integrations later.
    """)
