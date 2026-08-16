# Build the site
docs:
    hugo

# Serve the site locally with live reload
docs-serve:
    hugo server -D

# Copy the latest resume PDF from the resume_2026 repo into static/
sync:
    python3 scripts/sync_resume.py

# Re-render the social share card from scripts/og-card.html (macOS Chrome)
og-card:
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
      --hide-scrollbars --force-device-scale-factor=1 --window-size=1200,630 \
      --screenshot=static/img/og-card.png "file://$(pwd)/scripts/og-card.html"
