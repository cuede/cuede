from django.shortcuts import render


def format_post(request):
    return render(request, 'enunciados/formatted_post.html', {
        'post': request.GET['texto'],
    })
