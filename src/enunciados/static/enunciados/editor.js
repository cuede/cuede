const quill = new Quill('#editor', {
    theme: 'snow',
    formats: [],
    modules: {
        toolbar: '#toolbar'
    },
});

document.addEventListener('DOMContentLoaded', setupToolbarButtons);

function setupToolbarButtons() {
    const toolbarButtonHandlers = {
        'toolbar-formula': handleFormulaButton,
        'toolbar-code': handleCodeButton,
        'toolbar-header': handleHeaderButton,
        'toolbar-bold': handleBoldButton,
        'toolbar-italic': handleItalicButton,
        'toolbar-link': handleLinkButton,
    }

    for (const id in toolbarButtonHandlers) {
        document.getElementById(id).onclick = toolbarButtonHandlers[id];
    }
}

function handleFormulaButton() {
    surroundSelectionBy('$$\n', '\n$$\n');
}

function handleCodeButton() {
    surroundSelectionBy('```\n', '\n```\n');
}

function handleHeaderButton() {
    surroundSelectionBy('### ', '');
}

function handleBoldButton() {
    surroundSelectionBy('**', '**');
}

function handleItalicButton() {
    surroundSelectionBy('_', '_');
}

function handleLinkButton() {
    surroundSelectionBy('[', '](url)');
}

function surroundSelectionBy(before, after) {
    const selection = quill.getSelection();
    if (selection) {
        quill.insertText(selection.index + selection.length, after)
        quill.insertText(selection.index, before);
        quill.setSelection(selection.index + before.length, selection.length)
    }
}

const form = document.getElementById('form');
form.onsubmit = putEditorTextInHiddenTextArea;

function putEditorTextInHiddenTextArea() {
    const text = quill.getText();
    const textElement = document.getElementById('hidden_textarea');
    textElement.innerHTML = text;
    if (text.trim() === '') {
        const emptyTextError = document.getElementById('empty-text-error');
        emptyTextError.hidden = false;
        return false;
    }
}

document.addEventListener('DOMContentLoaded', setTabsClickListeners);

function setTabsClickListeners() {
    setEditorTabClickListener();
    setPreviewTabClickListener();
}

function setEditorTabClickListener() {
    $('#tab-escribir').on('shown.bs.tab click', function (e) {
        quill.focus();
    });
}

function setPreviewTabClickListener() {
    $('#tab-vista-previa').on('shown.bs.tab', updatePreview);
}

function updatePreview() {
    const contenido = document.getElementById('contenido-vista-previa');
    $(contenido).text(quill.getText());
    formatPost(contenido);
}
