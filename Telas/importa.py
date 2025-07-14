import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import os
from glob import glob
import pandas as pd
import time
from datetime import datetime
import xmltodict
import json
import socket as s

class Importador:

    def __init__(self):
        
        self.IP=s.gethostbyname(s.gethostname())
        self.path_base=os.path.join(os.getcwd(),'XML')
        os.makedirs(self.path_base,exist_ok=True)

        self.path_excel=os.path.join(os.getcwd(),'Notas')
        os.makedirs(self.path_excel,exist_ok=True)

        self.excel='notas.xlsx'

        temp_path=os.path.join(os.getcwd(),'PC',self.IP,'log.xlsx')
        self.xlsx=pd.read_excel(temp_path,dtype='object')

        pass

    def main(self):

        placehoder=st.empty()

        var_dict=dict()

        with placehoder.container():

            divs=st.columns([1,5,1],vertical_alignment='center')

            with divs[1].container():

                st.title('Importador XML')
                st.markdown('----')
                
                st.file_uploader(label='Importar',type='.xml',key='file_xml',accept_multiple_files=True)

                if st.session_state['file_xml']!=None:

                    df=pd.DataFrame(columns=['Chave NFe','NFe','Natureza Operação','Data de Emissão','CNPJ Emitente','Razão Social Emitente','Nome Fantasia Emitente','CNPJ Destinatário','Nome Fantasia Destinatário','SKU','Produto','NCM','CFOP','CST','Unid CMP','Qtde','Valor Unitário','Total dos Produtos','ICMS','Base de Cálculo'])                

                    for files in st.session_state['file_xml']:

                        dados_byte=files.getvalue()
                        name_file=files.name

                        temp_path=os.path.join(self.path_base,name_file)

                        with open(temp_path,'wb') as file:

                            file.write(dados_byte)

                            pass

                        with open(temp_path,'rb') as file:

                            xml=xmltodict.parse(file)

                            var_dict['chave']=xml['nfeProc']['protNFe']['infProt']['chNFe']
                            var_dict['natOp']=xml['nfeProc']['NFe']['infNFe']['ide']['natOp']
                            var_dict['nNF']=xml['nfeProc']['NFe']['infNFe']['ide']['nNF']
                            var_dict['dhEmi']=xml['nfeProc']['NFe']['infNFe']['ide']['dhEmi']
                            var_dict['emitCNPJ']=xml['nfeProc']['NFe']['infNFe']['emit']['CNPJ']
                            var_dict['emitxNome']=xml['nfeProc']['NFe']['infNFe']['emit']['xNome']
                            var_dict['emitxFant']=xml['nfeProc']['NFe']['infNFe']['emit']['xFant']
                            var_dict['detCNPJ']=xml['nfeProc']['NFe']['infNFe']['dest']['CNPJ']
                            var_dict['detxNome']=xml['nfeProc']['NFe']['infNFe']['dest']['xNome']

                            try:

                                var_dict['det']=xml['nfeProc']['NFe']['infNFe']['det']
                                
                                for p in var_dict['det']:

                                    df.loc[len(df)]=[var_dict['chave'],var_dict['nNF'],var_dict['natOp'],var_dict['dhEmi'],var_dict['emitCNPJ'],var_dict['emitxNome'],var_dict['emitxFant'],var_dict['detCNPJ'],var_dict['detxNome'],p['prod']['cProd'],p['prod']['xProd'],p['prod']['NCM'],p['prod']['CFOP'],p['imposto']['ICMS']['ICMS20']['CST'],p['prod']['uCom'],p['prod']['qCom'],p['prod']['vUnCom'],p['prod']['vProd'],p['imposto']['ICMS']['ICMS20']['vICMS'],p['imposto']['ICMS']['ICMS20']['vBC']]


                                    pass

                                pass

                            except:

                                df.loc[len(df)]=[var_dict['chave'],var_dict['nNF'],var_dict['natOp'],var_dict['dhEmi'],var_dict['emitCNPJ'],var_dict['emitxNome'],var_dict['emitxFant'],var_dict['detCNPJ'],var_dict['detxNome'],xml['nfeProc']['NFe']['infNFe']['det']['prod']['cProd'],xml['nfeProc']['NFe']['infNFe']['det']['prod']['xProd'],xml['nfeProc']['NFe']['infNFe']['det']['prod']['NCM'],xml['nfeProc']['NFe']['infNFe']['det']['prod']['CFOP'],xml['nfeProc']['NFe']['infNFe']['det']['imposto']['ICMS']['ICMS20']['CST'],xml['nfeProc']['NFe']['infNFe']['det']['prod']['uCom'],xml['nfeProc']['NFe']['infNFe']['det']['prod']['qCom'],xml['nfeProc']['NFe']['infNFe']['det']['prod']['vUnCom'],xml['nfeProc']['NFe']['infNFe']['det']['prod']['vProd'],xml['nfeProc']['NFe']['infNFe']['det']['imposto']['ICMS']['ICMS20']['vICMS'],xml['nfeProc']['NFe']['infNFe']['det']['imposto']['ICMS']['ICMS20']['vBC']]    

                                pass

                            pass

                        pass
                    
                    for c in ['SKU','NFe','Qtde','Valor Unitário','Total dos Produtos','ICMS','Base de Cálculo']:

                        if c in ['SKU','NFe']:

                            df[c]=df[c].astype(int)

                            pass

                        else:

                            df[c]=df[c].astype(float)

                            pass

                        pass

                    df['Data de Emissão']=df['Data de Emissão'].apply(lambda info: str(info).split('T')[0])
                    df['Data de Emissão']=pd.to_datetime(df['Data de Emissão'])

                    user_name=self.xlsx['E-mail'].unique().tolist()[-1]
                    empresa=self.xlsx['Empresa'].unique().tolist()[-1]

                    df['Usuário']=user_name
                    df['Empresa']=empresa
                    
                    df.drop_duplicates(inplace=True)
                    st.dataframe(df,use_container_width=True,hide_index=True)

                    st.button('Salvar',key='btn_save',type='primary')

                    if st.session_state['btn_save']:

                        if len(df)>0:

                            temp_path=os.path.join(self.path_excel,self.excel)
                            arq=glob(temp_path)

                            if len(arq)<=0:

                                df.to_excel(temp_path,sheet_name='XML',index=False)
                                
                                pass

                            else:

                                excel=pd.read_excel(temp_path)
                                lista=df['Chave NFe'].unique().tolist()
                                excel=excel.loc[~excel['Chave NFe'].isin(lista)]
                                
                                excel=pd.concat([excel,df],axis=0,ignore_index=True)
                                excel.to_excel(temp_path,sheet_name='XML',index=False)

                                pass

                            mensagem=st.success('Dados importados com sucesso.')
                            time.sleep(1)
                            mensagem.empty()

                            time.sleep(1)
                            streamlit_js_eval(js_expressions='parent.window.location.reload()')

                            pass

                        pass

                    pass

                pass


            pass


        pass    


    pass