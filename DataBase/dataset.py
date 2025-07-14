import streamlit as st
import pandas as pd
import os
from glob import glob

path_excel=os.path.join(os.getcwd(),'Notas')
excel='notas.xlsx'

def dados():

    temp_path=os.path.join(path_excel,excel)
    arq=glob(temp_path)


    df=pd.DataFrame(columns=['Chave NFe','NFe','Natureza Operação','Data de Emissão','CNPJ Emitente','Razão Social Emitente','Nome Fantasia Emitente','CNPJ Destinatário','Nome Fantasia Destinatário','SKU','Produto','NCM','CFOP','CST','Unid CMP','Qtde','Valor Unitário','Total dos Produtos','ICMS','Base de Cálculo'])    

    if len(arq)>0:

        df=pd.read_excel(temp_path)

        pass

    return df

    pass