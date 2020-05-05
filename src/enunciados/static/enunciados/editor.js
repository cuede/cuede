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

document.addEventListener("DOMContentLoaded", setTabsClickListeners);

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
    const spinner = document.getElementById('spinner-vista-previa');
    contenido.innerHTML = "";
    spinner.hidden = false;
    $.get({
        url: "/ajax/format_post/",
        data: {
            'texto': quill.getText()
        },
        success: (data) => {
            spinner.hidden = true;
            updatePreviewContent(contenido, data);
        }
    });
}

function updatePreviewContent(elementContenido, data) {
    elementContenido.innerHTML = data;
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, elementContenido]);
}


