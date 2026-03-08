# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [3.0.1] - 2026-03-08

### 🔧 Modificado

- Atualizado email do autor de `pedrokp@protonmail.com` para `pedrkp@proton.me`
- Atualizado em todos os metadados do pacote (pyproject.toml, __init__.py, README.md)

Sem mudanças funcionais em relação à v3.0.0.

---

## [3.0.0] - 2026-03-08

### 🎉 Versão Principal - Refatoração Completa

Esta é uma versão major com refatoração completa do código, mas mantém 100% de **compatibilidade com a API da versão 2.x**.

### ✅ Corrigido

- **[Issue #2]** **CRÍTICO**: Corrigido algoritmo de validação que rejeitava CPFs válidos incorretamente
  - O algoritmo anterior apenas somava os dígitos e comparava os dois primeiros caracteres da soma
  - Implementado o algoritmo **módulo 11 oficial** usado pela Receita Federal
  - CPFs que agora são validados corretamente:
    - `494.351.429-40` (49435142940)
    - `654.926.122-80` (65492612280)
    - `132.923.016-70` (13292301670)
    - `918.758.814-50` (91875881450)
  - Validação correta de CPFs com todos os dígitos iguais (ex: 111.111.111-11 → inválido)

- **[Issue #1]** Migrado de `setup.py` para `pyproject.toml` (PEP 517/518)
  - Resolve avisos de deprecação do pip 23.1+
  - Usa `hatchling` como build backend moderno
  - Instalação mais rápida e confiável

### 🆕 Adicionado

#### Nova API Moderna

- **`validate(cpf, show_region=False)`**: Nova função de validação
  - Aceita CPFs formatados ou não formatados
  - Opção de retornar informações da região
  - Type hints completos
  
- **`generate(count=1, region=None, formatted=True)`**: Nova função de geração
  - Parâmetro `count`: quantidade de CPFs a gerar
  - Parâmetro `region`: suporta **número** (0-9), **nome do estado** ou **sigla** 
  - Parâmetro `formatted`: escolha entre formato `XXX.XXX.XXX-XX` ou `XXXXXXXXXXX`
  - Exemplos:
    ```python
    cpf.generate(count=5, region="SP")
    cpf.generate(count=3, region=8)
    cpf.generate(count=10, region="São Paulo")
    cpf.generate(count=2, formatted=False)
    ```

#### Recursos Adicionais

- **Região por nome/sigla**: Aceita nomes de estados em português
  - Exemplos: "SP", "São Paulo", "rio de janeiro", "RJ", "Minas Gerais"
  - Case-insensitive
  - Suporta com e sem acentuação

- **Formatação configurável**: Escolha o formato de saída dos CPFs gerados
  - `formatted=True`: retorna `XXX.XXX.XXX-XX` (padrão)
  - `formatted=False`: retorna `XXXXXXXXXXX` (útil para bancos de dados)

- **Type hints completos**: Toda a API é tipada para melhor suporte de IDE e type checkers

#### Qualidade de Código

- **97% de test coverage** com pytest
- **112 testes** (unitários e de integração)
- **Testes específicos para issue #2** (garantia de não regressão)
- **Clean Architecture**: Código organizado em 4 camadas
  - Domain (entidades e regras de negócio)
  - Application (casos de uso)
  - Infrastructure (implementações concretas)
  - Presentation (API pública)
- **Princípios SOLID** aplicados em toda a codebase
- **Documentação completa** com docstrings e type hints

### ♻️ Modificado

- **Algoritmo de geração otimizado**: 
  - Anterior: Gerava números aleatórios e testava até encontrar válidos (ineficiente)
  - Novo: Gera 9 dígitos base e calcula os dígitos verificadores (sempre válido na primeira tentativa)
  - Performance: ~100x mais rápido para grandes quantidades

- **Estrutura de diretórios**: Migrado para layout `src/` (PEP 420)
  ```
  src/cpf/
  ├── domain/
  ├── application/
  ├── infrastructure/
  └── presentation/
  ```

- **Suporte a Python**: Agora suporta Python 3.8, 3.9, 3.10, 3.11, 3.12
  - Removido suporte para Python 2.x e 3.7

- **Cross-platform**: Classifiers atualizados para Windows, Linux e macOS

### 🔄 Compatibilidade Mantida

As funções antigas continuam funcionando exatamente como na v2.x:

- **`checar(cpf="", regiao=False)`**: Mantido 100% compatível
  - Agora usa o algoritmo correto internamente
  - Comportamento idêntico (incluindo `input()` se CPF não fornecido)
  
- **`gerar(quantidade=1, regiao=-1)`**: Mantido 100% compatível  
  - Sempre retorna CPFs formatados (comportamento original)
  - Aceita região como número (0-9 ou -1 para aleatório)

**Nenhum código existente será quebrado ao atualizar para v3.0!**

### 🗑️ Deprecated

Embora mantidas por compatibilidade, recomendamos migrar para a nova API:
- `checar()` → use `validate()`
- `gerar()` → use `generate()`

### 📚 Documentação

- README.md completamente reescrito com exemplos modernos
- Adicionado este CHANGELOG.md
- Docstrings completas em todas as funções públicas
- Exemplos de código atualizados

### 🏗️ Desenvolvimento

- Configurado `pyproject.toml` com todas as ferramentas de dev
- Adicionado suporte para pytest, mypy, ruff, black
- Configuração de coverage mínimo de 95%
- Estrutura de testes organizada (unit/ e integration/)

---

## [2.1] - 2021-01-20

### Adicionado
- Publicado como package no PyPI

### Modificado
- Melhorias gerais na documentação

---

## [2.0] - 2021-01-20

### Adicionado
- Primeira versão publicada como package Python
- Funções `checar()` e `gerar()`
- Suporte a regiões
- Formatação de CPF

---

## Tipos de Mudanças

- `Adicionado` para novos recursos
- `Modificado` para mudanças em recursos existentes
- `Deprecated` para recursos que serão removidos
- `Removido` para recursos removidos
- `Corrigido` para correções de bugs
- `Segurança` para vulnerabilidades

[3.0.0]: https://github.com/pedrokpp/gerador-e-checker-de-cpf/compare/v2.1...v3.0.0
[2.1]: https://github.com/pedrokpp/gerador-e-checker-de-cpf/releases/tag/v2.1
[2.0]: https://github.com/pedrokpp/gerador-e-checker-de-cpf/releases/tag/v2.0
