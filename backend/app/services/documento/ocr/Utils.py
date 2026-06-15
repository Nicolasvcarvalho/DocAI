import json
from ...processors.RG import RG
import os
import cv2 as cv
def extrai_rg(path_da_imagem: str, raw_data: bool = False) -> str:
    """Recebe o caminho de uma imagem de um RG e devolve o json com os dados dela. """
    if not os.path.exists(path_da_imagem): raise FileNotFoundError(f"Arquivo não encontrado: {path_da_imagem}")

    rg = cv.imread(path_da_imagem)

    if(rg is None): raise ValueError("Não foi possível decodificar a imagem. Verifique o formato. ")
    
    rg = RG(rg)

    rg_json = json.dumps(rg.ExportarDict(),ensure_ascii=False,indent=4,default=str)
    return rg_json

def extrai_compres(path_da_imagem: str) -> str:
    """Recebe o caminho de uma imagem de um Comprovante de Residência e devolve o json com os dados dele. """
    return ""