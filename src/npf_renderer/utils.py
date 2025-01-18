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

@media (min-width: 540px) {
  .post-body {
    width: 540px;
  }
}

.post-body > * {
  margin: 8px;
}

.layout-row {
  display: flex;
  flex-direction: row;
  gap: 4px;
  margin: 5px;
}

/* Image blocks and images*/

.image-block {
  width: 100%;
}

.post-body .image-block {
  margin: 0;
}

.image-container {
    position: relative;
}

.image-container img, .link-block img {
  display: block;

  height: 100%;
  width: 100%;
  max-width: 100%;
  object-fit: cover;
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

.heading1, .heading2 {
  margin: 0;
}

.quote {
  font-family: serif;
  font-size: 26px;
  margin-left: 0;
  margin-top: 0;
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

  width: 100%;
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

  color: #f1f1f1;
  background: rgba(0,0,0,0.4);

  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
}

.link-block-title {
  margin: 20px 15px;
  font-size: 1.5em;
}

.link-block-description-container {
  padding: 0 10px 15px 10px;
}

.link-block-description-container:only-child {
  padding: 10px 15px;
}

.site-name-author-separator {
  margin: 0px 3px;
}

.audio-block, .audio-block > iframe {
  width: 100%;
}

/* Spotify embeds can sometimes generate with a large amount of excess white space */
.spotify_audio_player {
  max-height: 352px;
}

/* Audio blocks */
.ab-heading {
  display: flex;
  justify-content: space-between;
  padding-left: 10px;
}

.ab-metadata {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 96px;
}

.ab-metadata > * {
  margin: 0;
}

img.ab-poster {
  width: 96px;
  height: 96px;
}

.ap-container {
  border: 3px solid rgba(0, 0, 0, 0.07);
}

.ap-container > audio {
  display: block;
  width: 100%;
}


/* Video blocks */
.video-block iframe {
  width: 100%;
}

.video-block {
  position: relative;
  width: 100%;
}

.post-body video {
  max-width: 540px;
  height: 100%;
  width: 100%;
}

/* Poll blocks */

.poll-block {
  display: flex;
  flex-direction: column;
  border: 3px solid rgba(0, 0, 0, 0.07);
  padding: 10px;

  width: 100%;
  box-sizing: border-box;
}

.poll-block > header > h3 {
  margin: 0 0 10px 0;
}

.poll-choices {
  list-style: none;
  margin: 0;
  padding: 0;

  display: flex;
  flex-direction: column;
  gap: 10px;
}

.poll-block > footer {
  margin-top: 10px;
  text-align: center;
}

.poll-metadata {
  display: flex;
  gap: 5px;
  align-items: center;
  justify-content: center;
}

.poll-choice {
  display: flex;
  align-items: center;
  position: relative;
  padding: 5px 10px;
  border: 3px solid rgba(0, 0, 0, 0.15);
  text-wrap: balance;
}

.vote-proportion {
  position: absolute;
  top: 0;
  left: 0;
  display: block;
  background: #e9e9e9;
  height: 100%;
}

.poll-winner .vote-proportion {
  background: #d0d0d0;
}

.answer {
  margin: 0;
  flex: 1;
}

.answer, .vote-count {
  z-index: 1
}

.vote-count {
  margin-left: auto;
}

/* Ask */

.ask {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-bottom: 10px;
  padding: 5px;
  gap: 10px;
}

.ask-header {
  margin-bottom: 6px;
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
