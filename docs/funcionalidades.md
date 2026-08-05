# Guia de funcionalidades

## Entrada e personalização

Ao abrir o app, o modal **"Crie seu Avatar"** aparece com a música da casa já tocando abafada ao fundo.

- **Preview + nome** ficam sempre visíveis no topo.
- **Desktop (≥768px)**: painel largo (`max-w-3xl`), todas as seções visíveis, opções quebrando linha (sem scroll horizontal).
- **Mobile**: as opções são divididas em três seções navegáveis por abas no topo do painel:
  - **Estilo** — cabelo/chapéu, acessórios, barba, roupas
  - **Rosto** — olhos, sobrancelhas, boca
  - **Cores** — tom de pele, cor do cabelo, cor da roupa e cor da aura
- **Cor da aura**: paleta com 11 cores (dois tons de laranja — o laranja AUVP `#DB7944` e o neon `#ff6600`).
- **Botões de entrada**:
  - **"Já tenho meu ingresso!"** → entra na festa como VIP (coroa dourada + brilho especial no avatar).
  - **"Não tenho ingresso"** → abre `https://privateday.auvp.com.br/#ingressos` em nova aba e entra como convidado.

Enquanto o modal está aberto, o áudio do player fica abafado (volume ~10% + desfoque no vídeo). Ao entrar, o som volta ao normal.

## Pista de dança

- Clique em qualquer ponto da pista para mover seu avatar (posição sincronizada para todos).
- **Pista WebGL (Three.js)**: globo de espelhos 3D facetado girando, luzes coloridas orbitando, feixes volumétricos e partículas de poeira brilhante — tudo **pulsando numa batida estimada (118 BPM)** quando há música audível. Carregado por import dinâmico; sem WebGL, o globo 2D em CSS permanece.
- Ladrilhos 80s acendem em cores neon aleatórias; luzes de ambiente pulsam nos cantos.
- **Reações rápidas**: barra no canto inferior esquerdo (🔥 ❤️ 👏 🕺 💃 😂). A reação sobe flutuando do seu avatar na tela de todo mundo (coleção `reactions`; o cliente líder apaga reações com mais de 2 min).
- **Passinhos de dança**: botão 🕺 abre o menu de presets — Giro, Pulinho, Quebradinha, Moonwalk (ou Parado). O passinho fica salvo na sua presença e todos veem seu avatar dançando.
- **👑 Área VIP** (canto superior direito): demarcada com corda dourada tracejada. VIPs circulam livremente; não-VIPs que clicam ali recebem um toast com botão direto para a página de ingressos.
- **Mesa de DJ** no canto inferior direito: vinis giram e o equalizador anima quando há música; mostra quem está "na mesa" (dono da música atual). O avatar do DJ é teleportado para a mesa enquanto sua música toca.
- VIPs têm coroa e aura laranja intensa; o DJ atual ganha aura rosa neon e fones.

## Fila do DJ e player

### Adicionar música
Cole um link do YouTube no campo da fila. A música entra no fim da fila com seu nome e o **título resolvido automaticamente** (oEmbed via noembed.com, sem chave de API); o título também aparece numa pílula sobre o player enquanto toca.

- Se a **playlist da casa** estiver tocando (ninguém na mesa), uma **contagem regressiva de 5 segundos** aparece sobre o player ("🎵 Música de Fulano entrando na pista!") e a sua música assume.

### Votar para pular
Quem está com a música tocando vê o botão **"Pular minha vez"** — passa a vez direto (com a contagem de 5 s), sem precisar de votação.

Para os demais, o botão **"Pular (x/y)"** no canto do player:
- `x` = votos atuais, `y` = votos necessários (**maioria dos online**: `ceil(online/2)`, mínimo 1).
- Cada pessoa vota uma vez por música (o botão trava depois do voto).
- Ao atingir o limiar: contagem regressiva de 5 s ("A pista votou: próxima música!") e a música é pulada.
- Os votos zeram a cada troca de música.

### 🔥 "Essa vai pra festa!"
Botão ao lado do "Pular". Um clique = um voto por pessoa por música (fica laranja depois de votar; mostra o total entre parênteses). Os votos ficam gravados **permanentemente** na coleção `partyVotes` do Firestore para a curadoria do setlist da festa real — cada registro guarda o vídeo, quem votou e quem tinha colocado a música.

### Troca automática
- **10 minutos**: qualquer vídeo é pulado automaticamente ao completar 10 min de reprodução.
- **Fim do vídeo**: quando o vídeo termina, a próxima música da fila entra sozinha.
- **Fila vazia**: sem próxima música, o player volta para a **playlist da casa** (vídeo aleatório da playlist oficial do esquenta), mutada com botão "🔊 Ativar som" (regra de autoplay dos navegadores).

## Chat

### Chat ao vivo (público)
- Últimas 50 mensagens, com cor da aura e coroa VIP de cada autor.
- **Balão de fala na pista**: a mensagem enviada aparece por ~6 s num balão sobre o avatar de quem escreveu (limite de 90 caracteres no balão; autores silenciados não geram balão).
- Mensagens do dia mostram só a hora (`14:32`); mensagens de dias anteriores mostram **data e hora** (`03/08 · 14:32`).
- **Censura automática**: palavrões da lista `BANNED_WORDS` são mascarados com asteriscos no envio (chat e DM).
- **Silenciar**: passe o mouse numa mensagem e toque no 🔇 para silenciar o autor (guardado localmente). As mensagens dele viram uma linha discreta "mensagem oculta — toque para reexibir", e DMs/reações dele deixam de aparecer para você.

### Chat privado (DM)
- **Clique no avatar de alguém na pista** para enviar uma **solicitação de papo** (o cursor vira "mãozinha" sobre os avatares).
- A pessoa recebe um **card de solicitação** (canto superior direito) com "Aceitar" / "Recusar". O papo só abre depois do aceite — quem pediu recebe um aviso e o painel abre automaticamente.
- Clicar em alguém que já te pediu papo equivale a aceitar; recusado, um novo clique reenvia a solicitação.
- Painel flutuante com bolhas estilo mensageiro (suas mensagens em laranja, as do outro em cinza).
- Mensagens novas com o painel fechado geram um **badge vermelho** com contagem sobre o avatar da pessoa na pista.
- Só os dois participantes veem a conversa (filtro por `convId` no cliente).
- **Disclaimer** exibido no painel e no card de solicitação: *"A AUVP não se responsabiliza pelas conversas ocorridas em privado nesta plataforma."*

## 🏆 Ranking da noite

Botão **🏆 Ranking** no header abre o painel com dois placares ao vivo:

- **🎧 DJs da noite**: quem mais emplacou músicas na mesa (top 5, contado pela coleção `history` — toda música que começa a tocar gera um registro).
- **🔥 Rumo à festa**: as músicas mais votadas em "Essa vai pra festa!" (top 5, com thumbnail, título e link para o YouTube).

## Responsividade

- Layout usa `100dvh` (estável em navegadores mobile com barra de endereço dinâmica).
- **Desktop/notebook (≥1024px)**: pista à esquerda, chat + fila em coluna fixa à direita.
- **Tablet/celular**: player e pista em cima, chat + fila ocupando ~48% da altura embaixo; painel de DM ancorado à esquerda; modal com abas.
- Header compacto: globo maior à esquerda, "PRIVATE DAY" e "Esquenta 2026" centralizados e colados.
