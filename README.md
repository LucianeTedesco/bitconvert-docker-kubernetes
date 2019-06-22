# Desenvolvendo uma aplicação utilizando Docker e Kubernetes

## Introdução
- Breve explicação sobre todo o trabalho (propósito, desenvolvimento e conclusões).

---

## Desenvolvimento

#### Nossa aplicação em python:

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

---

## Conclusões
- O projeto funcionou completamente ou parcialmente? Se parcialmente, o que o projeto não faz e por que não foi implementado?
- O que a equipe concluiu? Quais foram as dificuldades?
- Apresente ao menos uma sugestão de trabalho futuro (melhoria).

