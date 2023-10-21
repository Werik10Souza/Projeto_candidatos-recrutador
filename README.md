# Projeto_candidatos/recrutador
  Trabalho Prático de RAD em Python

O programa em Python que cria uma interface gráfica para um formulário de inscrição e uma área para recrutadores gerenciarem candidatos. Aqui está uma explicação simples do que o código faz:

- Ele usa a biblioteca Tkinter para criar uma janela de aplicativo com um formulário de inscrição para candidatos.

- O formulário de inscrição solicita informações, como nome, idade, email, cidade, estado, telefone, LinkedIn, status atual (empregado ou desempregado), habilidades interpessoais, habilidades técnicas, currículo anexado e expectativa salarial.

- Os candidatos preenchem o formulário e podem anexar seu currículo.

- Quando o candidato envia o formulário, as informações são armazenadas em um banco de dados SQLite.

- Há um botão "Área do Recrutador" que permite que os recrutadores acessem uma área onde podem filtrar, visualizar e exportar candidatos em um arquivo CSV.

- Na Área do Recrutador, os recrutadores podem filtrar candidatos com base em critérios como cidade, estado, expectativa salarial, email e telefone.

- Os candidatos filtrados são exibidos em uma tabela com informações, incluindo seu nome, cidade, estado, expectativa salarial, email, telefone e status.

- Os recrutadores podem classificar os candidatos individualmente com tags de status (aprovado, reprovado ou em espera).

- Há um botão para exportar a lista de candidatos filtrados para um arquivo CSV para análise posterior.

- A interface também inclui uma imagem na área direita.

Este código é útil para coletar inscrições de candidatos e ajudar os recrutadores a gerenciar e avaliar os candidatos de forma mais eficaz
