import re
import cv2 as cv
import numpy as np
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
            "logradouro": self.logradouro if self.logradouro else "",
            "numero": self.numero if self.numero else "",
            "bairro": self.bairro if self.bairro else "",
            "cidade": self.cidade if self.cidade else "",
            "estado": self.estado if self.estado else "",
            "cep": self.cep if self.cep else ""
        }

    def CorrigirOrientacao(self, img: np.ndarray) -> np.ndarray:
        """
        Testa as 4 rotações possíveis em uma miniatura da imagem.
        A rotação que revelar mais palavras-chave é a correta.
        """
        alt, larg = img.shape[:2]
        escala = 600 / max(alt, larg)
        img_mini = cv.resize(img, (0, 0), fx=escala, fy=escala)
        
        rotacoes = {
            0: img_mini,
            90: cv.rotate(img_mini, cv.ROTATE_90_CLOCKWISE),
            180: cv.rotate(img_mini, cv.ROTATE_180),
            270: cv.rotate(img_mini, cv.ROTATE_90_COUNTERCLOCKWISE)
        }
        
        palavras_chave = ["CEP", "RUA", "AV", "AVENIDA", "BAIRRO", "VALOR", "VENCIMENTO", "FATURA", "ENEL", "CAGECE", "MÊS", "PAGAMENTO"]
        
        melhor_rotacao = 0
        max_matches = -1
        
        
        for angulo, img_rot in rotacoes.items():
            resultados = self._reader.readtext(img_rot, detail=0)
            texto_amostra = " ".join(resultados).upper()
            matches = sum(1 for p in palavras_chave if p in texto_amostra)
            
            if matches > max_matches:
                max_matches = matches
                melhor_rotacao = angulo
                
        
        if melhor_rotacao == 90:
            return cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
        elif melhor_rotacao == 180:
            return cv.rotate(img, cv.ROTATE_180)
        elif melhor_rotacao == 270:
            return cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
            
        return img

    def PreProcessar(self) -> np.ndarray:
        img_corrigida = self.CorrigirOrientacao(self.imagem)
        altura = img_corrigida.shape[0]
        
        
        img_topo = img_corrigida[0 : int(altura * 0.45), :]
        
        if len(img_topo.shape) == 3:
            img_cinza = cv.cvtColor(img_topo, cv.COLOR_BGR2GRAY)
        else:
            img_cinza = img_topo
            
        img_upscaled = cv.resize(img_cinza, None, fx=2.0, fy=2.0, interpolation=cv.INTER_CUBIC)
        img_processada = cv.GaussianBlur(img_upscaled, (3, 3), 0)
        
        self.imagem = img_processada
        return self.imagem

    def _limpar_numero(self, num_str: str) -> str:
        """Helper para limpar o número encontrado e padronizar S/N"""
        num_limpo = num_str.strip(' ,.-/')
        if num_limpo in ['S/N', 'SN', 'S', 'N']:
            return 'S/N'
        return num_limpo

    def ExtrairTexto(self) -> None:
        df_texto = self.ExtracaoOCR()
        
        if df_texto is None or df_texto.empty:
            return

        linhas_texto = df_texto['Texto'].astype(str).tolist()
        texto_completo = " ".join(linhas_texto).upper()

        
        match_cep = re.search(r'\b(\d{2}[\.\s]?\d{3}[\-\s]?\d{3})\b', texto_completo)

        if match_cep:
            cep_puro = re.sub(r'\D', '', match_cep.group(1))
            if len(cep_puro) == 8:
                self.cep = f"{cep_puro[:5]}-{cep_puro[5:]}"
                
                try:
                    response = requests.get(f"https://viacep.com.br/ws/{cep_puro}/json/", timeout=5)
                    if response.status_code == 200:
                        dados = response.json()
                        if "erro" not in dados:
                            self.logradouro = dados.get("logradouro", "").upper()
                            self.bairro = dados.get("bairro", "").upper()
                            self.cidade = dados.get("localidade", "").upper()
                            self.estado = dados.get("uf", "").upper()
                except requests.RequestException:
                    pass

        
        if self.logradouro:
            nome_rua = self.logradouro
            for termo in ["RUA ", "AVENIDA ", "AV ", "TRAVESSA ", "RODOVIA ", "PRAÇA "]:
                nome_rua = nome_rua.replace(termo, "")
            nome_rua = nome_rua.strip()

            
            regex_ancora = r'(?:[,\-\s]+|N[O°º]?\s+)(S/?N|SN|\d{1,5}[A-Z]?)'

            for i, linha in enumerate(linhas_texto):
                linha_upper = linha.upper()
                
                
                if nome_rua in linha_upper and len(nome_rua) > 3:
                    parte_posterior = linha_upper.split(nome_rua)[-1]
                    
                    match_num = re.search(regex_ancora, parte_posterior)
                    if match_num and match_num.group(1):
                        self.numero = self._limpar_numero(match_num.group(1))
                        if self.numero: break
                    
                    
                    if i + 1 < len(linhas_texto):
                        prox_linha = linhas_texto[i+1].upper()
                        
                        match_num_prox = re.search(r'^(?:[,\-\s]*|N[O°º]?\s*)(S/?N|SN|\d{1,5}[A-Z]?)', prox_linha)
                        if match_num_prox and match_num_prox.group(1):
                            self.numero = self._limpar_numero(match_num_prox.group(1))
                            if self.numero: break

        
        if not self.numero:
            for linha in linhas_texto:
                linha_upper = linha.upper()
                
                match_virgula = re.search(r',\s*(S/?N|SN|\d{1,5}[A-Z]?)\b', linha_upper)
                if match_virgula:
                    cand = match_virgula.group(1)
                    cand_limpo = self._limpar_numero(cand)
                    if cand_limpo: 
                        self.numero = cand_limpo
                        break
