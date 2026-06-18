import re
import unicodedata
import numpy as np
import pandas as pd
import cv2 as cv
import requests
from app.services.documento.processors.Documento import Documento

class ComprovanteResidencia(Documento):
    def __init__(self, imagem: np.ndarray) -> None:
        super().__init__(imagem)
        
        self.logradouro: str = ""
        self.numero: str = ""
        self.bairro: str = ""
        self.cidade: str = ""
        self.estado: str = ""
        self.cep: str = ""
        
        self.ExtrairTexto()

    @property
    def TamanhoAlvo(self) -> tuple[int, int]:
        return (1920, 1080)

    @property
    def ExportarDict(self) -> dict:
        return {
            "Logradouro": self.logradouro if self.logradouro else "",
            "Número": self.numero if self.numero else "",
            "Bairro": self.bairro if self.bairro else "",
            "Cidade": self.cidade if self.cidade else "",
            "Estado": self.estado if self.estado else "",
            "CEP": self.cep if self.cep else ""
        }

    def CorrigirOrientacao(self, img: np.ndarray) -> np.ndarray:
        alt, larg = img.shape[:2]
        max_dim = max(alt, larg)
        escala = 1000 / max_dim if max_dim > 1000 else 1.0
        img_mini = cv.resize(img, (int(larg * escala), int(alt * escala)), interpolation=cv.INTER_AREA)
        
        if len(img_mini.shape) == 3:
            img_mini_gray = cv.cvtColor(img_mini, cv.COLOR_BGR2GRAY)
        else:
            img_mini_gray = img_mini.copy()
            
        rotacoes = {
            0: img_mini_gray,
            90: cv.rotate(img_mini_gray, cv.ROTATE_90_CLOCKWISE),
            180: cv.rotate(img_mini_gray, cv.ROTATE_180),
            270: cv.rotate(img_mini_gray, cv.ROTATE_90_COUNTERCLOCKWISE)
        }
        
        melhor_angulo = 0
        max_pontos = -1
        termos_chave = ["CEP", "CP", "ENDERECO", "RUA", "AVENIDA", "BAIRRO", "FATURA", "CONSUMO"]
        
        for angulo, img_rot in rotacoes.items():
            h, w = img_rot.shape[:2]
            topo_teste = img_rot[0:int(h * 0.65), 0:w]
            
            textos = self._reader.readtext(topo_teste, detail=0)
            texto_completo = " ".join(textos).upper()
            texto_completo = self._remover_acentos(texto_completo)
            
            pontos = sum(1 for termo in termos_chave if termo in texto_completo)
            ceps = re.findall(r'\b\d{5}-?\d{3}\b', texto_completo)
            pontos += len(ceps) * 5
            
            if pontos > max_pontos:
                max_pontos = pontos
                melhor_angulo = angulo
                
        if melhor_angulo != 0:
            if melhor_angulo == 90: return cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
            elif melhor_angulo == 180: return cv.rotate(img, cv.ROTATE_180)
            elif melhor_angulo == 270: return cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
            
        return img

    def PreProcessar(self) -> np.ndarray:
        img_temp = self.imagem.copy()
        img_temp = self.CorrigirOrientacao(img_temp)
        
        alt, larg = img_temp.shape[:2]
        img_temp = img_temp[0:int(alt * 0.65), 0:larg]
        
        if len(img_temp.shape) == 3:
            img_temp = cv.cvtColor(img_temp, cv.COLOR_BGR2GRAY)

        img_temp = cv.resize(img_temp, None, fx=2.0, fy=2.0, interpolation=cv.INTER_CUBIC)

        clahe = cv.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
        img_temp = clahe.apply(img_temp)
            
        return img_temp

    def _remover_acentos(self, txt: str) -> str:
        return ''.join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')

    def _validar_e_buscar_cep(self, cep: str) -> bool:
        try:
            cep_limpo = re.sub(r'\D', '', cep)
            if len(cep_limpo) == 8:
                response = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=5)
                if response.status_code == 200:
                    dados = response.json()
                    if "erro" not in dados:
                        self.cidade = dados.get("localidade", "").upper()
                        self.estado = dados.get("uf", "").upper()
                        self.logradouro = dados.get("logradouro", "").upper()
                        self.bairro = dados.get("bairro", "").upper()
                        return True
        except requests.exceptions.RequestException as e:
            print(f"Erro na API ViaCEP: {e}")
        return False

    def ExtrairTexto(self) -> None:
        df_ocr = self.ExtracaoOCR()
        linhas_documento = []
        
        if not df_ocr.empty:
            df_ocr['y_centro'] = df_ocr['Box'].apply(lambda b: (b[0][1] + b[2][1]) / 2)
            df_ocr['x_min'] = df_ocr['Box'].apply(lambda b: min(p[0] for p in b))
            df_ocr['altura'] = df_ocr['Box'].apply(lambda b: b[2][1] - b[0][1])
            
            tolerancia_y = df_ocr['altura'].median() * 0.8 
            
            df_ocr = df_ocr.sort_values(by='y_centro').reset_index(drop=True)
            linhas_brutas = []
            linha_temp = []
            y_anterior = -1
            
            for _, row in df_ocr.iterrows():
                y_centro = row['y_centro']
                if y_anterior == -1 or abs(y_centro - y_anterior) <= tolerancia_y:
                    linha_temp.append(row)
                    if y_anterior == -1: y_anterior = y_centro
                    else: y_anterior = (y_anterior + y_centro) / 2 
                else:
                    linhas_brutas.append(linha_temp)
                    linha_temp = [row]
                    y_anterior = y_centro
                    
            if linha_temp:
                linhas_brutas.append(linha_temp)

            for linha_b in linhas_brutas:
                linha_b_ordenada = sorted(linha_b, key=lambda r: r['x_min'])
                textos = [str(r['Texto']).strip() for r in linha_b_ordenada if str(r['Texto']).strip()]
                if textos:
                    linhas_documento.append(" ".join(textos).upper())

        mapa_ocr_numeros = str.maketrans("SBGOILZsbgoilz", "58601125860112")
        
        ceps_candidatos = []
        
        regex_cep_ancorado = r'(?:C[\W_]*E?[\W_]*P)[\W_]*(\d{5})[\W_]*(\d{3})'
        regex_cep_solto = r'(?<!\d)(\d{5})[\W_]*(\d{3})(?!\d)'

        for linha in linhas_documento:
            linha_num = linha.translate(mapa_ocr_numeros)
            
            for m in re.finditer(regex_cep_ancorado, linha_num):
                cep_cand = f"{m.group(1)}-{m.group(2)}"
                if cep_cand not in ceps_candidatos: ceps_candidatos.append(cep_cand)
                
            for m in re.finditer(regex_cep_solto, linha_num):
                cep_cand = f"{m.group(1)}-{m.group(2)}"
                if cep_cand not in ceps_candidatos: ceps_candidatos.append(cep_cand)

        cep_final_valido = None
        
        for cep_cand in reversed(ceps_candidatos):
            if self._validar_e_buscar_cep(cep_cand):
                cep_final_valido = cep_cand
                self.cep = cep_cand
                break
                
        if not cep_final_valido and ceps_candidatos:
            self.cep = ceps_candidatos[-1]

        indicadores_rua = r'\b(RUA|ROA|AVENIDA|AV\.|AV|TRAVESSA|RODOVIA|ALAMEDA|PRACA|R\.|R)\b'
        
        for i, linha in enumerate(linhas_documento):
            linha_limpa = self._remover_acentos(linha)
            
            if re.search(indicadores_rua, linha_limpa):
                partes = [p.strip() for p in re.split(r'[,]', linha)]
                
                if len(partes) >= 2:
                    num_str = partes[1].translate(mapa_ocr_numeros)
                    match_num = re.match(r'^([S/N]+|\d+[A-Z]?)', num_str)
                    if match_num:
                        self.numero = match_num.group(1).strip()
                    else:
                        self.numero = num_str.split()[0] if num_str else ""
                    break
                else:
                    linha_fixa = linha.translate(mapa_ocr_numeros).strip()
                    match_sem_virgula = re.search(r'(?:RUA|ROA|AVENIDA|AV\.|AV|TRAVESSA|RODOVIA|ALAMEDA|PRACA|R\.|R).*?\s+([S/N]+|\d+[A-Z]?)', linha_fixa)
                    if match_sem_virgula:
                        self.numero = match_sem_virgula.group(1).strip()
                    break
