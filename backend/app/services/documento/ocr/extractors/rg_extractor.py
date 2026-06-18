import json

from app.models.versao_documento import VersaoDocumento

from app.services.documento.ocr.Utils import extrai_rg


class RGExtractor:

    @staticmethod
    def executar(
        versao_documento: VersaoDocumento
    ) -> tuple[dict, str]:

        '''dados_final = {}

        textos_extraidos = []

        for arquivo in versao_documento.arquivos:

            dados_json, texto_extraido = extrai_rg(
                arquivo.file_path,
                raw_data=True
            )

            dados_json = json.loads(
                dados_json
            )[0]

            dados_final.update(
                dados_json
            )

            if texto_extraido:

                textos_extraidos.append(
                    texto_extraido
                )

        texto_completo = "\n".join(
            textos_extraidos
        )'''

        dados_final = {
            "nome": "João Silva",
            "cpf": "12345678900",
            "rg": "2345678",
            "data_nascimento": "2000-01-01",
            "nome_pai": "José Silva",
            "nome_mae": "Maria Silva"
        }

        texto_completo = "texto extraido"

        return (
            dados_final,
            texto_completo
        )