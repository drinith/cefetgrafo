import math
class Vertice:

    def __init__(self, nome,id=None):
        self.nome=nome
        self.id=id
        self.listaAdj=[]
        self.visitado='branco'
        self.time=0
        self.anterior=None
        self.distancia=0
        self.chave=0
        self.rank=0
        self.aresta=None
  
class Aresta:

    def __init__(self, vertice1,vertice2,peso):
        self.v1=vertice1
        self.v2=vertice2
        self.peso=peso
        self.reAresta=None
  

class Grafo:

    def __init__(self):
        self.fila = []
        self.pilha = []
        self.lista =[]
        self.verticeLista = []
        self.arestaLista =[]
        self.armazenaOrdem = []
        self.time=0
        self.ciclo=0
        self.caminho=[]
        self.matriz=[]
        self.arestaArmazenada=[]

    def carregaListaVerticeCarga(self,path):
        arq = open(path, 'r')
        texto = arq.readlines()
        leVertice = False
        leLigacao = False
        aresta =[]
        i=0
        for linha in texto :
            
            if(linha=='Vertices\n'):
                leVertice=True
                leLigacao = False
                continue
            if(linha=='Ligacoes\n'):
                leVertice=False
                leLigacao = True
                continue
            
            if leVertice:
                self.verticeLista.append(Vertice(linha.replace('\n',''),i))#Preencgendo a lista de vertices
                i+=1
            if leLigacao:
                #posicao 0 da aresta é o nome do vertice
                aresta = linha.replace('\n','').split(" ")
                for v in self.verticeLista:
                    if(aresta[0]==v.nome):
                        for v2 in self.verticeLista:
                             if(aresta[1]==v2.nome):
                                a = Aresta(v,v2,int(aresta[2]))
                                self.arestaLista.append(a)
                                v.listaAdj.append(a)

            if(linha=='Vertices\n'):
                leVertice=True
                leLigacao = False
            if(linha=='Ligacoes\n'):
                leVertice=False
                leLigacao = True
            #For para preencher os vertices
            
        self.count=len(self.verticeLista)       
        arq.close()

    def floyd(self):

        tMatriz = self.verticeLista.__len__()
        matriz=[]
        for i in range(tMatriz):
	        matriz.append( [0] * tMatriz )
        for i in range(tMatriz):
            for j in range (tMatriz):
                if(i==j):
                    matriz[i][j]=0
                else:
                    matriz[i][j]=math.inf
        for v in self.verticeLista:
            for a in v.listaAdj:
                matriz[a.v1.id][a.v2.id]=a.peso
        
        for k in  range(tMatriz):
            for i in range(tMatriz):
                for j in range (tMatriz):
                    if matriz[i][j] > matriz[i][k] + matriz[k][j]:
                        matriz[i][j] = matriz[i][k] + matriz[k][j] 
        
        self.matriz = matriz

    def buscaEmLargura (self,v:Vertice):
        self.initializeSinlgeSource(v)
        v.visitado="cinza"
        v.distancia=0
        v.anterior=None
        self.fila=[]
        self.fila.append(v)
        while self.fila!=[]:
                u = self.fila.pop(0)
                self.armazenaOrdem.append(u)
                for a in u.listaAdj:
                    if a.v2.visitado=="branco":
                        a.v2.visitado="cinza"
                        a.v2.distancia= a.v1.distancia+1
                        a.v2.anterior=a.v1
                        self.fila.append(a.v2)
                u.visitado ="preto"                

    def buscaEmProfundidadePreOrdem(self,v:Vertice):
        
        v.visitado='cinza'
        self.armazenaOrdem.append(v)
        for a in v.listaAdj:
            a.v1.anterior = a.v2
            if a.v2.visitado =="branco":
                a.v2.visitado="cinza"
                a.v2.distancia= a.v1.distancia+1
                a.v2.anterior=v
                self.buscaEmProfundidadePreOrdem(a.v2)
        v.visitado='preto'
            
    def buscaEmProfundidadePosOrdem(self,v:Vertice):
        v.visitado='cinza'
        v.distancia=0
        v.anterior=None
        for a in v.listaAdj:
            if a.v2.visitado =="branco":
                a.v2.distancia= v.distancia+1
                a.v2.anterior=v
                self.buscaEmProfundidadePosOrdem(a.v2)
        self.armazenaOrdem.append(v)
        v.visitado='preto'
      
    def initializeSinlgeSource(self,raiz):
        for cada in self.verticeLista:
            cada.distancia = math.inf
            cada.anterior = None
            cada.visitado ="branco"
            self.fila.append(cada)
        raiz.distancia=0
        return raiz

    def bellmanFord(self,raiz:Vertice):
        self.initializeSinlgeSource(raiz)
        # Acredito que se quisesse chegar em um ponto era só passar a posição do vertice
        for v in self.verticeLista:
            for a in v.listaAdj:
                v.visitado = "cinza" 
                self.relax(a.v1,a.v2,a.peso)
                
             
        for a in self.arestaLista:
            if (a.v2.distancia>a.v1.distancia+a.peso):
                return False
        return True   
   
    def dijkstra(self,raiz:Vertice):
        self.initializeSinlgeSource(raiz)
        
        while self.fila!=[]:
            u = self.extractMin(self.fila)
            self.pilha.append(u)
            for a in u.listaAdj:
                self.relax(a.v1,a.v2,a.peso)
    
    def kruskal(self):
        
        #ordeno as arestas
        arestaOrdem = sorted(self.arestaLista,key=lambda item: item.peso)
        
        count=0
        for v in self.verticeLista:
            v.anterior=v
            v.rank=0

        while(arestaOrdem!=[]):
            a=arestaOrdem.pop(0)

            x=self.find(a.v1)
            y=self.find(a.v2)

            if(x!=y):
                self.arestaArmazenada.append(a)
                self.union(x,y)      
                count+=a.peso
            
        print(count)

    def union(self,xroot,yroot):

        if xroot.rank < yroot.rank: 
            xroot.anterior = yroot 
        elif xroot.rank > yroot.rank: 
            yroot.anterior = xroot 
  
        else : 
            yroot.anterior = xroot 
            xroot.rank += 1
    
    def find(self,vertice:Vertice)->Vertice:

        while vertice==vertice.anterior :
            return vertice
        return self.find(vertice.anterior)

    def prim(self,raiz:Vertice):
        count =0
        posicao =""
        for v in self.verticeLista:
            v.distancia = math.inf
            v.anterior= None
            self.fila.append(v)
        raiz.distancia=0
        while self.fila != []:
            self.fila = sorted(self.fila,key=lambda item: item.distancia)
            u = self.fila.pop(0)
            u.visitado="cinza"
            posicao+=u.nome+"->"
            count+=u.distancia
            for a in u.listaAdj:
                if a.v2.visitado =="branco" and a.peso<a.v2.distancia:
                    a.v2.anterior = u
                    a.v2.distancia = a.peso        
        print("valor "+str(count)) 
        print(posicao)

    def johnson(self, v:Vertice):
        self.initializeSinlgeSource(v)

        if (self.bellmanFord(v)):
            for a in self.arestaLista:
                a.peso =a.peso+a.v1.distancia-a.v2.distancia
            self.dijkstra(v)


    def relax(self,v1,v2,pesoAresta):
        if(v2.visitado=="cinza"):
            self.ciclo+=1           

        if v2.distancia>v1.distancia+pesoAresta:
            v2.distancia=v1.distancia+pesoAresta
            v2.anterior=v1

    def extractMin(self,verticeLista):
        vMenor = verticeLista[0]
        p=0
        for posicao in range(len(verticeLista)-1):
            if vMenor.distancia>verticeLista[posicao].distancia:
                vMenor = verticeLista[posicao]
                p=posicao
        
        return verticeLista.pop(p)
  
    def imprimirVerticesCaminhos(self,vertice:Vertice):

        if(vertice.anterior is not None):
            print('O vertice %s vem de %s'% (vertice.nome,vertice.anterior.nome)) 
            self.imprimirVerticesCaminhos(vertice.anterior)
        else:
            print('O vertice %s não vem de nenhum lugar'% (vertice.nome))
    


    def printArmazenaOrdem(self):
       
        sequencia=" "
        for o in self.armazenaOrdem:
            sequencia = sequencia+"->"+o.nome
        print(sequencia)   

    def caminhoLista (self,inicio:Vertice,fim:Vertice):
       
       if (inicio!=fim):
           self.lista.append(fim)
           self.caminhoLista(inicio,fim.anterior)
       else:
           return self.lista    
    
    def solucaoProblemaProva(self):

        self.pilha.extend(self.verticeLista)

        while self.pilha!=[]:
            
            v = self.pilha.pop(0)

            for a in v.listaAdj:
                a.v2.anterior = v

        vPai = Vertice("pai")
        for v in self.verticeLista:

            if v.anterior==None:
                v.anterior == vPai

    #Agora teria que rodar a busca em profundidade

    def fordFulkerson(self,source:Vertice,sink:Vertice):
        #aqui poderia inicializar mas já uso none nos anteriores
        aReLista=[]
        for a in self.arestaLista:
            aRe = Aresta(a.v2,a.v1,0)
            a.reAresta = aRe
            aReLista.append(aRe)
        self.arestaLista.extend(aReLista)
        max_flow=0
        listaVertice=[]
        #Testar primeiro o BFS
        while self.BFSFord(source,sink):
            self.caminhoLista(source,sink)
            sorted(self.lista,key=lambda item:item.aresta.peso)
            path_flow = self.lista.pop(0).aresta.peso
            
        

    def BFSFord(self,source:Vertice,sink:Vertice):
        
        self.fila.append(source)
        source.visitado='cinza'

        while self.fila!=[]:

            u= self.fila.pop(0)

            for a in u.listaAdj:

                if a.v2.visitado=="branco" and a.peso>0:
                    self.fila.append(a.v2)
                    a.v2.visitado="cinza"
                    a.v2.anterior = u
                    a.v2.aresta =a

        return True if sink.visitado=="cinza" else False        

#Anotações 
# self.fila = sorted(self.fila,key=lambda item: item.distancia)


if __name__=="__main__":

    grafo = Grafo()
    grafo.carregaListaVerticeCarga('carga_aresta.txt')
    #grafo.prim(grafo.verticeLista[2])
    #grafo.kruskal()
    #print (grafo.ciclo)
    grafo.fordFulkerson(grafo.verticeLista[0],grafo.verticeLista[3])
    
 


