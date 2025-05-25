<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Shared Notepad</title>
  <style>
    body {
      margin: 0;
      padding: 20px;
      background: #fff;
      font-family: 'Segoe UI', sans-serif;
    }
    textarea {
      width: 100%;
      height: 90vh;
      border: none;
      outline: none;
      resize: none;
      font-size: 18px;
      line-height: 28px;
      background-image: linear-gradient(#eee 1px, transparent 1px);
      background-size: 100% 28px;
      padding: 10px;
    }
    .toolbar {
      display: flex;
      gap: 10px;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }
    button, select {
      padding: 8px 12px;
      border: none;
      background: #333;
      color: #fff;
      cursor: pointer;
      border-radius: 4px;
    }
    button:hover, select:hover {
      background: #555;
    }
  </style>
</head>
<body>

<div class="toolbar">
  <button onclick="saveNote()">Save</button>
  <button onclick="copyText()">Copy</button>
  <button onclick="deleteNote()">Delete</button>
  <select onchange="translateNote(this.value)">
    <option value="">Translate</option>
    <option value="en">English</option>
    <option value="bn">Bengali</option>
    <option value="hi">Hindi</option>
  </select>
</div>

<form method="POST" style="margin:0;">
  <textarea name="note" id="note"><?= htmlspecialchars(file_get_contents('note.txt')) ?></textarea>
</form>

<script>
  function saveNote() {
    document.forms[0].submit();
  }

  function copyText() {
    const txt = document.getElementById("note");
    txt.select();
    document.execCommand("copy");
    alert("Copied!");
  }

  function deleteNote() {
    if (confirm("Delete all note content?")) {
      document.getElementById("note").value = '';
      saveNote();
    }
  }

  async function translateNote(lang) {
    const text = document.getElementById("note").value;
    if (!text.trim() || !lang) return;

    const res = await fetch(`https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${lang}&dt=t&q=` + encodeURIComponent(text));
    const data = await res.json();
    const translated = data[0].map(x => x[0]).join('');
    document.getElementById("note").value = translated;
  }
</script>

<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['note'])) {
  file_put_contents('note.txt', $_POST['note']);
  header("Location: " . $_SERVER['PHP_SELF']);
  exit;
}
?>
</body>
</html>