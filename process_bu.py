#!/usr/bin/python

import sys

from PIL import Image
from pyzbar.pyzbar import decode


TRANSLATIONS = {
    "QRBU": "Boletim de urna: {}",
    "VRQR": "Versão do QR code: {}",
    "VRCH": "Versão da chave: {}",
    "ORIG": "Origem do boletim de urna: {}",
    "ORLC": "Origem da configuração: {}",
    "PROC": "Número do processo eleitoral: {}",
    "DTPL": "Data do pleito: {}",
    "PLEI": "Número do pleito: {}",
    "TURN": "Turno: {}",
    "FASE": "Fase: {}",
    "UNFE": "Unidade federativa: {}",
    "MUNI": "Municipio: {}",
    "ZONA": "Zona: {}",
    "SECA": "Seção: {}",
    "IDUE": "Número de série da urna: {}",
    "IDCA": "Código de identificação da carga: {}",
    "LOCA": "Número do local de votação: {}",
    "APTO": "Quantidade de eleitores aptos: {}",
    "COMP": "Quantidade de eleitores que compareceram para votar: {}",
    "FALT": "Quantidade de eleitores que faltaram: {}",
    "DTAB": "Data de abertura da urna: {}",
    "HRAB": "Hora de abertura da urna: {}",
    "DTFC": "Data de fechamento da urna: {}",
    "HRFC": "Hora de fechamento da urna: {}",
    "IDEL": "Código da eleição: {}",
    "CARG": "Código do cargo: {}",
    "TIPO": "Tipo: {}",
    "VERC": "Versão do pacote de dados: {}",
    "PART": "Número do partido: {}",
    "LEGP": "Quantidade de votos de legenda para o partido: {}",
    "TOTP": "Total de votos apurados para o partido: {}",
    "HASH": "Hash da seção de conteúdo do boletim de urna: {}",
}


class Translator:

    def translate(self, key, value):
        value_processor = getattr(self, key.lower(), None)
        if value_processor:
            new_value = value_processor(value)
        else:
            new_value = value

        translation_text = TRANSLATIONS.get(key, key + ": {}")
        return translation_text.format(new_value)

    @staticmethod
    def qrbu(value):
        return value.replace(":", "/")

    @staticmethod
    def orlc(value):
        low_value = value.lower()
        if low_value == "leg":
            return "Eleição oficial"
        elif low_value == "com":
            return "Eleição comunitária"
        else:
            return value


def translate_bu(bu_data):
    translator = Translator()
    for key, value in bu_data:
        print(translator.translate(key, value))


def read_bu(image_path):
    decoded = decode(Image.open(image_path))
    if not decoded:
        return [("Erro de leitura", image_path)]
    data = decoded[0].data.decode("utf-8")
    split_data = data.split(" ")
    bu_data = []
    for item in split_data:
        key, value = item.split(":", 1)
        bu_data.append((key, value))
    return bu_data


def main():
    pass


if __name__ == "__main__":
    translate_bu(read_bu(sys.argv[1]))
