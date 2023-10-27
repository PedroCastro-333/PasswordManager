import pymongo


class DbController:
    def __init__(self, url: str, db_name: str, collection_name: str) -> None:
        """
        Inicializa um objeto DbController.

        Args:
            url (str): URL do servidor MongoDB.
            db_name (str): Nome do banco de dados.
            collection_name (str): Nome da coleção (tabela) no banco de dados.
        """
        self.__db_url = url
        self.__client = pymongo.MongoClient(url)
        self.__db = self.__client[db_name]
        self.__collection = self.__db[collection_name]

    # Propriedades / atributos
    @property
    def db_url(self):
        """Obtém a URL do servidor MongoDB."""
        return self.__db_url

    @db_url.setter
    def db_url(self, url):
        """Define a URL do servidor MongoDB."""
        if url:
            self.__db_url = url
            return "URL alterada com sucesso"
        else:
            return "URL inválida"

    # Métodos

    def salvar(self, document: dict) -> str:
        """
        Salva um documento na coleção.

        Args:
            document (dict): Documento a ser inserido na coleção.

        Returns:
            str: Uma mensagem indicando que a senha foi salva com sucesso.
        """
        self.__collection.insert_one(document)
        return "Senha salva com sucesso"

    def find(self, servico: str = None) -> tuple:
        """
        Consulta documentos na coleção com base no serviço.

        Args:
            servico (str): Serviço a ser usado como critério de consulta. Se None, retorna todos os documentos.

        Returns:
            list: Uma lista de documentos que correspondem ao critério de consulta.
        """
        if servico:
            # Consulta documentos com base no campo "serviço"
            result = self.__collection.find({"serviço": servico})
        else:
            # Se "servico" for None, retorna todos os documentos
            result = self.__collection.find()

        # Converte o resultado em uma lista de dicionários
        documents = [document for document in result]

        return documents

    def delete(self, servico: str, usuario: str) -> None:
        if servico and usuario:
            # Define o critério de pesquisa com base no serviço e usuário

            # Remove o documento que corresponde ao critério de pesquisa
            result = self.__collection.find_one_and_delete(
                {"serviço": servico, "usuário": usuario})

            if result:
                print("Senha deletada com sucesso.")
            else:
                print("Senha não encontrada para exclusão.")

    def update_password(self, servico: str, usuario: str, nova_senha: str) -> None:
        """
        Atualiza a senha de um serviço e usuário no banco de dados.

        Esta função permite atualizar a senha associada a um serviço e usuário
        específicos no banco de dados.

        Args:
            servico (str): O serviço cuja senha será atualizada.
            usuario (str): O usuário associado ao serviço.
            nova_senha (str): A nova senha para o serviço e usuário.

        Returns:
            None
        """
        # Verifica se o serviço e usuário existem no banco de dados
        documento = self.__collection.find_one(
            {"serviço": servico, "usuário": usuario})
        if documento:
            # Atualiza o campo "senha" com a nova senha
            self.__collection.update_one(
                {"serviço": servico, "usuário": usuario},
                {"$set": {"senha": nova_senha}}
            )
            print("Senha atualizada com sucesso.")
        else:
            print("Serviço e/ou usuário não encontrado. Nenhuma senha foi atualizada.")
