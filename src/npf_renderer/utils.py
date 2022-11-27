BASIC_LAYOUT_CSS = """
.post-body {
  display: flex;
  flex-direction: column;
  max-width: 540px;
  margin: 0;
}

.post-body * {
  margin: 0
}

.layout-row {
  display: flex;
  flex-direction: row;
  gap: 4px;
  margin: 5px;
}

img {
  max-width: 100%;
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
}

.ask-content * {
  margin-bottom: 10px;
}

.asker-avatar {
  width: 48px;
  height: 48px;
}

"""
