BASIC_LAYOUT_CSS = """
.post {
  display: flex;
  flex-direction: column;
  max-width: 540px;
}

.layout-row {
  display: flex;
  flex-direction: row;
  gap: 4px;
  margin: 5px;
}

.layout-row > * {
  margin: 0;
}

img {
  max-width: 100%;
}

"""