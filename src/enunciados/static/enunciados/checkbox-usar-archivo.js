function toggleHideEditor() {
    $('#editor-container').collapse("toggle")
}

function toggleDisabledEditorOnCheckboxClick() {
    const checkbox = document.getElementById("editor-disable-checkbox");
    checkbox.onclick = toggleHideEditor;
}

document.addEventListener("DOMContentLoaded", toggleDisabledEditorOnCheckboxClick, false);
