const quill = new Quill('#editor', {
    theme: 'snow',
    formats: ['code', 'formula'],
    modules: {
        toolbar: '#toolbar'
    },
});

const toolbar = quill.getModule('toolbar');
toolbar.addHandler('code', toolbarCodeHandler);
toolbar.addHandler('formula', toolbarFormulaHandler);

function toolbarCodeHandler() {
    surroundSelectionBy('```\n', '\n```\n');
}

function toolbarFormulaHandler() {
    surroundSelectionBy('\\[\n', '\n\\]\n');
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
    contenido.hidden = true;
    spinner.hidden = false;
    $.get({
        url: "/ajax/format_post/",
        data: {
            'texto': quill.getText()
        },
        success: (data) => {
            spinner.hidden = true;
            updatePreviewContent(contenido, data);
            contenido.hidden = false;
        }
    });
}

function updatePreviewContent(elementContenido, data) {
    elementContenido.innerHTML = data;
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, elementContenido]);
}


