from DependencyContainer import DependencyContainer


def Inject(cls):
    """
    Decorator for injecting dependencies into the class constructor.

    Parameters
    ----------
    cls : class
        The class whose dependencies need to be injected.

    Returns
    -------
    class
        The class with dependencies injected into the constructor.
    """
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        """
        Modified __init__ method to inject dependencies.

        Parameters
        ----------
        self : object
            The instance of the class.
        *args : tuple
            Positional arguments for the original __init__ method.
        **kwargs : dict
            Keyword arguments for the original __init__ method.
        """
        annotations = getattr(original_init, "__annotations__", {})
        args_names = original_init.__code__.co_varnames[
            1 : original_init.__code__.co_argcount
        ]
        # Crear un diccionario con los nombres de los argumentos y sus valores
        args_dict = dict(zip(args_names, args))
        args_dict.update(kwargs)  # Actualizar con los argumentos de palabra clave proporcionados
        # Identificar los argumentos que son dependencias
        dependency_args = {
            name: annotation
            for name, annotation in annotations.items()
            if isinstance(annotation, type)
        }
        # Rellenar las dependencias faltantes
        for name, annotation in dependency_args.items():
            if args_dict.get(name) is None:
                service = DependencyContainer.get_service(annotation)
                if service:
                    args_dict[name] = service
        # Reconstruir args y kwargs
        new_args = [args_dict[name] for name in args_names]
        original_init(self, *new_args)

    cls.__init__ = new_init
    return cls
