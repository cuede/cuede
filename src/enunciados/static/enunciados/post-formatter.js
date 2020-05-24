document.addEventListener("DOMContentLoaded", formatAllPostsInPage);

function formatAllPostsInPage() {
    const postClass = "post";
    const posts = document.getElementsByClassName(postClass);
    Array.from(posts).forEach(formatPost);
}

function formatPost(element) {
    element.innerHTML = marked(element.innerHTML);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, element]);
}
