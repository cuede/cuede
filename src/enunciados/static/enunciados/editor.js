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

// Si ponemos primero mathjax, cuando hay $$ adentro de ``` ``` se muestra el código html de mathjax.
// Si ponemos primero marked, los \( por ejemplo se reemplazan por (, y esos son marcadores
// alternativos de mathmode de latex. Podríamos dejar de soportarlos, pero habría que entonces
// cambiar todos los \( ... \) y \[ ... \] presentes en posts por $ ... $ y $$ ... $$.

// Usar marked implica cosas del markdown de github que quiza no queremos, o sea:
// - Links
// - hr (-------- por ejemplo)

function updatePreview() {
    const contenido = document.getElementById('contenido-vista-previa');
    $(contenido).text(quill.getText());
    formatMarkdown(contenido);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, contenido]);
}

function formatMarkdown(element) {
    element.innerHTML = marked(element.innerHTML);
}
