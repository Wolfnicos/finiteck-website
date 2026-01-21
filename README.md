# Finiteck Website

Official website for Finiteck, the personal money-saving assistant for iOS.

**Live site:** [finiteck.com](https://finiteck.com)

---

## Purpose

This website serves three functions:

1. **Marketing landing page** - Explains what Finiteck does and drives App Store downloads
2. **Privacy Policy** - Required for App Store submission (Apple requires a valid URL)
3. **Terms of Service** - Required for subscription-based apps

---

## Hosting

This site is hosted via **GitHub Pages** with a custom domain.

- Repository: `finiteck-website`
- Branch: `main`
- Custom domain: `finiteck.com`
- HTTPS: Enabled automatically by GitHub

---

## File Structure

```
finiteck-website/
├── index.html          # Landing page
├── privacy.html        # Privacy Policy (App Store requirement)
├── terms.html          # Terms of Service
├── css/
│   └── style.css       # All styles
├── images/
│   ├── app-icon.png    # App icon (512x512 recommended)
│   ├── screenshot-1.png # App screenshot (optional)
│   └── app-store-badge.svg
├── CNAME               # Custom domain configuration
├── README.md           # This file
└── .gitignore
```

---

## How to Update Content

### Edit text content

1. Open the relevant HTML file (`index.html`, `privacy.html`, or `terms.html`)
2. Edit the text directly
3. Commit and push to `main`
4. Changes go live automatically within minutes

### Update styles

1. Edit `css/style.css`
2. Commit and push
3. Hard refresh the browser to see changes (Cmd+Shift+R)

### Replace images

1. Add new images to the `images/` folder
2. Update the `src` attribute in HTML if filenames changed
3. Commit and push

---

## Custom Domain Setup

The `CNAME` file contains `finiteck.com`.

To complete domain setup:

1. In your domain registrar (where you bought finiteck.com), add these DNS records:

   **For apex domain (finiteck.com):**
   ```
   Type: A
   Name: @
   Value: 185.199.108.153

   Type: A
   Name: @
   Value: 185.199.109.153

   Type: A
   Name: @
   Value: 185.199.110.153

   Type: A
   Name: @
   Value: 185.199.111.153
   ```

   **For www subdomain (optional):**
   ```
   Type: CNAME
   Name: www
   Value: wolfnicos.github.io
   ```

2. In GitHub repository settings:
   - Go to Settings → Pages
   - Custom domain: `finiteck.com`
   - Check "Enforce HTTPS"

3. Wait for DNS propagation (up to 24 hours, usually faster)

---

## App Store Compliance

This website fulfills Apple's App Store requirements:

| Requirement | Page |
|-------------|------|
| Privacy Policy URL | `https://finiteck.com/privacy.html` |
| Terms of Service URL | `https://finiteck.com/terms.html` |
| Support URL | `https://finiteck.com` (or mailto link) |

When submitting to the App Store, use these exact URLs.

---

## No Tracking

This website intentionally contains:

- No analytics scripts
- No cookies
- No third-party requests (except App Store badge)
- No cookie consent banners needed

This matches the app's privacy-first positioning.

---

## Tech Stack

- Pure HTML5
- Pure CSS3
- No JavaScript frameworks
- No build tools required
- Responsive design (mobile-first)

---

## Local Development

To preview locally:

```bash
# Option 1: Python
python -m http.server 8000

# Option 2: PHP
php -S localhost:8000

# Option 3: Just open in browser
open index.html
```

---

## License

All rights reserved. This website and its content are proprietary to Finiteck.
