# Arquitetura

## Visão geral

O app é um **cliente Firebase puro**: não existe backend próprio. Cada navegador aberto é um "peer" que lê e escreve no Firestore; a UI de todos converge pelos listeners `onSnapshot`. A autenticação é **anônima** (cada visitante ganha um `uid` efêmero).

```
┌───────────┐   onSnapshot    ┌────────────────────┐
│ Navegador │◄───────────────►│ Firestore          │
│ (index.htm)│  setDoc/addDoc │ artifacts/{appId}/ │
└───────────┘                 │   public/data/…    │
      ▲                       └────────────────────┘
      │ postMessage (IFrame API)
      ▼
┌───────────┐
│  YouTube  │ (player embed + playlist da casa)
└───────────┘
```

## Modelo de dados (Firestore)

Caminho base: `artifacts/{appId}/public/data/…` — `appId = auvp-privateday`.

### `users/{uid}` — presença e perfil
```js
{
  name, color, isVIP,
  avatarConfig: { top, accessories, facialHair, clothing, eyes,
                  eyebrows, mouth, skinColor, hairColor, clothesColor },
  x, y,          // posição na pista (0–100 %)
  lastUpdate     // heartbeat; considerado online se < 120 s
}
```
Heartbeat a cada 30 s (`startHeartbeat`). Usuários sem update há 2 min somem da pista.

### `chat/{autoId}` — chat público
```js
{ uid, name, isVIP, color, text, timestamp }
```
O cliente exibe as últimas 50, ordenadas por `timestamp`. Mensagens de dias anteriores mostram `dd/mm · hh:mm`.

### `dm/{autoId}` — chat privado
```js
{ convId, from, fromName, fromColor, to, text, timestamp }
```
`convId` = os dois uids ordenados e unidos por `_` (ex.: `abc_xyz`). Cada cliente filtra localmente as mensagens em que participa (`from === meuUid || to === meuUid`). Não-lidas: badge no avatar, contadas a partir do início da sessão (`dmSessionStart`) ou da última leitura (`dmReadAt`).

### `queue/{autoId}` — fila do DJ
```js
{ videoId, addedByName, addedByUid, timestamp }
```

### `player/state` — vídeo atual (documento único)
```js
{ videoId, startedAt, addedByName, addedByUid }   // videoId null = playlist da casa
```

### `player/skipVotes` — votação de pular (documento único)
```js
{ videoId, votes: { uid: true, ... } }
```
Só vale se `videoId` bater com o vídeo atual. Resetado (`votes:{}`) a cada troca de música.

### `player/countdown` — contagem regressiva (documento único)
```js
{ endsAt, reason }   // endsAt null = sem contagem
```

### `partyVotes/{videoId_uid}` — curadoria "Essa vai pra festa!"
```js
{ videoId, uid, name, addedByName, timestamp }
```
ID composto garante 1 voto por usuário por vídeo. **Esta coleção é o produto da curadoria — não apagar.** Para exportar: leia a coleção e agrupe por `videoId` (título recuperável via `https://www.youtube.com/oembed?url=...`).

## Mecanismos de sincronização

### Iframe estável + overlay
`renderPlayer()` recria o `<iframe id="ytFrame">` **apenas** quando `videoId`/`startedAt` mudam (chave `lastPlayerKey`). Tudo que muda com frequência (votos, contagem, avisos) é HTML dentro de `#playerOverlay`, atualizado por `updatePlayerOverlay()` — assim o vídeo nunca reinicia por causa de um voto.

### Eleição de líder
Ações automáticas que só podem acontecer **uma vez** (pular aos 10 min, avançar ao fim do vídeo) são executadas apenas pelo cliente cujo `uid` é o **menor** entre os online (`isLeader()`). Os demais ignoram o gatilho. Se o líder cair, o próximo menor uid assume naturalmente no snapshot seguinte de `users`.

### Contagem regressiva
`startCountdown(reason, action)`:
1. Grava `player/countdown = {endsAt: agora+5s, reason}` → todos os clientes exibem o overlay (ticker local de 200 ms atualiza o número).
2. O cliente **que iniciou** agenda `setTimeout(5s)` → executa `action()` (trocar música) e limpa o doc.

Disparada em dois casos: música adicionada enquanto a playlist da casa toca, e votação de pular atingindo o limiar.

### Votação de pular
- Limiar: `max(1, ceil(onlines / 2))` — maioria simples dos presentes.
- Voto: merge no mapa `votes` de `player/skipVotes`; 1 voto por uid, sem retirar voto.
- Quem registra o voto que cruza o limiar inicia a contagem.

### Limite de 10 minutos
Timer local de 5 s em cada cliente compara `Date.now() - startedAt` com `MAX_PLAY_MS`. Ao estourar, o líder chama `playNextVideo()`.

### Fim de vídeo
No `load` do iframe o app envia `{event:'listening'}` (handshake da IFrame API). O YouTube passa a postar eventos; `onStateChange` com `info === 0` (ended) faz o líder avançar a fila. A playlist da casa avança sozinha (embed `videoseries`).

### Playlist da casa (fallback)
Sem `videoId` no `player/state`, cada cliente monta o embed `videoseries?list=…&index=aleatório` **mutado** (autoplay com som é bloqueado pelos navegadores sem interação) com botão "🔊 Ativar som". O fallback é local — não sincronizado entre clientes — o que é aceitável, pois é só ambiente.

### "Filtro" de áudio com o modal aberto
O YouTube não expõe o áudio do embed ao Web Audio (cross-origin), então o efeito de frequências cortadas é **simulado**: `setVolume(10)` via postMessage + `blur/saturate` no iframe. Reaplicado a cada 1,5 s enquanto o modal está aberto (o player pode não estar pronto na primeira tentativa).

## Segurança

- **Escape de HTML**: `esc()` é aplicado a nomes e mensagens antes de qualquer `innerHTML`.
- **Auth anônima + regras públicas**: qualquer visitante pode escrever nas coleções públicas — modelo aceito para um evento efêmero. Não guarde nada sensível nessas coleções.
- A chave de API do Firebase no HTML **não é segredo** (é um identificador de projeto); a proteção real são as regras do Firestore.
