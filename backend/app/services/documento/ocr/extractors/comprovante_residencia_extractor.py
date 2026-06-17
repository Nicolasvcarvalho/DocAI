import json

from app.models.versao_documento import VersaoDocumento

from app.services.documento.ocr.Utils import extrai_compres

class ComprovanteResidenciaExtractor:

    @staticmethod
    def executar(
        versao_documento: VersaoDocumento
    ) -> tuple[dict, str]:

        arquivo = versao_documento.arquivos[0]

        '''dados_json, texto_extraido = (
            extrai_compres(
                arquivo.file_path,
                raw_data=True
            )
        )'''

        '''dados_json = json.loads(
            dados_json
        )[0]'''

        
        dados_json = {
        "logradouro": "Rua das Flores",
        "numero": "123",
        "bairro": "Centro",
        "cidade": "Fortaleza",
        "estado": "CE",
        "cep": "60000-000"
        }

        texto_extraido = "texto extraido"

        return (
            dados_json,
            texto_extraido
        )