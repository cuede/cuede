from django.shortcuts import redirect, get_object_or_404
from django.views.generic.list import ListView


class VersionesView(ListView):
    context_object_name = 'versiones'

    def _volver_a_version(self, objeto, pk):
        version = get_object_or_404(objeto.versiones, pk=pk)
        if objeto.versiones.ultima().texto != version.texto:
            version.pk = None
            version.save()

    def get_object(self):
        """
        Devuelve el objeto para el cual se quieren ver
        las versiones, o levanta un 404 si no se encuentra.

        Debería tener un atributo versiones que tenga las versiones.
        """
        pass

    def get_success_url(self):
        """
        Devuelve la URL a la que redireccionar luego de
        volver efectivamente a una versión anterior.
        """
        pass

    def get_queryset(self):
        objeto = self.get_object()
        return objeto.versiones.all()

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('version_pk')
        if pk:
            self._volver_a_version(self.get_object(), pk)
            return redirect(self.get_success_url())
        else:
            return self.get(request)
