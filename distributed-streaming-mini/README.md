# Distributed Streaming (Mini Demo) — sem Docker, só Python

Este projeto **simula** um sistema de armazenamento distribuído ultra-simples para **mostrar em sala**:

* 3 "nós" locais (servidores estáticos) em portas diferentes;
* **latência simulada** por nó (ex.: 50 ms, 150 ms, 300 ms);
* um script de **replicação** que copia um vídeo para todos os nós;
* um script que **mede** quem responde mais rápido e **abre** o arquivo diretamente do nó mais rápido.

> É didático: não tem autenticação, CDN real, nem replicação inteligente. Mas serve para **explicar conceitos** (latência, replicação, disponibilidade).

---

## 🔧 Requisitos

* Python 3.9+ instalado (Windows/Mac/Linux).
* Não precisa instalar bibliotecas externas.

---

## 📂 Estrutura

```
distributed-streaming-mini/
├─ start_node.py            # inicia um nó (HTTP) com latência simulada
├─ replicate.py             # replica um arquivo local para as pastas dos nós
├─ pick_node_and_open.py    # escolhe o nó mais rápido e abre o arquivo no navegador
├─ nodes.json               # configuração dos nós (portas, pastas, latência)
├─ node1/storage/           # pasta de arquivos do nó 1
├─ node2/storage/           # pasta de arquivos do nó 2
└─ node3/storage/           # pasta de arquivos do nó 3
```

---

## 🚀 Passo a passo (iniciante)

1. **Entre na pasta** `distributed-streaming-mini`.

2. **Inicie os 3 nós** (cada um em uma janela/aba de terminal separada):

```bash
# Nó 1 (mais rápido)
python start_node.py --name node1 --port 8001 --latency-ms 50 --root node1/storage
# Nó 2
python start_node.py --name node2 --port 8002 --latency-ms 150 --root node2/storage
# Nó 3 (mais lento)
python start_node.py --name node3 --port 8003 --latency-ms 300 --root node3/storage
```

Cada janela exibirá logs como:
`GET /meu_video.mp4 (latência simulada: 50 ms, total ~52 ms)`

3. **Replicar um vídeo** (pequeno) do seu computador:

```bash
python replicate.py "C:/caminho/para/demo.mp4"
```

Isso copia o arquivo para:

* `node1/storage/demo.mp4`
* `node2/storage/demo.mp4`
* `node3/storage/demo.mp4`

4. **Abrir automaticamente no nó mais rápido**:

```bash
python pick_node_and_open.py demo.mp4
```

O script mede o tempo de resposta a `/health` e abre `http://localhost:PORT/demo.mp4` no navegador.

---

### 🔗 Alternativa manual

Você pode acessar qualquer nó diretamente no navegador:

* `http://127.0.0.1:8001/demo.mp4`
* `http://127.0.0.1:8002/demo.mp4`
* `http://127.0.0.1:8003/demo.mp4`

➡️ Avance a barra do player: o navegador usa **Range Requests** e o servidor já suporta, simulando **streaming progressivo**.

---

## 🎓 Demonstrações que você pode fazer em sala

* **Latência**: pare o nó 1 (Ctrl+C) e rode o seletor de novo → ele escolherá o nó 2.
* **Disponibilidade**: se um nó cair, o sistema ainda atende pelos outros.
* **Replicação**: troque o arquivo local e rode `replicate.py` → todos os nós recebem a nova versão.
* **Cache/versão**: se o navegador mostrar o antigo, use Ctrl+F5 para forçar reload.

---

## 🛑 Encerrando

Para encerrar, pressione **Ctrl + C** em cada janela onde os nós estão rodando.

---
