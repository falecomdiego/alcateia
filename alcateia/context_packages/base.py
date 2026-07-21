import abc
from typing import Dict, List, Any

class BaseContextPackage(abc.ABC):
    """
    Classe base abstrata para representar pacotes de contexto (Context Packages)
    na arquitetura ALCATEIA. Define as regras de conformidade, caminhos das fontes,
    tabelas taxonômicas e configurações específicas de cada domínio.
    """

    @property
    @abc.abstractmethod
    def package_id(self) -> str:
        """ID única identificadora do pacote de contexto."""
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Nome humanamente legível do domínio de contexto."""
        pass

    @property
    @abc.abstractmethod
    def version(self) -> str:
        """Versão do pacote de contexto."""
        pass

    @abc.abstractmethod
    def get_compliance_rules(self) -> Dict[str, Any]:
        """
        Retorna as regras de privacidade e conformidade (ex: expurgação de e-mails, 
        telefones, pseudonimização de perfis).
        """
        pass

    @abc.abstractmethod
    def get_sources_mapping(self) -> Dict[str, Dict[str, Any]]:
        """
        Retorna o mapa de fontes oficiais autorizadas do domínio, vinculando 
        fonte_id aos caminhos locais e metadados.
        """
        pass

    @abc.abstractmethod
    def get_taxonomy_definitions(self) -> Dict[str, List[str]]:
        """
        Retorna os eixos taxonômicos e as palavras-chave/nuances que
        orientam a classificação analítica probabilística de sentimento e temas.
        """
        pass

    @abc.abstractmethod
    def get_mock_reasoning_data(self) -> Dict[str, Dict[str, Any]]:
        """
        Retorna as respostas simuladas estruturadas de raciocínio de alta fidelidade
        associadas aos conteúdos das publicações para o modo demonstrativo (offline).
        """
        pass
