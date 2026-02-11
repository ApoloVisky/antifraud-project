# 🚀 Roadmap para deixar o projeto mais profissional

Este roadmap está organizado em fases para evoluir o projeto de **demo funcional** para um pipeline mais próximo de produção.

## Fase 1 — Base sólida (rápida)

### 1) Configuração centralizada com variáveis de ambiente
- Criar um arquivo `.env.example` com:
  - `KAFKA_BOOTSTRAP_SERVERS`
  - `KAFKA_TOPIC_TRANSACTIONS`
  - `MODEL_PATH`
  - `STREAM_RESULTS_PATH`
- Evitar strings fixas (`localhost:9092`, caminhos de arquivo) no código.

### 2) Logging estruturado
- Substituir `print` por `logging` com níveis (`INFO`, `WARNING`, `ERROR`).
- Incluir contexto no log (`transaction_id`, status de predição, erro de parsing).

### 3) Qualidade mínima de código
- Adicionar `ruff` + `black` + `isort`.
- Adicionar `pytest` com testes unitários simples:
  - validação de schema de mensagem;
  - teste do carregamento do modelo;
  - teste de predição com payload válido.

### 4) Tratamento de erros e resiliência
- Producer e Consumer com retry/backoff para conexão Kafka.
- No consumer, proteger parse de mensagens inválidas e seguir processando.
- Persistência do offset/estado de consumo com estratégia explícita.

---

## Fase 2 — Dados e Machine Learning

### 5) Feature engineering realista
- Expandir além de `amount`:
  - hora da transação, país, canal, dispositivo, score histórico, etc.
- Normalização e encoding em pipeline do `scikit-learn` (`Pipeline`, `ColumnTransformer`).

### 6) Métricas de ML de verdade
- Reportar `precision`, `recall`, `f1`, `roc_auc`, matriz de confusão.
- Ajustar limiar de decisão para reduzir falso negativo de fraude.

### 7) Versionamento de modelo
- Salvar artefatos com versão (`fraud_model_v1.pkl`) + metadados de treino.
- Registrar dataset de treino, data, features e métricas no build do modelo.

### 8) Detecção de drift
- Monitorar distribuição das features e taxa de fraude ao longo do tempo.
- Criar alerta quando a distribuição em produção divergir da de treino.

---

## Fase 3 — Arquitetura e operação

### 9) Persistência adequada
- Em vez de CSV em loop, usar banco/OLAP:
  - PostgreSQL (transacional)
  - ClickHouse/BigQuery (analítico)
- CSV pode continuar apenas para modo demo/local.

### 10) Contrato de dados
- Definir schema versionado (JSON Schema/Avro).
- Validar mensagens no producer e consumer.

### 11) Observabilidade
- Expor métricas com Prometheus (ex.: throughput, latência, taxa de erro).
- Criar dashboard operacional (Grafana) além do dashboard de negócio.

### 12) Segurança e compliance
- Sanitização de dados sensíveis.
- Criptografia em trânsito e em repouso quando aplicável.
- Controle de acesso para tópicos Kafka e serviços.

---

## Fase 4 — Produto e experiência

### 13) Dashboard mais executivo
- KPIs por janela de tempo (5m/1h/24h).
- Filtros por faixa de valor, canal, região.
- Série temporal da taxa de fraude e alertas visuais.

### 14) API para integrações
- Criar API (FastAPI) para consultar transações e predições.
- Endpoint de healthcheck e status do modelo em produção.

### 15) CI/CD
- Pipeline com lint + testes + build docker + verificação de segurança.
- Deploy automatizado para ambiente de staging.

---

## Recomendação prática: o próximo passo

Se você quiser começar agora com o maior impacto para escalar com qualidade, siga este plano objetivo:

- [Próximo passo de escala (plano de 2 semanas)](PROXIMO_PASSO_ESCALA.md)

---

## Backlog priorizado (ordem sugerida)

1. Config por `.env` + logging estruturado.
2. Testes básicos com `pytest`.
3. Contrato de dados + validação de payload.
4. Métricas de ML e versão de modelo.
5. Persistência em banco + dashboard temporal.
6. Observabilidade (Prometheus/Grafana) + alertas.

---

## Critérios de pronto (Definition of Done) para cada melhoria

- Código com lint/format aprovados.
- Testes automatizados cobrindo o caso principal.
- Documentação atualizada no `readme.md`.
- Evidência de execução (log, print de tela ou métrica).
