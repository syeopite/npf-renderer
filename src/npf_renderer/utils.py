BASIC_LAYOUT_CSS = """
.post-body {
  display: flex;
  flex-direction: column;
  max-width: 540px;
  margin: 0;
  font-size: 16px;
  white-space: pre-wrap;
  word-break: break-word;
}

.post-body > * {
  margin: 8px;
}

.post-body .image-block {
  margin: 0;
}

.layout-row {
  display: flex;
  flex-direction: row;
  gap: 4px;
  margin: 5px;
}

.image-container, img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

img {
  max-width: 100%;
}

/* Text blocks */

.indented {
  margin: 10px;
  border-left: 3px solid rgba(0, 0, 0, 0.07);
  padding-left: 10px;
}

.heading1 {
font-size: 1.6em
}

.heading2 {
font-size: 1.3em
}

.quote {
  font-size: 26px;
}

.inline-small {
  font-size: 12px;
}

.text-block a {
  color: inherit;
}

/* Link Blocks */

.link-block {
  border: 1px;
  border-style: solid;
  border-color: rgba(0,0,0,0.4);
}

.poster-container {
  position: relative;
  display: flex;
  height: 240px;
  text-align: center;
}

.poster-overlay-text {
  display: flex;
  align-items: center;
  justify-content: center;

  position: absolute;
  width: 100%;
  height: 100%;

  background: rgba(0,0,0,0.4);
}

.link-block-title {
  margin: 20px 15px;
  font-size: 1.5em;
}

.poster-overlay-text {
  margin: 0;
  color: #f1f1f1;
}

.link-block-description-container {
  padding: 0 10px 15px 10px;
}

.site-name-author-separator {
  margin: 0px 3px;
}

/* Ask */

.ask {
  display: flex;
  flex-direction: row;
  margin-bottom: 10px;
  padding: 10px;
}

.ask-header {
  margin-bottom: 6px;
}

.ask-body {
  margin-right: 20px;
  width: 540px;
}

.ask-content * {
  margin-bottom: 10px;
}

.asker-avatar {
  width: 48px;
  height: 48px;
  border-radius: 2px;
}

/* Placeholders */
.unsupported-content-block {
  border: 3px solid rgba(0, 0, 0, 0.07);
  padding: 0em 1em;
}

.unsupported-content-block-message * {
  margin: 10px;
}

.unsupported-content-block h1 {
  font-size: 1.6em
}

"""
