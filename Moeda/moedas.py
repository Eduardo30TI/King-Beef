class Moeda:

    def FormatarMoeda(valor):
        a = "{:,.2f}".format(float(valor))
        b = a.replace(',','v')
        c = b.replace('.',',')
        return c.replace('v','.')

        pass

    def Numero(valor):

        a = "{:,.0f}".format(int(valor))
        b = a.replace(',','v')
        c = b.replace('.',',')
        valor=c.replace('v','.')

        return valor

        pass
    
    def Peso(valor):
        
        a = "{:,.3f}".format(float(valor))
        b = a.replace(',','v')
        c = b.replace('.',',')
        return c.replace('v','.')

        pass

    pass