# Exemplos de Uso - CPF v3.0.0

Esta pasta contém scripts de exemplo demonstrando como usar a biblioteca CPF.

## Scripts Disponíveis

### 1. `cli_modern.py` - Interface CLI Moderna (Recomendado)

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

### 2. `cli_legacy.py` - Interface CLI Legada

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

### Validação Simples

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

### Geração com Região por Nome

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
python examples/cli_modern.py
python examples/cli_legacy.py
```

---

## Criando Seus Próprios Scripts

Use estes exemplos como base para criar suas próprias aplicações:

1. **Aplicações Web**: Use `cpf.validate()` e `cpf.generate()` em suas APIs
2. **Scripts CLI**: Adapte os exemplos acima
3. **Testes automatizados**: Gere CPFs válidos para seus testes
4. **Formulários**: Valide CPFs em tempo real

---

## Mais Informações

- **Documentação completa**: Ver [README.md](../README.md) na raiz do projeto
- **API Reference**: Ver docstrings em `src/cpf/presentation/api.py`
- **Testes**: Ver `tests/` para mais exemplos de uso
