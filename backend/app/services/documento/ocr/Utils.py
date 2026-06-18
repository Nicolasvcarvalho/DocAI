from app.services.documento.processors.RG import RG
from app.services.documento.processors.ComprovanteResidencia import ComprovanteResidencia
import os
import pandas as pd
import cv2 as cv
def extrai_rg(path_da_imagem: str, raw_data: bool = False) -> tuple[str,str]:
    """Recebe o caminho de uma imagem de um RG e devolve o json com os dados dela. Se o parâmetro raw_data for True, também devolve um json
    com a extração bruta dos dados numa tupla (dados_filtrados,dados_brutos) """
    if not os.path.exists(path_da_imagem): raise FileNotFoundError(f"Arquivo não encontrado: {path_da_imagem}")

    rg = cv.imread(path_da_imagem)

    if(rg is None): raise ValueError("Não foi possível decodificar a imagem. Verifique o formato. ")
   
    rg = RG(rg)

    rg_json = pd.DataFrame([rg.ExportarDict()])
    rg_json = rg_json.to_json(orient='records',force_ascii=False,indent=4)

    if(raw_data):
        raw_json = rg.ExtracaoOCR()
        raw_json = raw_json.drop('Box',axis=1)
        raw_json = raw_json.to_json(orient='records',force_ascii=False,indent=4)
        return (rg_json,raw_json)
    else: return (rg_json,"")


def extrai_compres(path_da_imagem: str, raw_data: bool = False) -> tuple[str, str]:
    """ Recebe o caminho de uma imagem de um comprovante de residência e devolve o json com os dados dela. 
    Se o parâmetro raw_data for True, também devolve um json com a extração bruta dos dados 
    numa tupla (dados_filtrados, dados_brutos).
    """
    if not os.path.exists(path_da_imagem): raise FileNotFoundError(f"Arquivo não encontrado: {path_da_imagem}")

    comp = cv.imread(path_da_imagem)

    if comp is None: raise ValueError("Não foi possível decodificar a imagem. Verifique o formato.")
    
    comp = ComprovanteResidencia(comp)

    comp_json = pd.DataFrame([comp.ExportarDict])
    comp_json = comp_json.to_json(orient='records', force_ascii=False, indent=4)

    if raw_data:
        raw_json = comp.ExtracaoOCR()
        if not raw_json.empty and 'Box' in raw_json.columns:
            raw_json = raw_json.drop('Box', axis=1)
        raw_json = raw_json.to_json(orient='records', force_ascii=False, indent=4)
        return (comp_json, raw_json)
    else: 
        return (comp_json, "")