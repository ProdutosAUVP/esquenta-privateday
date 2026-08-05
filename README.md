# 🪩 Esquenta AUVP Private Day

Pista de dança virtual em tempo real para o esquenta do **AUVP Private Day 2026**. Os usuários criam um avatar, dançam numa pista 80s, conversam no chat ao vivo (e no privado), colocam músicas do YouTube na fila do DJ e votam no que toca — tudo sincronizado entre todos os participantes via Firebase.

**App de arquivo único:** todo o HTML, CSS e JavaScript vivem em [`index.htm`](index.htm). Não há build, bundler nem dependências locais — basta servir o arquivo (GitHub Pages, por exemplo).

## ✨ Funcionalidades

### Pista & Avatar
- **Avatar personalizável** (DiceBear Avataaars): cabelo, acessórios, barba, roupas, olhos, sobrancelhas, boca, tom de pele e cores — organizado em seções (**Estilo / Rosto / Cores**), com abas no mobile e painel largo no desktop.
- **Aura colorida** na pista, coroa e brilho VIP para quem já tem ingresso.
- **Pista de dança 80s** com ladrilhos animados, globo refletor pendurado e mesa de DJ com vinis girando e equalizador.
- Clique na pista para mover seu avatar; presença sincronizada em tempo real.

### Música (Fila do DJ)
- Qualquer pessoa cola um link do YouTube e entra na fila.
- **Votação para pular**: o botão "Pular" registra votos; quando a maioria dos online vota, rola uma **contagem regressiva de 5s** e a música troca.
- **Limite de 10 minutos**: todo vídeo é pulado automaticamente ao completar 10 min de reprodução.
- **Playlist da casa (fallback)**: se ninguém está tocando nada, o player reproduz um vídeo aleatório da [playlist oficial](https://youtu.be/yY1881tE4bo?list=PLyMBoXJME_lqvOTGagEL0vh43fSsbpRW1). Quando alguém adiciona uma música, uma contagem regressiva aparece e a música do usuário assume a mesa.
- **🔥 "Essa vai pra festa!"**: botão de voto por música, gravado no Firestore (`partyVotes`) para curadoria do gosto musical da galera para a festa real.
- Avanço automático ao fim de cada vídeo (YouTube IFrame API).

### Chat
- **Chat ao vivo** para todos, com destaque VIP. Mensagens de dias anteriores exibem a data.
- **Chat privado (DM)**: clique no avatar de alguém na pista para abrir uma conversa 1:1, com badge de mensagens não lidas.

### Entrada
- Dois botões no final da personalização:
  - **"Já tenho meu ingresso!"** → entra como VIP (coroa + brilho).
  - **"Não tenho ingresso"** → abre a [página de ingressos](https://privateday.auvp.com.br/#ingressos) e entra como convidado.
- Enquanto o painel de personalização está aberto, o áudio da música fica **abafado** (volume reduzido + desfoque no vídeo — simulação de filtro, já que o YouTube não expõe o áudio do embed ao Web Audio).

## 🚀 Como rodar

1. Sirva o `index.htm` em qualquer host estático (GitHub Pages, Netlify, etc.) — ou abra localmente.
2. O app precisa de internet para: Tailwind CDN, Google Fonts, Firebase, DiceBear e YouTube.
3. As credenciais do Firebase já estão em `FIREBASE_CONFIG_FALLBACK` dentro do `index.htm` (projeto `auvp-privateday`). Para usar outro projeto, veja [docs/deploy.md](docs/deploy.md).

## 📚 Documentação

| Arquivo | Conteúdo |
|---|---|
| [docs/arquitetura.md](docs/arquitetura.md) | Estrutura do código, modelo de dados no Firestore, sincronização (líder, contagem, votos) |
| [docs/funcionalidades.md](docs/funcionalidades.md) | Guia detalhado de cada funcionalidade e como ela funciona por dentro |
| [docs/deploy.md](docs/deploy.md) | Publicação, configuração do Firebase e solução de problemas |
| [CLAUDE.md](CLAUDE.md) | Guia para desenvolvimento com Claude Code neste repositório |

## 🛠 Stack

- **UI**: HTML + [Tailwind CSS (CDN)](https://tailwindcss.com) + CSS custom (animações da pista)
- **Tempo real**: [Firebase](https://firebase.google.com) — Auth anônimo + Firestore (`onSnapshot`)
- **Avatares**: [DiceBear v8 – Avataaars](https://www.dicebear.com)
- **Player**: YouTube IFrame Embed + postMessage API
- **Fontes**: Poppins, Anek Latin e DiscoDiva (display)
