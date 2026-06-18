import json

from app.models.versao_documento import VersaoDocumento

from app.services.documento.ocr.Utils import extrai_compres

class ComprovanteResidenciaExtractor:

    @staticmethod
    def executar(
        versao_documento: VersaoDocumento
    ) -> tuple[dict, str]:

        arquivo = versao_documento.arquivos[0]

        dados_json, texto_extraido = extrai_compres(arquivo.file_path, raw_data=True)

        dados_json = json.loads(dados_json)[0]

        return (
            dados_json,
            texto_extraido
        )