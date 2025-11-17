Place font files (woff, woff2, ttf, otf) in the `fonts/` folder (next to this app). Then run the helper script to copy the fonts into `assets/fonts/` and generate a CSS file that Dash will load automatically.

Steps:

1. Put your downloaded font files into the `fonts/` folder located in the same directory as the app (e.g. `#5 Data Visualization/fonts/`).
2. From the `#5 Data Visualization` directory run:

   python move_fonts_to_assets.py

3. Restart the Dash server. The generated CSS will be at `assets/custom_fonts.css` and the fonts will be under `assets/fonts/`.

Notes:

- The script will only copy files with extensions: .woff, .woff2, .ttf, .otf
- The CSS uses the filename (cleaned) as the font-family. You can override names and define additional @font-face rules manually in `assets/custom_fonts.css` if needed.
