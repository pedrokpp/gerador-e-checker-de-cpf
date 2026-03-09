# Exemplos de Uso - CPF/CNPJ v3.1.0

Esta pasta contém scripts de exemplo demonstrando como usar a biblioteca CPF e CNPJ.

## Scripts Disponíveis

### 1. `cli_modern.py` - Interface CLI CPF (API v3.0)

Script interativo que demonstra a **nova API v3.0** com todos os recursos modernos:

- ✅ Validação com informação de região
- ✅ Geração com região por **nome ou sigla** (ex: "SP", "São Paulo")
- ✅ Formatação configurável (com ou sem pontos/hífen)
- ✅ Validação em lote

**Executar:**
```bash
python examples/cli_modern.py
```

**Recursos demonstrados:**
- `cpf.validate(cpf, show_region=True)` - Validação com região
- `cpf.generate(count, region, formatted)` - Geração flexível
- Suporte a região por nome: "SP", "RJ", "Minas Gerais", etc.
- Opção de formato customizável

---

### 2. `cli_cnpj.py` - Interface CLI CNPJ (API v3.1) ⭐ NOVO

Script interativo que demonstra a **nova API CNPJ v3.1** com todos os recursos:

- ✅ Validação de CNPJ com formatação flexível
- ✅ Geração de matrizes (filial 0001) ou filiais aleatórias
- ✅ Formatação configurável (com ou sem pontos/barra/hífen)
- ✅ Validação em lote

**Executar:**
```bash
python examples/cli_cnpj.py
```

**Recursos demonstrados:**
- `cnpj.validate(cnpj)` - Validação de CNPJ
- `cnpj.generate(count, formatted, matriz_only)` - Geração flexível
- Suporte a matrizes e filiais
- Opção de formato customizável

---

### 3. `cli_legacy.py` - Interface CLI Legada (CPF)

Script que demonstra a **API v2.x** (backward compatibility):

- ✅ Mantém 100% de compatibilidade com código antigo
- ✅ Usa funções `checar()` e `gerar()`
- ✅ Comportamento idêntico à v2.x

**Executar:**
```bash
python examples/cli_legacy.py
```

**Recursos demonstrados:**
- `cpf.checar(cpf, regiao=False)` - API legada de validação
- `cpf.gerar(quantidade, regiao=-1)` - API legada de geração

---

## Exemplos de Código

### Validação de CPF

```python
import cpf

# Validar CPF (aceita formatado ou não)
resultado = cpf.validate("494.351.429-40")
print(resultado)  # True

# Validar com informação de região
resultado = cpf.validate("494.351.429-40", show_region=True)
print(resultado)
# {'valid': True, 'region': 'Paraná – Santa Catarina'}
```

### Validação de CNPJ ⭐ NOVO

```python
import cnpj

# Validar CNPJ (aceita formatado ou não)
resultado = cnpj.validate("11.222.333/0001-81")
print(resultado)  # True

resultado = cnpj.validate("11222333000181")
print(resultado)  # True

# Rejeita CNPJs inválidos
resultado = cnpj.validate("11.111.111/1111-11")
print(resultado)  # False
```

### Geração de CPF com Região

```python
import cpf

# Gerar CPFs de São Paulo (por sigla)
cpfs = cpf.generate(count=5, region="SP")
print(cpfs)
# ['123.456.789-09', '987.654.321-00', ...]

# Gerar CPFs do Rio de Janeiro (por nome)
cpfs = cpf.generate(count=3, region="Rio de Janeiro")
print(cpfs)

# Gerar sem formatação (útil para banco de dados)
cpfs = cpf.generate(count=2, region="SP", formatted=False)
print(cpfs)
# ['12345678909', '98765432100']
```

### Geração de CNPJ ⭐ NOVO

```python
import cnpj

# Gerar CNPJs de matriz (filial 0001)
cnpjs = cnpj.generate(count=5, matriz_only=True)
print(cnpjs)
# ['11.222.333/0001-81', '45.678.901/0001-23', ...]

# Gerar CNPJs com filiais aleatórias
cnpjs = cnpj.generate(count=3, matriz_only=False)
print(cnpjs)
# ['11.222.333/0245-67', '45.678.901/1234-56', ...]

# Gerar sem formatação (útil para banco de dados)
cnpjs = cnpj.generate(count=2, formatted=False)
print(cnpjs)
# ['11222333000181', '45678901000123']
```

### Backward Compatibility

```python
import cpf

# API antiga continua funcionando
valido = cpf.checar("494.351.429-40")
print(valido)  # True

cpfs = cpf.gerar(quantidade=5, regiao=8)  # São Paulo
print(cpfs)
```

---

## Testar os Exemplos

Depois de instalar a biblioteca:

```bash
# Instalar a biblioteca (se ainda não instalou)
pip install cpf

# Ou instalar do código fonte
pip install -e .

# Executar exemplos
python examples/cli_modern.py   # CPF
python examples/cli_cnpj.py     # CNPJ (novo!)
python examples/cli_legacy.py   # CPF legado
```

---

## Criando Seus Próprios Scripts

Use estes exemplos como base para criar suas próprias aplicações:

1. **Aplicações Web**: Use `cpf.validate()`, `cpf.generate()`, `cnpj.validate()` e `cnpj.generate()` em suas APIs
2. **Scripts CLI**: Adapte os exemplos acima
3. **Testes automatizados**: Gere CPFs e CNPJs válidos para seus testes
4. **Formulários**: Valide CPFs e CNPJs em tempo real
5. **Sistemas de cadastro**: Valide documentos brasileiros completos

---

## Mais Informações

- **Documentação completa**: Ver [README.md](../README.md) na raiz do projeto
- **API Reference**: Ver docstrings em `src/cpf/presentation/api.py`
- **Testes**: Ver `tests/` para mais exemplos de uso
