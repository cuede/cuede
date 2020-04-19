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
form.onsubmit = function () {
    textElement.innerHTML = quill.getText();
}
