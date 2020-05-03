const checkboxId = "editor-disable-checkbox";

function toggleHideEditor(checkbox, editor) {
    if (checkbox.checked) {
        editor.collapse("hide");
    } else {
        editor.collapse("show");
    }
}

function toggleDisabledEditorOnCheckboxClick() {
    const checkbox = document.getElementById(checkboxId);
    const editorContainer = $('#editor-container');
    const updateEditorVisibility = () => {toggleHideEditor(checkbox, editorContainer)};
    checkbox.onclick = updateEditorVisibility;
    editorContainer.on('hidden.bs.collapse', updateEditorVisibility);
    editorContainer.on('shown.bs.collapse', updateEditorVisibility);
}

document.addEventListener("DOMContentLoaded", toggleDisabledEditorOnCheckboxClick, false);

form.onsubmit = function () {
    const checkbox = document.getElementById(checkboxId);
    if (!checkbox.checked) {
        return putEditorTextInHiddenTextArea();
    }
}
