# Deploy e configuração

## Publicação

O app é um único arquivo estático (`index.html`). Qualquer host serve:

- **GitHub Pages** (recomendado): Settings → Pages → Deploy from branch → branch principal, pasta `/`. O arquivo `index.html` é servido como raiz.
- Netlify/Vercel/Cloudflare Pages: arraste o arquivo ou aponte para o repositório.

Requisitos do ambiente do visitante: internet liberada para `cdn.tailwindcss.com`, `fonts.googleapis.com`, `www.gstatic.com` (Firebase), `api.dicebear.com`, `raw.githubusercontent.com` (fonte DiscoDiva), `img.youtube.com`, `www.youtube.com`, `cdn.jsdelivr.net` (Three.js — opcional, com fallback 2D) e `noembed.com` (títulos — opcional).

**Identidade visual**: o globo da marca é o arquivo local `GLOBO.png` e o nome "PRIVATE DAY" usa o lettering `LETTERING.png` (ambos na raiz do repositório, referenciados por caminho relativo — sirva os três arquivos juntos).

## Firebase

O projeto usa **Auth anônimo** + **Firestore**. As credenciais ficam no bloco `FIREBASE_CONFIG_FALLBACK` do `index.html` (hoje apontando para o projeto `auvp-privateday`). A chave de API do Firebase não é secreta — a segurança vem das regras do Firestore.

### Usar outro projeto Firebase

1. Crie um projeto em [console.firebase.google.com](https://console.firebase.google.com).
2. Ative **Authentication → Sign-in method → Anonymous**.
3. Crie um banco **Firestore** (modo produção).
4. Publique regras liberando o caminho público do app:
   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /artifacts/{appId}/public/data/{document=**} {
         allow read, write: if request.auth != null;
       }
     }
   }
   ```
5. Copie o config (Configurações do projeto → Seus apps → Web) para `FIREBASE_CONFIG_FALLBACK` e ajuste `APP_ID_FALLBACK` para o `projectId`.

### Moderação / manutenção dos dados

Operações úteis direto no console do Firestore (`artifacts/{appId}/public/data/…`):

- **Limpar o chat**: apague os documentos da coleção `chat` (e `dm`, se quiser zerar os privados).
- **Destravar o player**: apague ou edite `player/state` (defina `videoId: null`).
- **Zerar votação de pular**: apague `player/skipVotes`.
- **Zerar ranking**: apague os documentos da coleção `history` (as reações em `reactions` se limpam sozinhas — o cliente líder apaga as antigas).
- **Exportar curadoria**: exporte a coleção `partyVotes`; agrupe por `videoId`. O título de cada vídeo pode ser resolvido via `https://www.youtube.com/oembed?url=https://youtu.be/{videoId}&format=json`.

Também dá para automatizar via REST (auth anônima + Firestore REST API) — foi assim que o chat foi limpo em 05/08/2026.

## Parâmetros ajustáveis (constantes no `index.html`)

| Constante | Padrão | Efeito |
|---|---|---|
| `FALLBACK_PLAYLIST` | `PLyMBoXJME_lqvOTGagEL0vh43fSsbpRW1` | Playlist da casa quando ninguém está tocando |
| `MAX_PLAY_MS` | `600000` (10 min) | Tempo máximo de reprodução por vídeo |
| `COUNTDOWN_MS` | `5000` | Duração da contagem regressiva de troca |
| `TICKETS_URL` | `https://privateday.auvp.com.br/#ingressos` | Destino do botão "Não tenho ingresso" e do toast da Área VIP |
| `DJ_X` / `DJ_Y` | `89` / `78` | Posição (%) do DJ na pista |
| `VIP_ZONE` | `{x1:72, y1:5, x2:98, y2:32}` | Retângulo (%) da Área VIP na pista |
| `BANNED_WORDS` | lista em pt-BR | Palavras censuradas no chat/DM |
| `BPM` (bloco WebGL) | `118` | Batida estimada do pulso visual da pista 3D |

## Solução de problemas

| Sintoma | Causa provável | Correção |
|---|---|---|
| Tela "Firebase não configurado" | `FIREBASE_CONFIG_FALLBACK` vazio | Preencher config (acima) |
| Loading trava e abre sem conexão após 10 s | Sem rede até o Firebase / auth falhou | Verificar regras, Auth anônimo ativado e rede |
| Playlist da casa muda mas sem som | Política de autoplay do navegador | Comportamento esperado — o visitante clica em "🔊 Ativar som" |
| Vídeo reinicia para todos ao votar | Regressão: iframe sendo recriado no overlay | Manter o padrão `renderPlayer`/`updatePlayerOverlay` (ver CLAUDE.md) |
| Música não pula aos 10 min com a aba fechada | Só clientes abertos executam ações (não há backend) | Esperado — precisa de ao menos 1 participante online |
