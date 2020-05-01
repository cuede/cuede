const checkboxId = "editor-disable-checkbox";

function toggleHideEditor() {
    $('#editor-container').collapse("toggle")
}

function toggleDisabledEditorOnCheckboxClick() {
    const checkbox = document.getElementById(checkboxId);
    checkbox.onclick = toggleHideEditor;
}

document.addEventListener("DOMContentLoaded", toggleDisabledEditorOnCheckboxClick, false);

form.onsubmit = function () {
    const checkbox = document.getElementById(checkboxId);
    if (!checkbox.checked) {
        textElement.innerHTML = quill.getText();
    }
}
