# Guia de funcionalidades

## Entrada e personalização

No **primeiro acesso**, o modal **"Crie seu Avatar"** aparece com a música da casa já tocando abafada ao fundo — e o boneco já vem com um **visual sorteado** (cabelo, roupa, rosto, tom de pele e cor da aura): ninguém entra na pista com o mesmo avatar padrão. O sorteio evita rostos tristes/enjoados e coloca acessório e barba só de vez em quando.

Quem **já personalizou antes vai direto para a pista** — sem modal na cara de novo. O visual, o nome e o status de ingresso da última visita são reaproveitados, e um toast de boas-vindas lembra que o botão do avatar no header reabre a personalização.

- **Preview + nome** ficam sempre visíveis no topo, com o botão **🎲 Aleatório** logo abaixo do preview para sortear outro visual completo a qualquer momento.
- Cada opção de estilo é um **card com a imagem do avatar** usando aquela opção (miniaturas geradas pelo DiceBear) — nada de escolher só pelo texto.
- **Uma linha por categoria**: cada catálogo (cabelo, roupas, olhos, cores…) fica numa faixa única, navegável por **scroll lateral** — no desktop e no mobile. O painel não estica em altura por causa de uma categoria grande.
- **Mobile**: as opções são divididas em três seções navegáveis por abas no topo do painel:
  - **Estilo** — cabelo/chapéu, acessórios, barba, roupas
  - **Rosto** — olhos, sobrancelhas, boca
  - **Cores** — tom de pele, cor do cabelo, cor da roupa e cor da aura
- **Cor da aura**: paleta com 11 cores (dois tons de laranja — o laranja AUVP `#DB7944` e o neon `#ff6600`).
- **Botões de entrada**:
  - **"Já tenho meu ingresso!"** → entra na festa como VIP (coroa dourada + brilho especial no avatar).
  - **"Não tenho ingresso"** → abre `https://privateday.auvp.com.br/#ingressos` em nova aba e entra como convidado.

Enquanto o modal está aberto, o áudio do player fica abafado (volume ~10% + desfoque no vídeo). Ao entrar, o som volta ao normal.

**Perfil salvo no navegador**: nome, avatar completo, cor da aura, passinho e status de ingresso ficam no `localStorage` (`esquentaProfile`) — na próxima visita tudo volta como estava. Uma segunda chave (`esquentaPerfilPronto`) marca quem já concluiu a personalização e é o que dispensa o modal nas visitas seguintes.

## Pista de dança

- Ao entrar, cada pessoa surge num **ponto aleatório** da pista (fora da Área VIP e da cabine do DJ) — nada de aglomeração no centro.
- Clique em qualquer ponto da pista para mover seu avatar (posição sincronizada para todos).
- **Pista WebGL (Three.js)**: globo de espelhos 3D facetado girando, luzes coloridas orbitando, feixes volumétricos e partículas de poeira brilhante — tudo **pulsando numa batida estimada (118 BPM)** quando há música audível. Carregado por import dinâmico; sem WebGL, o globo 2D em CSS permanece.
- Ladrilhos 80s acendem em cores neon aleatórias; luzes de ambiente pulsam nos cantos.
- **Reações rápidas**: barra no canto inferior esquerdo (🔥 ❤️ 👏 🕺 💃 😂). A reação sobe flutuando do seu avatar na tela de todo mundo (coleção `reactions`; o cliente líder apaga reações com mais de 2 min).
- **Passinhos de dança**: botão 🕺 abre o menu de presets — Giro, Pulinho, Quebradinha, Moonwalk (ou Parado). O passinho fica salvo na sua presença e todos veem seu avatar dançando.
- **👑 Área VIP** (canto superior direito): demarcada com corda dourada tracejada. VIPs circulam livremente; não-VIPs que clicam ali recebem um toast com botão direto para a página de ingressos. Quem está **dentro do lounge** ganha regalias:
  - **Reações exclusivas douradas** (🥂 💎 👑 ✨) numa barra própria, com brilho dourado ao flutuar — só funcionam com o avatar dentro da área.
  - **Destaque visual**: taça 🥂 e aura dourada extra no avatar, visíveis para toda a pista.
  - **Privacidade do lounge**: quem está na área só recebe solicitações e mensagens privadas de quem **também** está lá dentro — de fora, o clique mostra um aviso (com link para comprar ingresso, se a pessoa não for VIP).
- **Mesa de DJ** no canto inferior direito: vinis giram e o equalizador anima quando há música; mostra quem está "na mesa" (dono da música atual). O avatar do DJ é teleportado para a mesa enquanto sua música toca.
- VIPs têm coroa e aura laranja intensa; o DJ atual ganha aura rosa neon e fones.

## Fila do DJ e player

### Adicionar música
Cole um link do YouTube no campo da fila. A música entra no fim da fila com seu nome e o **título resolvido automaticamente** (oEmbed via noembed.com, sem chave de API); o título também aparece numa pílula sobre o player enquanto toca.

**Para tocar, é preciso estar na pista**: a fila vive no Firestore e recarregar a página **não** custa o lugar (a volta acontece dentro da tolerância de ausência). Mas quem fecha o app, minimiza ou troca de aba por mais de ~45 s sai da pista e **perde a vez**: a música é removida da fila pelo cliente líder. Enquanto isso, a música aparece na lista marcada com **"· fora da pista ⚠️"** — o aviso some assim que a pessoa volta.

- Se a **playlist da casa** estiver tocando (ninguém na mesa), uma **contagem regressiva de 5 segundos** aparece sobre o player ("🎵 Música de Fulano entrando na pista!") e a sua música assume.

### Votar para pular
Quem está com a música tocando vê o botão **"Pular minha vez"** — passa a vez direto (com a contagem de 5 s), sem precisar de votação.

Para os demais, o botão **"Pular (x/y)"** no canto do player:
- `x` = votos atuais, `y` = votos necessários: **50%+1 dos presentes ou 10 votos**, o que for menor (mínimo 1).
- Cada pessoa vota uma vez por música (o botão trava depois do voto).
- Ao atingir o limiar: contagem regressiva de 5 s ("A pista votou: próxima música!") e a música é pulada.
- Os votos zeram a cada troca de música.

### 🔥 "Essa vai pra festa!"
Botão ao lado do "Pular". Um clique = um voto por pessoa por música (fica laranja depois de votar; mostra o total entre parênteses). Os votos ficam gravados **permanentemente** na coleção `partyVotes` do Firestore para a curadoria do setlist da festa real — cada registro guarda o vídeo, quem votou e quem tinha colocado a música.

### Reprodução sincronizada — o DJ no comando
- **Todo mundo assiste ao mesmo ponto do vídeo**: quem entra no meio da música já começa nos segundos certos, e um ajuste automático corrige qualquer descompasso maior que 6 s.
- **Só o DJ controla o player** — e mesmo ele não avança nem retrocede: ninguém tem a barra de progresso do YouTube. O DJ pausa/retoma tocando no vídeo; para os demais, cliques e teclado ficam bloqueados (aviso "🔒 Só o DJ controla o player").
- **Propagandas**: o botão **"📺 Pular propaganda"** libera os cliques no player por 15 s — tempo de apertar o "Pular anúncio" do YouTube — e depois re-trava sozinho. Se alguém pausar sem querer nesse intervalo, a sincronia corrige em segundos.
- **O que o DJ faz, todos veem**: pausar e retomar no player do DJ replica para toda a pista em segundos.

### Troca automática
- **10 minutos**: qualquer vídeo é pulado automaticamente ao completar 10 min de reprodução.
- **Fim do vídeo**: quando o vídeo termina, a próxima música da fila entra sozinha.
- **DJ que sai da tela**: o crachá "🎧 Sua vez na mesa!" avisa para **ficar na tela**. Se quem está na mesa fecha o app, minimiza ou troca de aba por mais de ~45 s, a pista não fica refém: o líder passa a vez com a contagem de 5 s ("🎧 Fulano saiu da pista — próxima música!"). Ao voltar, a pessoa recebe um toast explicando que perdeu a vez.
- **Vídeo que não toca** (removido, privado, embed bloqueado, indisponível na região): o erro do player dispara a troca ("⚠️ Vídeo indisponível — próxima música!") em vez de deixar a pista na tela preta até os 10 min.
- **Player travado**: se o *seu* player para de dar sinal por 45 s (buffer infinito, iframe morto), o app recarrega **só o seu iframe** e volta no ponto certo da música — sem pular a música para os outros.
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
