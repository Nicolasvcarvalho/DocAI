import json

from app.models.versao_documento import VersaoDocumento

from app.services.documento.ocr.Utils import extrai_rg


class RGExtractor:

    @staticmethod
    def executar(
        versao_documento: VersaoDocumento
    ) -> tuple[dict, str]:

        dados_final = {}

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
        )

        return (
            dados_final,
            texto_completo
        )