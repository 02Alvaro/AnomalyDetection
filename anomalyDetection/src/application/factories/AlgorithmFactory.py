from domain.exceptions.AlgorithmNotFound import AlgorithmDataNotFound
from domain.interfaces.AlgorithmConfigurator import AlgorithmConfigurator


class AlgorithmFactory:
    """
    Factory class for creating algorithm configurations.

    Attributes
    ----------
    algorithm_config : dict
        A dictionary mapping algorithm names to their configuration classes.
    """
    algorithm_config = {}

    @staticmethod
    def Configurator_for(name):
        """
        Decorator for registering an algorithm configuration class.

        Parameters
        ----------
        name : str
            The name of the algorithm.

        Returns
        -------
        function
            A decorator function that registers the class in the algorithm_config dictionary.
        """
        def decorator(cls):
            AlgorithmFactory.algorithm_config[name] = cls
            return cls

        return decorator

    @staticmethod
    def create(name, data_file, **kwargs):
        """
        Creates an instance of the specified algorithm configuration.

        Parameters
        ----------
        name : str
            The name of the algorithm.
        data_file : str
            The data file to be used for the algorithm.
        **kwargs : dict
            Additional keyword arguments to be passed to the algorithm configuration.

        Returns
        -------
        AlgorithmConfigurator
            An instance of the specified algorithm configuration.

        Raises
        ------
        AlgorithmDataNotFound
            If the specified algorithm configuration is not found.
        """
        data_class: AlgorithmConfigurator = AlgorithmFactory.algorithm_config.get(name)
        if not data_class:
            raise AlgorithmDataNotFound(name)

        return data_class(data_file=data_file, **kwargs)
