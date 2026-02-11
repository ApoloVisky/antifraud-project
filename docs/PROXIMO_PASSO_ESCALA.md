# 🎯 Próximo passo para escalar e profissionalizar

Se você for fazer **apenas uma coisa agora**, faça esta:

## Implementar a camada de confiabilidade do Consumer

Hoje, o maior risco para escala está em:
- gravação contínua em CSV;
- falta de contrato de payload;
- pouca observabilidade operacional.

A melhoria com melhor custo/benefício é transformar o consumer em um serviço resiliente, com persistência em banco e métricas.

---

## Escopo objetivo (MVP de produção)

### 1) Trocar persistência de CSV por PostgreSQL
- Criar tabela `transactions_scored` com índices por `event_time` e `fraud_prediction`.
- Fazer inserts em lote (`batch insert`) a cada N mensagens ou T segundos.
- Manter CSV apenas como fallback local.

### 2) Validar contrato da mensagem
- Definir JSON Schema da transação (campos obrigatórios e tipos).
- Rejeitar mensagens inválidas para um tópico de erro (`transactions-dlq`).

### 3) Melhorar confiabilidade do consumo Kafka
- Configurar `consumer group` e `enable_auto_commit=False`.
- Fazer commit de offset **somente após** persistência com sucesso.
- Implementar retry com backoff exponencial para falhas transitórias.

### 4) Observabilidade mínima
- Expor métricas Prometheus:
  - `messages_consumed_total`
  - `messages_failed_total`
  - `prediction_latency_ms`
  - `db_write_latency_ms`
- Criar logs estruturados JSON com `transaction_id` e `status`.

---

## Resultado esperado

Com esse passo você ganha:
- escalabilidade (sem gargalo de arquivo local),
- rastreabilidade (erros e métricas),
- confiabilidade operacional (offset com semântica correta),
- base pronta para evoluir para Kubernetes/Cloud.

---

## Plano de execução (2 semanas)

### Semana 1
- [ ] Subir PostgreSQL no `docker-compose`.
- [ ] Criar camada de repositório para escrita em banco.
- [ ] Migrar consumer para batch write + commit manual de offset.

### Semana 2
- [ ] Implementar JSON Schema + DLQ.
- [ ] Adicionar métricas Prometheus e logs estruturados.
- [ ] Ajustar dashboard para ler do banco (em vez de CSV).

---

## Definition of Done

- Consumer processa mensagens continuamente sem perda após restart.
- Dashboard continua funcional usando dados persistidos em banco.
- Existe painel com throughput, erro e latência.
- README atualizado com arquitetura nova e instruções de run.
