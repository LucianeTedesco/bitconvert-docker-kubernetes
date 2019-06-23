# Desenvolvendo uma aplicação utilizando Docker e Kubernetes

## Introdução
O propósito deste trabalho é construir uma simples aplicação em Python, que será dividida em dois containers: um para o serviço que obtém o valor do bitcoin, e outro para o serviço que obtém a cotação do dolar. A divisão é para evidenciar comunicação entre containers. Será disponibilizada a imagem dos dois serviços no Docker Hub, e será feita a orquestração dos containers com Kubernetes.

## Desenvolvimento

#### Nossa aplicação em python:
Como o projeto tem seu foco principal no uso do docker e kubernates, contamos apenas com uma simples aplicação em python que irá calcular o preço da moeda Bitcoin em reais.  
O calculo é feito por meio de dois serviços. Um deles, é responsável por obter a cotação do dólar no site dolarhoje.com. Para isso usamos as bibliotecas requests e beautifulsoup além do Flask. A primeira é utilizada para se criar uma requisição ao site dolarhoje, então com o beautifulsoup extraimos o conteúdo html dessa request e procuramos pelo input de id 'nacional', que contém o valor do dólar.    
**Realizando requisição:**
```python
req = requests.get('https://www.dolarhoje.com/')
```
**Extraindo conteúdo com beautifulsoup:**
```python
soup = BeautifulSoup(content, 'html.parser')
valorDolarReal = soup.find(name='input', attrs={'id': 'nacional'})
```
O outro serviço fica com a responsabilidade de buscar o preço da bitcoin em dólar. Para isso utilizamos apenas a biblioteca requests, pois o valor virá de uma API.  
**Realizando requisição:**
```python
response = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/')
```
**Obtendo valor do bitcoindo objeto JSON retornado pela API**
```python
valorBitcoin = response.json()[0].get('price_usd')
```
Ainda no primeiro serviço, contamos com um segundo endpoint que é responsável por fazer o calculo do preço da bitcoin em reais. Esse endpoint chamará o primeiro endpoint desse serviço e o end point do segundo serviço para fazer o calculo do preço e retornar em um JSON.  
**Exemplo JSON de retorno**
```JSON
{"valor":"40720.06"}
```
#### Utilizando Docker em nosso projeto: 
O Docker nada mais é do que uma plataforma para desenvolvedores e administradores de sistemas desenvolverem, implementarem e executarem aplicativos com container.  
Um container é uma instância de uma imagem. Uma imagem é um pacote executável que inclui tudo o que é necessário para executar um programa (código, bibliotecas, variáveis de ambiente, arquivos de configurações e etc.) 

**Preparando o ambiente:** 
Neste passo-a-passo, será visto como instalar o Docker no Ubuntu. Todos os comandos listados devem ser executados no seu terminal. 

1. Remover possíveis versões antigas do Docker: 
```sh
sudo apt-get remove docker docker-engine docker.io 
```
2. Atualizar o banco de dados de pacotes: 
```sh
sudo apt-get update 
```
3. Adicionar ao sistema a chave GPG oficial do repositório Docker: 
```sh
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - 
```
4. Adicionar o repositório do Docker às fontes do APT: 
```sh
sudo add-apt-repository \ 
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu\ 
  $(lsb_release -cs) \ 
  stable" 
```
5. Atualizar o banco de dados de pacotes, para ter acesso aos pacotes do Docker a partir do novo repositório adicionado: 
```sh
sudo apt-get update 
```
6. Por fim, instale o pacote Docker-ce: 
```sh
sudo apt-get install docker-ce 
```
7. Para verificar se o Docker foi instalado corretamente verificando a sua versão: 
```sh
sudo docker version 
```

**Criando a nossa imagem:**
No nosso projeto, devemos criar o arquivo Dockerfile, que nada mais é do que um arquivo de texto. Ele pode ter qualquer nome, porém nesse caso ele também deve possuir a extensão `.dockerfile`. 
Abaixo é mostrado o dockerfile criado para o projeto bitcoin.

```dockerfile
#Utiliza a imagem do python, versão 3.7.3 e a imagem da Alpine Linux na versão 3.9 
FROM python:3.7.3-alpine3.9 
#Copia o conteúdo do nosso diretório atual para o diretório do container especificado 
COPY . /server/ 
#Define o diretório de trabalho 
WORKDIR /server/ 
#Instala todo os pacotes necessários especificados no arquivo requirements.txt. 
RUN pip install -r requirements.txt 
#Executa os comandos abaixo assim que o container for iniciado 
ENTRYPOINT ["python", "app.py"] 
```

**Build da nossa imagem:**
Para criar a imagem, precisamos fazer o seu build através do comando `docker build`, comando utilizado para buildar uma imagem a partir de um dockerfile.  

Como o comando abaixo será executado dentro da pasta do projeto, podemos utilizar o ponto ( `.` ) para indicar onde está o arquivo dockerfile. Além disso, passamos a tag da imagem, o seu nome, através da flag `-t`, seguido de dois pontos ( `:` ) e sua versão. 

```sh
docker build . -t luciane/bitcoin:1.0
```

**Compartilhando a imagem no Docker Hub:**
Já criamos a imagem, mas por enquanto ela só está na nossa máquina local. Para disponibilizar a imagem para outras pessoas, precisamos enviá-la para o Docker Hub. 
O primeiro passo é criar a nossa conta. Com ela criada, no terminal nós executamos o comando `docker login` e digitamos o nosso login e senha que acabamos de criar. 
Após isso, basta executar o comando `docker push`, passando a imagem que queremos subir, por exemplo: 
```sh
docker push luciane/bitcoin:1.0 
```
Por fim, ao acessar a nossa conta do Docker Hub, podemos ver que a imagem está lá. Para baixá-la, podemos utilizar o comando `docker pull`: 
```sh
docker pull luciane/bitcoin:1.0 
```
Esse comando somente baixa a imagem, sem criar nenhum container acima dela. 

#### Utilizando Kubernetes em nosso projeto: 
Para gerenciar nossa aplicação utilizamos o Kubernetes que é um software que nos permite implantar, dimensionar e gerenciar conteiners em um cluster. 

**Preparando o ambiente:**
Neste passo-a-passo, será visto como configurar o Kubernetes localmente com a plataforma Minikube. Todos os comandos listados devem ser executados no seu terminal. 

Como o Minikube utiliza um ambiente virtualizado, é necessário instalar o VirtualBox.  
1. No Ubuntu, podemos utilizar o Ubuntu Software para realizar o download. Pesquise por VirtualBox, deverá aparecer a opção de instalação e posteriormente clique no botão Instalar.

Uma vez que a instalação do VirtualBox foi realizada, será necessário realizar a instalação do Minikube, seguem os passos de instalação: 

2. Abrir o terminal e digitar o seguinte comando: 
```sh
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && sudo chmod +x minikube && sudo mv minikube /usr/local/bin/ 
```
Para realizarmos a comunicação com o cluster gerenciado pelo Kubernetes, devemos instalar o kubectl, seguem os passos de instalação: 

3. Abrir o terminal e digitar o seguinte comando: 
```sh
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl 
```
4. Na sequência, devemos mudar a permissão para executável: 
```sh
chmod +x ./kubectl  
```
5. Por fim, devemos mover o kubectl para as variáveis de ambiente: 
```sh
sudo mv ./kubectl /usr/local/bin/kubectl 
```
Após a instalação e inicialização do Minikube na máquina local, será criado um ambiente virtualizado (VM), em que haverá o cluster, a máquina Mestre - que estará recebendo as configurações do arquivo YML - e a máquina Python, a receber a implementação dos containers que formam a aplicação. 

**Criando os arquivos de configuração:**
Como não existe um objeto container no Kubernetes, utilizamos o menor objeto existente, o *Pod*, que além disto é o mais básico, portanto não adiciona a camada de estado desejado da nossa aplicação para o Kubernetes gerenciar.

Ou seja, é necessário colocar o objeto Pod em outro, o *Deployment*, a partir de então, o Kubernetes saberá que sempre queremos ter um pod rodando em nosso cluster.

Abaixo é mostrado o Deployment criado para o projeto bitcoin.
```yml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: bitcoin
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: bitcoin
    spec:
      containers:
        - name: bitcoin
          image: luciane/bitcoin:1.0
          ports:
            - containerPort: 5000
```
Feito isto, voltaremos ao terminal e inicializaremos o minikube. 
```sh
 minikube start 
```
Como queremos que seja criado o Deployment especificado  em nosso cluster, digitaremos: 
```sh
kubectl create -f bitconvert_deployment.yml 
```
Para verificar se o Pod está realmente sendo executado:
```sh
kubectl get pods
```
Veremos que o pod denominado "bitcoin", está com status "Running", isto é, está rodando perfeitamente.
Caso ocorra algum problema que impeça o funcionamento do Pod, esperamos que o Kubernetes tome alguma ação para reverter a situação. Para isso iremos remover um dos pods:
```sh
kubectl delete pods bitcoin-555bd7fbb8-9vqmx
```
Como no nosso arquivo está configurado para sempre existir dois pod, `replicas: 2`, o Kubernetes percebe o estado atual e cria um novo pod. Podemos verificar através do comando:
```sh
kubectl get pods
```
Isto demonstra que garantimos o gerenciamento por parte do Kubernetes, que criou um novo pod denominado `bitcoin-65f867f7dd-27cxd` para substituir aquele que foi removido.

No entanto, os objetos Pod estão em constante alteração: é possível aumentar ou diminuir sua quantidade, ou que sejam encerrados por algum problema e, no caso, o Kubernetes precisará criar um novo objeto para substituí-los, o que ocasionará em um novo endereço IP.

Por conta disto, não conseguimos acessar os novos objetos Pod diretamente, sendo necessário abstrair o acesso a eles em um objeto *Service*.

A ideia é que ele faça a abstração do acesso para os objetos Pod. Podemos configurá-lo para que ele atue como se fosse um balanceador de cargas, dividindo a quantidade de acessos e requisições que nossa aplicação terá, por estes pods que criamos.

Abaixo é mostrado o Service criado para o projeto bitcoin.
```yml
apiVersion: v1
kind: Service
metadata:
  name: bitcoin
spec:
  selector:
    app: bitcoin
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```
Acima, é especificado que Service precisará acessar uma porta de comunicação da nossa aplicação, a 80, que se comunica com a porta 5000 do nosso Pod, e que é necessário estabelecer um vínculo entre o objeto Service e o Pod através do `selector`, 
Como queremos que seja criado o Service especificado, digitaremos: 
```sh
kubectl create -f bitconvert_service.yml 
```
Para visualizar o status do cluster podemos acessar o painel administrativo, através do comando:
```sh
minikube dashboard
```

## Conclusões
Começamos com a aplicação em python, cujas tarefas dividimos em containers, e disponibilizamos as imagens no Docker Hub.
Feito isso, instalamos o minikube para utilizar o gerenciamento desejado do Kubernetes em nossa aplicação. No entando, o Kubernetes não possui um objeto denominado "Container", tivemos que criar o objeto Deployment. Nele informamos que sempre deve existir dois pods. Deletamos um dos pods e, assim, conseguimos evidenciar a criação de outro, conforme desejado.
Vimos que os pods são muito instáveis, por isso, não conseguimos acessar um pod diretamente. Para solucionar esse problema foi criado o objeto Service. Nele definimos também o balanciamento entre os pods existentes.
O projeto funcionou conforme o desejado, não apresentando dificuldades. Uma sugestão de trabalho futuro é configurar o cluster no Goolge Cloud.

