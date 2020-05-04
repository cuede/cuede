var quill = new Quill('#editor', {
    theme: 'snow',
    formats: ['code', 'formula'],
    modules: {
        toolbar: '#toolbar'
    },
});

function surroundSelectionBy(before, after) {
    var selection = quill.getSelection();
    if (selection) {
        quill.insertText(selection.index + selection.length, after)
        quill.insertText(selection.index, before);
        quill.setSelection(selection.index + before.length, selection.length)
    }
}

function toolbarCodeHandler() {
    surroundSelectionBy('```\n', '\n```\n');
}

function toolbarFormulaHandler() {
    surroundSelectionBy('\\[\n', '\n\\]\n');
}

var toolbar = quill.getModule('toolbar');
toolbar.addHandler('code', toolbarCodeHandler);
toolbar.addHandler('formula', toolbarFormulaHandler);

var textElement = document.getElementById('hidden_textarea');
var form = document.getElementById('form');

form.onsubmit = putEditorTextInHiddenTextArea;

function putEditorTextInHiddenTextArea() {
    const text = quill.getText();
    textElement.innerHTML = text;
    if (text.trim() === "") {
        const emptyTextError = document.getElementById("empty-text-error");
        emptyTextError.hidden = false;
        return false;
    }
}

function updatePreview() {
    $.get({
        url: "/ajax/format_post/",
        data: {
            'texto': quill.getText()
        },
        success: function (data) {
            const idVistaPrevia = 'vista-previa';
            document.getElementById(idVistaPrevia).innerHTML = data;
            MathJax.Hub.Queue(["Typeset", MathJax.Hub, idVistaPrevia]);
        }
    });
}

function setPreviewTabClickListener() {
    const tab = document.getElementById("tab-vista-previa");
    tab.onclick = updatePreview;
}

document.addEventListener("DOMContentLoaded", setPreviewTabClickListener);
