from django.urls import reverse


class BreadcrumbPage:
    def __init__(self, title, url=None):
        self.title = title
        self.url = url


def breadcrumb_materia(materia_carrera):
    return [
        BreadcrumbPage(
            materia_carrera.carrera,
            reverse('materias', kwargs={
                'carrera': materia_carrera.carrera})
        ),
        BreadcrumbPage(materia_carrera, materia_carrera.get_absolute_url()),
    ]


def breadcrumb_conjunto_de_enunciados(materia_carrera, conjunto):
    return breadcrumb_materia(materia_carrera) + [
        BreadcrumbPage(conjunto)
    ]
