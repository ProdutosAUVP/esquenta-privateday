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
- **Globo refletor** pendurado no topo, com brilho colorido pulsante e balanço suave.
- Ladrilhos 80s acendem em cores neon aleatórias; luzes de ambiente pulsam nos cantos.
- **Mesa de DJ** no canto inferior direito: vinis giram e o equalizador anima quando há música; mostra quem está "na mesa" (dono da música atual). O avatar do DJ é teleportado para a mesa enquanto sua música toca.
- VIPs têm coroa e aura laranja intensa; o DJ atual ganha aura rosa neon e fones.

## Fila do DJ e player

### Adicionar música
Cole um link do YouTube no campo da fila. A música entra no fim da fila com seu nome.

- Se a **playlist da casa** estiver tocando (ninguém na mesa), uma **contagem regressiva de 5 segundos** aparece sobre o player ("🎵 Música de Fulano entrando na pista!") e a sua música assume.

### Votar para pular
Botão **"Pular (x/y)"** no canto do player:
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
- Mensagens do dia mostram só a hora (`14:32`); mensagens de dias anteriores mostram **data e hora** (`03/08 · 14:32`).

### Chat privado (DM)
- **Clique no avatar de alguém na pista** para abrir uma conversa privada (o cursor vira "mãozinha" sobre os avatares).
- Painel flutuante com bolhas estilo mensageiro (suas mensagens em laranja, as do outro em cinza).
- Mensagens novas com o painel fechado geram um **badge vermelho** com contagem sobre o avatar da pessoa na pista.
- Só os dois participantes veem a conversa (filtro por `convId` no cliente).

## Responsividade

- Layout usa `100dvh` (estável em navegadores mobile com barra de endereço dinâmica).
- **Desktop/notebook (≥1024px)**: pista à esquerda, chat + fila em coluna fixa à direita.
- **Tablet/celular**: player e pista em cima, chat + fila ocupando ~48% da altura embaixo; painel de DM ancorado à esquerda; modal com abas.
- Header compacto: globo maior à esquerda, "PRIVATE DAY" e "Esquenta 2026" centralizados e colados.
