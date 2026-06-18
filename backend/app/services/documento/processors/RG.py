import re
import unicodedata
from datetime import datetime
import numpy as np
import pandas as pd
import cv2 as cv
import matplotlib.pyplot as plt

from app.services.documento.processors.Documento import Documento

class RG(Documento):
    def __init__(self, imagem: np.ndarray) -> None:
        super().__init__(imagem)
       
        self.registro_geral: str = ""
        self.nome_candidato: str = ""
        self.naturalidade: str = ""
        self.data_nascimento: str | datetime = ""
        self.data_expedicao: str | datetime = ""
        self.cpf: str = ""
        self.orgao_emissor: str = ""
        self.nome_pai: str = ""
        self.nome_mae: str = ""
       
        self.ExtrairTexto()

    @property
    def TamanhoAlvo(self) -> tuple[int, int]:
        return (1920, 1080)

    def CorrigirOrientacao(self, img: np.ndarray) -> np.ndarray:
        alt, larg = img.shape[:2]
        max_dim = max(alt, larg)
       
        if max_dim > 1200:
            escala = 1200 / max_dim
            img_mini = cv.resize(img, (int(larg * escala), int(alt * escala)), interpolation=cv.INTER_AREA)
        else:
            img_mini = img.copy()
           
        rotacoes = {
            0: img_mini,
            90: cv.rotate(img_mini, cv.ROTATE_90_CLOCKWISE),
            180: cv.rotate(img_mini, cv.ROTATE_180),
            270: cv.rotate(img_mini, cv.ROTATE_90_COUNTERCLOCKWISE)
        }
       
        melhor_angulo = 0
        max_pontos = -1
       
        termos_peso_2 = ["BRASIL", "ESTADO", "SECRETARIA", "SEGURANCA", "REGISTRO", "GERAL", "NOME", "FILIACAO", "NATURALIDADE", "NASCIMENTO"]
        termos_peso_1 = ["SSP", "POLICIA", "IDENTIFICACAO", "PERICIAS", "TITULAR", "ASSINATURA", "PROIBIDO", "PLASTIFICAR"]
       
        for angulo, img_rot in rotacoes.items():
            textos = self._reader.readtext(img_rot, detail=0)
            texto_completo = " ".join(textos).upper() #type: ignore
           
            pontos = 0
            pontos += sum(2 for termo in termos_peso_2 if termo in texto_completo)
            pontos += sum(1 for termo in termos_peso_1 if termo in texto_completo)
           
            datas = re.findall(r'\d{2}/\d{2}/\d{4}', texto_completo)
            pontos += len(datas) * 5
           
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
        altura_atual, largura_atual = img_temp.shape[:2]
       
        nova_largura = int(largura_atual * 2)
        nova_altura = int(altura_atual * 2)
       
        if nova_largura > 0 and nova_altura > 0:
            img_temp = cv.resize(img_temp, (nova_largura, nova_altura), interpolation=cv.INTER_CUBIC)

        img_temp = self.FiltroCinza(imagem=img_temp, inplace=False)

        if img_temp is not None:
            clahe = cv.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
            img_temp = clahe.apply(img_temp)
        return img_temp #type:ignore

    def _remover_acentos(self, txt: str) -> str:
        return ''.join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')

   

    def ExtrairTexto(self) -> None:
        df_ocr = self.ExtracaoOCR()
       
        textos_originais = []
        textos_limpos = []
        mapa_ocr_numeros = str.maketrans("SBGOILZ", "5860112")

        for texto in df_ocr["Texto"]:
            if not str(texto).strip(): continue
            t_orig = str(texto).upper().strip()
            t_limpo = self._remover_acentos(t_orig)
            textos_originais.append(t_orig)
            textos_limpos.append(t_limpo)

        texto_completo_num = " ".join(textos_originais).translate(mapa_ocr_numeros)

        match_cpf = re.search(r'(?<!\d)(\d{3})\D{0,3}(\d{3})\D{0,3}(\d{3})\D{0,3}(\d{2})(?!\d)', texto_completo_num)
        if match_cpf:
            self.cpf = f"{match_cpf.group(1)}.{match_cpf.group(2)}.{match_cpf.group(3)}-{match_cpf.group(4)}"

        todas_datas = []
        for i, t in enumerate(textos_originais):
            t_num = t.translate(mapa_ocr_numeros)
            matches = re.findall(r'\b(\d{2})\s*[/|\-]\s*(\d{2})\s*[/|\-]\s*(\d{4})\b', t_num)
            for m in matches:
                data_str = f"{m[0]}/{m[1]}/{m[2]}"
                idx_inicio = max(0, i-2)
                idx_fim = min(len(textos_originais), i+3)
                contexto = " ".join(textos_originais[idx_inicio:idx_fim]).upper()
                todas_datas.append({'data': data_str, 'contexto': contexto})

        ano_atual = datetime.now().year
        datas_validas = []

        for item in todas_datas:
            d_str = item['data']
            ctx = item['contexto']
            try:
                dt = datetime.strptime(d_str, "%d/%m/%Y")
                if 1890 <= dt.year <= ano_atual + 20: # Permite futuro internamente para Válido Até
                    datas_validas.append({'dt': dt, 'str': d_str, 'ctx': ctx})
            except ValueError:
                continue

        for item in datas_validas:
            ctx = item['ctx']
            d_str = item['str']
            dt = item['dt']
           
            if "NASC" in ctx and not self.data_nascimento:
                self.data_nascimento = d_str
            elif ("EXPED" in ctx or "EMISS" in ctx) and dt.year <= ano_atual + 1 and not self.data_expedicao:
                self.data_expedicao = d_str

        if not self.data_nascimento or not self.data_expedicao:
            datas_passado = [d for d in datas_validas if d['dt'].year <= ano_atual + 1]
            datas_passado.sort(key=lambda x: x['dt'])
           
            if not self.data_nascimento and datas_passado:
                self.data_nascimento = datas_passado[0]['str']
            if not self.data_expedicao and len(datas_passado) > 1:
                self.data_expedicao = datas_passado[-1]['str']

        linhas_orgao = []
        termos_orgao = ["ESTADO", "SECRETARIA", "PERICIA", "DEFESA", "REPUBLICA", "SSP", "POLICIA", "SEGURANCA", "INSTITUTO", "GOVERNO", "FEDERAL", "CIVIL", "IDENTIFICACAO"]
        termos_rejeitados = ["COORDENADORIA", "HUMANA", "BIOMETRICA", "CARTEIRA", "NACIONAL"]
       
        for t in textos_originais[:30]:
            t_sem_acento = self._remover_acentos(t)
            if any(p in t_sem_acento for p in termos_orgao) and not any(ex in t_sem_acento for ex in termos_rejeitados):
                t_limpo = re.sub(r'[^A-Z\s/\-]', '', t).strip()
                if len(t_limpo) > 4 and t_limpo not in linhas_orgao:
                    linhas_orgao.append(t_limpo)
        if linhas_orgao: self.orgao_emissor = " / ".join(linhas_orgao)

        candidatos_rg = []
        for i, t in enumerate(textos_originais):
            t_num = t.translate(mapa_ocr_numeros).replace('.', '')
            matches_rg = re.finditer(r'\b(\d{5,11})\s*[-]?\s*([0-9X])?\b', t_num)
           
            for m in matches_rg:
                num_completo = m.group(1) + (m.group(2) if m.group(2) else "")
                apenas_num = m.group(1)
               
                eh_cpf = self.cpf and (apenas_num in self.cpf.replace('.', '').replace('-', ''))
   
                eh_data = any(apenas_num in d['data'].replace('/', '') for d in todas_datas)
               
   
                if not eh_cpf and not eh_data and len(apenas_num) >= 5:
                    idx_inicio = max(0, i-3)
                    idx_fim = min(len(textos_originais), i+4)
                    contexto = " ".join(textos_originais[idx_inicio:idx_fim]).upper()
                   
                    peso = 0
                    if "REGISTRO" in contexto or "GERAL" in contexto or "IDENTIDADE" in contexto: peso += 10
                    if len(num_completo) >= 8: peso += 5
                   
                    candidatos_rg.append({'num': num_completo, 'peso': peso})

        if candidatos_rg:
            candidatos_rg.sort(key=lambda x: x['peso'], reverse=True)
            self.registro_geral = candidatos_rg[0]['num']
            if len(self.registro_geral) >= 8 and '-' not in self.registro_geral:
                self.registro_geral = self.registro_geral[:-1] + "-" + self.registro_geral[-1]

        def eh_lixo(texto: str) -> bool:
            if len(texto) < 3: return True
            t_upper = re.sub(r'[^\w\s]', '', self._remover_acentos(texto)).upper()
           

            fatais = [
                "SECRETARIA", "SEGURANCA", "PUBLICA", "PERICIA", "FORENSE",
                "COORDENADORIA", "IDENTIFICACAO", "BIOMETRICA", "VALIDA", "TERRITORIO",
                "REGISTRO", "GERAL", "REPUBLICA", "FEDERATIVA", "BRASIL", "ESTADO",
                "ASSINATURA", "DIRETOR", "POLEGAR", "PLASTIFICAR", "PROIBIDO", "MINISTERIO",
                "DATA", "EXPEDICAO", "DEFESA", "SOCIAL", "GOVERNO", "DOCUMENTO",
                "NASOIME", "IMENI", "MENI", "CARTEIRA", "EMISSAO", "DIREITO",
                "ESQUERDO", "LEI", "VIA", "CPF", "ORIGEM", "MUNICIPIO",
                "NACION", "DAFES", "DEFES", "SOCI", "TERRITO", "SSP", "DETRAN", "POLICIA"
            ]
            if any(f in t_upper for f in fatais): return True
            palavras = set(t_upper.split())
            if palavras.issubset({"DE", "DA", "DO", "DOS", "DAS", "RG", "O", "N", "UF", "A"}): return True
            return False

        def limpar_linha(texto: str) -> str:

            t = re.sub(r'\b(N[O0D]?ME( SOCIAL)?|NAME|HOME|HDME|HANIE|FILI[A-Z]*|FILA[A-Z]*|ILIACA|FLIACA|NATURAL[A-Z]*|DATADE|LOCAL|DOC\.? ORIGEM|NASCIMENTO|PAI|M[AÃ]E)\b', '', texto, flags=re.IGNORECASE)
            t = re.sub(r'[^A-Z\s]', '', self._remover_acentos(t))
            return re.sub(r'\s+', ' ', t).strip()

        estado_atual = None
        linhas_nome, linhas_filiacao, linhas_naturalidade = [], [], []

        for i, t_orig in enumerate(textos_originais):
            t_limpo = textos_limpos[i]
            t_upper_raw = re.sub(r'[^\w\s]', '', t_limpo)


            if re.search(r'\b(N[O0D]ME|NAME|NDME|HOME|HDME)', t_upper_raw):
                estado_atual = 'NOME'
            elif re.search(r'\b(FILI|FILA|ILIAC|FLIAC|FLLJ|PAI|MAE)', t_upper_raw):
                estado_atual = 'FILIACAO'
            elif re.search(r'\b(NATU|LOCAL|MUNIC)', t_upper_raw):
                estado_atual = 'NATURALIDADE'
            elif re.search(r'\b(DOC|ORIGEM|CPF|REGIST|ASSIN|DATA|LEI|VALID|NASC|POLEG)', t_upper_raw):
                if estado_atual in ['NOME', 'FILIACAO']:
                    estado_atual = 'OUTRO'

            conteudo_limpo = limpar_linha(t_orig)
           
            if conteudo_limpo and not eh_lixo(conteudo_limpo):
                if estado_atual == 'NOME':
                    if conteudo_limpo not in linhas_nome:
                        linhas_nome.append(conteudo_limpo)
                elif estado_atual == 'FILIACAO':
                    if not any(conteudo_limpo == n for n in linhas_nome) and conteudo_limpo not in linhas_filiacao:
                        linhas_filiacao.append(conteudo_limpo)
                elif estado_atual == 'NATURALIDADE':
                    if conteudo_limpo not in linhas_naturalidade:
                        linhas_naturalidade.append(conteudo_limpo)

        if linhas_nome: self.nome_candidato = " ".join(linhas_nome)
       
        if linhas_filiacao:
            if len(linhas_filiacao) >= 2:
                meio = len(linhas_filiacao) // 2
                self.nome_pai = " ".join(linhas_filiacao[:meio]).strip()
                self.nome_mae = " ".join(linhas_filiacao[meio:]).strip()
            else:
                self.nome_mae = linhas_filiacao[0]

        if linhas_naturalidade:
            self.naturalidade = linhas_naturalidade[0]
        else:
            ufs = "AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO"
            for t in textos_originais:
                t_limpo = re.sub(r'\b(NASCIMENTO|NATURALIDADE)\b', '', t.upper()).strip()
                match_nat = re.search(fr'\b([A-Z\s]{{3,}}?)\s*[-/]*\s*({ufs})\b', t_limpo)
                if match_nat:
                    cand_nat = f"{match_nat.group(1).strip()}-{match_nat.group(2)}"
       
                    if not eh_lixo(self._remover_acentos(cand_nat.replace('-', ' '))):
                        self.naturalidade = cand_nat
                        break

    def ObterDataNascimentoComoDatetime(self) -> datetime | None:
        if isinstance(self.data_nascimento, str) and self.data_nascimento:
            dt = self.ConveterStringParaDatetime(self.data_nascimento)
            if dt: self.data_nascimento = dt
        return self.data_nascimento if isinstance(self.data_nascimento, datetime) else None

    def ObterDataExpedicaoComoDatetime(self) -> datetime | None:
        if isinstance(self.data_expedicao, str) and self.data_expedicao:
            dt = self.ConveterStringParaDatetime(self.data_expedicao)
            if dt: self.data_expedicao = dt
        return self.data_expedicao if isinstance(self.data_expedicao, datetime) else None

    def ConveterStringParaDatetime(self, data_str: str) -> datetime | None:
        if not data_str: return None
        try: return datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError: return None

    def ExportarDict(self) -> dict:
        return {
            "nome": self.nome_candidato,
            "rg": self.registro_geral,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento,
            "nome_pai": self.nome_pai,
            "nome_mae": self.nome_mae,
        }

