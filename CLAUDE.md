# CLAUDE.md

Guia para trabalhar neste repositório com Claude Code (ou qualquer agente/dev).

## Visão geral

App de página única (**`index.html`**) — pista de dança virtual do esquenta AUVP Private Day. Sem build, sem `package.json`, sem framework: HTML + Tailwind via CDN + um único `<script type="module">` com todo o JavaScript. Documentação em `README.md` e `docs/`.

## Regras do projeto

- **Tudo em um arquivo.** Não crie arquivos JS/CSS separados; mantenha o padrão de arquivo único do `index.html`.
- **Idioma:** todo texto visível ao usuário, comentários e commits em **português (pt-BR)**.
- **Estilo visual:** dark (`#050505`), paleta AUVP — laranja `#DB7944`, azul `#0B2A47`, vermelho `#932621`, creme `#FFF7EB` — com neons 80s (rosa `#ff00cc`, ciano `#00ffff`) apenas em detalhes da pista.
- **Identidade:** sempre que usar o globo da marca, use `GLOBO.png`; para o nome "PRIVATE DAY" (ex.: header), use o lettering `LETTERING.png` — ambos na raiz do repo, por caminho relativo.
- **Tailwind para layout, CSS custom só para animações** (bloco `<style>` no `<head>`).
- **Sem dependências novas** sem necessidade real. CDNs atuais: Tailwind, Google Fonts, Firebase 11.x (gstatic), DiceBear v8, YouTube.

## Arquitetura do JS (ordem dentro do `<script type="module">`)

1. Ícones SVG (`Icons`) e injeção nos `<span id="icon-*">`
2. Config do Firebase (`FIREBASE_CONFIG_FALLBACK` — preencher para hospedar fora do ambiente Claude)
3. Catálogos do avatar (`TOPS`, `EYES`, `AURA_COLORS`, …) e `getAvatarUrl()`
4. Constantes da pista (`FALLBACK_PLAYLIST`, `MAX_PLAY_MS`, `COUNTDOWN_MS`, `TICKETS_URL`) e estado global (`currentVideo`, `queue`, `skipVotes`, `countdownState`, `partyVotes`, `dmMessages`, …)
5. Pista (ladrilhos, mesa de DJ), `iniciarUI()`, auth
6. Helpers `pdoc()`/`pcol()` + listeners `onSnapshot` (users, chat, queue, player, partyVotes, dm)
7. Presença (`updatePresence`, heartbeat de 30 s)
8. Renders: `renderUsers`, `renderChat`, `renderQueue`, `renderPlayer`/`updatePlayerOverlay`, `renderDM`, `renderSettingsModal`
9. Lógica de votos/contagem/limite de 10 min/fim de vídeo/duck de áudio
10. Handlers de formulários e do modal

## Padrões importantes (não quebrar)

- **Iframe estável**: `renderPlayer()` recria o iframe **só quando o vídeo muda** (`lastPlayerKey`); votos/contagem/avisos são desenhados em `#playerOverlay` por `updatePlayerOverlay()`. Nunca redesenhe o iframe em snapshots de votos/usuários, senão o vídeo reinicia para todo mundo.
- **Líder**: ações automáticas (limite de 10 min, avanço ao fim do vídeo) são executadas apenas pelo cliente com **menor uid** entre os online (`isLeader()`), para evitar escrita duplicada.
- **Contagem regressiva sincronizada**: doc `player/countdown` (`{endsAt, reason}`). Quem inicia a contagem executa a ação no `setTimeout`; os demais apenas exibem o overlay (ticker de 200 ms).
- **Escape de HTML**: todo conteúdo vindo de usuário (nomes, mensagens) passa por `esc()` antes de entrar em `innerHTML`.
- **Modo offline**: o app precisa abrir mesmo sem Firebase (`configValida === false` ou falha de auth) — mantenha os guards `if (!currentUser || !db) return;`.
- **Timestamps**: `Date.now()` do cliente (sem serverTimestamp) — comparações toleram pequenos desvios de relógio.
- **WebGL é progressivo**: o Three.js entra por `import()` dinâmico dentro de try/catch; se falhar (CDN bloqueado, sem GPU), o globo 2D `#cssDiscoBall` permanece. Nunca torne o Three.js um import estático — derrubaria o app inteiro.
- **Dados de usuário em animações/classes**: valores como `dance` e `emoji` são validados contra whitelists antes de virarem classe CSS/DOM.
- **Silenciamento é local** (localStorage `esquentaMuted`) e a censura de palavrões acontece **no envio** (`censor()`); não há papel de admin.
- **Perfil persistido no navegador** (localStorage `esquentaProfile`): carregado com merge defensivo na inicialização; `saveProfile()` deve ser chamado em toda mutação de `localProfile`.

## Firestore (caminho base `artifacts/{appId}/public/data/…`)

| Coleção/Doc | Uso |
|---|---|
| `users/{uid}` | presença + perfil (x, y, avatarConfig, color, isVIP, lastUpdate) |
| `chat/{auto}` | chat público |
| `dm/{auto}` | chat privado (`convId` = uids ordenados unidos por `_`) |
| `dmThreads/{convId}` | solicitação de papo (`{a, b, requestedBy, status}`) — DM só abre com `status='accepted'` |
| `queue/{auto}` | fila do DJ |
| `player/state` | vídeo atual (`videoId`, `startedAt`, `addedByUid`, `addedByName`, `title`) |
| `player/skipVotes` | votos de pular (`{videoId, votes:{uid:true}}`) — resetado a cada troca |
| `player/countdown` | contagem regressiva (`{endsAt, reason}`) |
| `player/playback` | sincronia de reprodução (`{videoId, state, time, at}`) — publicado pelo DJ; os demais seguem |
| `partyVotes/{videoId_uid}` | votos "Essa vai pra festa!" (curadoria — nunca apagar) |
| `history/{auto}` | músicas já tocadas (`videoId`, `byUid`, `byName`, `title`) — base do ranking |
| `reactions/{auto}` | reações flutuantes (`uid`, `emoji`, `x`, `y`, `timestamp`) — o líder apaga as com >2 min |

Campos extras no perfil (`users/{uid}`): `dance` (passinho: `''|spin|jump|shake|moonwalk`).

Detalhes em [docs/arquitetura.md](docs/arquitetura.md).

## Testes / verificação

- Sem suíte de testes. Validação mínima após alterações no JS:
  ```bash
  python3 -c "import re;open('/tmp/app.mjs','w').write(re.search(r'<script type=\"module\">(.*?)</script>', open('index.html').read(), re.S).group(1))" && node --check /tmp/app.mjs
  ```
- Teste visual com Playwright/Chromium quando possível. **Atenção:** no sandbox os CDNs (Tailwind/gstatic) podem estar bloqueados pelo proxy — a página abre sem estilo e sem Firebase; isso não é um bug do app.
- Sempre teste os dois viewports: desktop (~1440px) e mobile (~390px). O layout usa `dvh` e breakpoints `md`/`lg`.

## Git

- Branch de trabalho: a informada na tarefa (atual: `claude/private-day-improvements-0vyiga`).
- Commits em português, no padrão `tipo: descrição` (`feat:`, `fix:`, `docs:`, `config:`).
