# PS5 YouTube Coach — free starter v2

## What it does
- Game-specific video ideas and editing tips
- Title, description, and tag templates
- Thumbnail concepts and thumbnail checklist
- Upload-time experiments and YouTube Studio scheduling guidance
- Troubleshooting checklists for low/zero views, low click-through, retention, yellow-dollar/limited ads, copyright claims, and processing/visibility issues

## What it does not do
- It is not a full generative AI model.
- It does not sign into or inspect your YouTube account.
- It does not upload or schedule videos directly.
- It cannot guarantee views or overturn a monetization decision.

## Deploy using a phone
1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, and `README.md`.
3. Use Streamlit Community Cloud if your account is eligible for its free tier.
4. Select the repository and `app.py` and deploy.
5. Open the app URL in your Android browser; use the browser menu to add it to your home screen if that option is available.

Hosting providers can change their free-tier limits and availability. This app code itself does not call paid APIs.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
