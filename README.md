# VBP
## 🚀 Aplicação de Análise de Dados

Dashboard web interativo para análise do VBP municipal, desenvolvido a pedido da Controladoria do município de Centenário do Sul-PR.<br>
Base de dados disponibilizada pela Secretaria de Agricultura e Abastecimento.<br>
Dashboard web interativo de análise para dispositivos moveis e computadores.

![vbp](https://user-images.githubusercontent.com/82631808/180009450-61198359-1c1e-47a4-a460-aeef4c9b3054.png)


## 📦 Configuração

### 📋 Pré-requisitos

Crie um ambiente virtual conforme o arquivo de [requerimentos](https://github.com/denisms7/vbp_pmcs/blob/main/requirements.txt)


### 🔧 Instalação

Após a configuração do ambiente virtual basta executar o arquivo app.py e a aplicação estará on-line no link: http://127.0.0.1 não sendo necessário informar a porta pois o mesmo está sendo disponibilizado na porta 80 do servidor, esta porta pode ser alterada na variável port= localizada ao final do arquivo app.py

````
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=False)
````


## 📦 Desenvolvimento

Este e um projeto desenvolvido com embase em Flask então para implementação da aplicação em produção recomendamos utilizar a documentação do próprio Flask: [Deploying to Production](https://flask.palletsprojects.com/en/2.1.x/deploying/)


## 🛠️ Construído com

* [Python](https://www.python.org/) - Linguagem matriz utilizada
* [Pandas](https://pandas.pydata.org/) - Usado para análise de dados
* [Dash](https://plotly.com/dash/) - Framework web daseado em [Flask](https://flask.palletsprojects.com/en/2.1.x/)
* [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) - Framework CSS usado
* [Plotly](https://plotly.com/python/) - Usado para gerar os Graficos



## ✒️ Autores

* **Desenvolvedor** - *Denis Muniz Silva* - [Portfólio](https://denisms7.github.io/portifolio_dms) - [LinkedIn](https://www.linkedin.com/in/denisms/)


## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE.md](https://github.com/denisms7/Supermarket_Sales_01/blob/main/LICENSE) para detalhes.
