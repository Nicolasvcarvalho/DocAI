from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import cv2 as cv
import easyocr
import matplotlib.pyplot as plt

class Documento(ABC):
    _reader: easyocr.Reader = easyocr.Reader(['pt', 'en'], gpu=True) 

    def __init__(self, imagem: np.ndarray) -> None:
        self.imagem: np.ndarray = imagem

    @property
    @abstractmethod
    def TamanhoAlvo(self) -> tuple[int, int]:
        pass
    
    @abstractmethod
    def ExtrairTexto(self) -> dict | str:
        """Cada documento implementa sua lógica p/ extrair """
        pass
    
    @property
    @abstractmethod
    def ExportarDict(self) -> dict:
        pass
    
    @abstractmethod
    def CorrigirOrientacao(self,imagem: np.ndarray) -> np.ndarray:
        pass
    
    def PreProcessar(self) -> np.ndarray:
        """Método hook. Por padrão, retorna a cópia da imagem original. Classes filhas DEVEM sobrescrever este método para aplicar seus filtros específicos """
        return self.imagem.copy()
        
    def ExtracaoOCR(self) -> pd.DataFrame:
        imagem_pronta = self.PreProcessar()
        resultados = self._reader.readtext(imagem_pronta)

        altura_img = imagem_pronta.shape[0]
        banda_y = max(15, altura_img // 65)

        if resultados:
            resultados.sort(key=lambda r: (r[0][0][1] // banda_y, r[0][0][0])) #type: ignore

        dados = [
            {"Box": bbox, "Texto": texto, "Confianca": confianca} 
            for (bbox, texto, confianca) in resultados
        ]
        return pd.DataFrame(dados)
    def DesenharDetectados(self, resultados_ocr: list) -> np.ndarray:
        """Método utilitário para desenhar retângulos ao redor dos textos detectados """
        img_copia = self.imagem.copy()
        for (bbox, texto, prob) in resultados_ocr:

            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            

            cv.rectangle(img_copia, top_left, bottom_right, (0, 0, 255), 2)
        return img_copia
    def FiltroCinza(self, imagem: np.ndarray | None = None, inplace: bool = False) -> np.ndarray | None:
        img = self.imagem if imagem is None else imagem
        cinza = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        if inplace: 
            self.imagem = cinza
            return None
        return cinza

    def AlteraDimensoes(self, imagem: np.ndarray | None = None, size: tuple[int, int] | None = None, inplace: bool = False) -> np.ndarray | None:
        img = self.imagem if imagem is None else imagem
        largura_alvo, altura_alvo = size if size is not None else self.TamanhoAlvo
        altura_orig, largura_orig = img.shape[:2]
        escala = min(largura_alvo / largura_orig, altura_alvo / altura_orig)
        nova_largura = int(largura_orig * escala)
        nova_altura = int(altura_orig * escala)
        img_redimensionada = cv.resize(img, (nova_largura, nova_altura), interpolation=cv.INTER_AREA)
        if len(img.shape) == 3:
            fundo_branco = np.full((altura_alvo, largura_alvo, 3), 255, dtype=np.uint8)
        else:
            fundo_branco = np.full((altura_alvo, largura_alvo), 255, dtype=np.uint8)
        x_offset = (largura_alvo - nova_largura) // 2
        y_offset = (altura_alvo - nova_altura) // 2
        fundo_branco[y_offset:y_offset + nova_altura, x_offset:x_offset + nova_largura] = img_redimensionada
        if inplace:
            self.imagem = fundo_branco
            return None
        return fundo_branco

    def ReducaoRuido(self, imagem: np.ndarray | None = None, size: tuple[int, int] = (5, 5), sigmax: float = 0, sigmay: float = 0, inplace: bool = False) -> np.ndarray | None:
        """Usa do ruído gaussiano para reduzir o ruído da imagem """
        if size[0] % 2 == 0 or size[1] % 2 == 0 or size[0] <= 0 or size[1] <= 0: raise ValueError("Kernel inválido")
        img = self.imagem if imagem is None else imagem
        blur_img = cv.GaussianBlur(src=img, ksize=size, sigmaX=sigmax, sigmaY=sigmay)
        if inplace: self.imagem = blur_img; return None
        return blur_img

    def Binarizacao(self, imagem: np.ndarray | None = None, inplace: bool = False) -> np.ndarray | None:
        img = self.imagem if imagem is None else imagem
        _, img_bin = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        if inplace: self.imagem = img_bin; return None
        return img_bin

    def Bordas(self, imagem: np.ndarray | None = None, inplace: bool = False) -> np.ndarray | None:
        img = self.imagem if imagem is None else imagem
        bordas = cv.Canny(img, 100, 200)
        if inplace: self.imagem = bordas; return None
        return bordas

    def Norm(self, imagem: np.ndarray | None = None, inplace: bool = False) -> np.ndarray | None:
        img = self.imagem if imagem is None else imagem
        img_norm = img.astype(np.float32) / 255.0
        if inplace: self.imagem = img_norm; return None
        return img_norm
    
    def ExibeImagem(self) -> None:
        self.imagem = cv.cvtColor(self.imagem,cv.COLOR_BGR2RGB)
        plt.imshow(self.imagem)
        plt.axis('off')
        plt.show()
