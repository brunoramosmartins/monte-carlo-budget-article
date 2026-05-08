# Por Que o Seu Orcamento Nunca Crava o Valor Exato

## Simulacao Monte Carlo para Planejamento Orcamentario — de Estimativas Pontuais a Distribuicoes de Probabilidade

---

## 0. O Que Voce Precisa Saber

Este artigo assume familiaridade com:

**Necessario:**
- Calculo basico: derivadas, integrais, expansao de Taylor (usados em §4–§5)
- Probabilidade basica: variaveis aleatorias, FDP / FMP, FDA, esperanca, variancia
- Leitura confortavel de notacao matematica

**Util mas nao obrigatorio:**
- Exposicao previa a Lei dos Grandes Numeros e ao Teorema Central do Limite (ambos sao derivados a partir de primeiros principios em §4 e §5)
- Familiaridade com intervalos de confianca (derivados em §5)
- Conhecimento operacional de NumPy (usado na implementacao, mas o artigo e legivel sem)

**Fora do escopo (nao sera coberto):**
- Distribuicoes de cauda pesada e como escolhe-las — ver o artigo companheiro sobre selecao de distribuicoes
- Inferencia Bayesiana alem de um exemplo conceitual de atualizacao (§8)
- Problemas de qualidade de dados reais (NDA, censura, ruido de reporte)
- Previsao em series temporais (regimes rolantes, ARIMA, modelos em espaco de estados)

### Guia de Leitura

O artigo opera em tres niveis de profundidade. Escolha o que faz sentido para voce.

| Se voce e… | Leia | Pule / passe rapido |
|------------|------|---------------------|
| Gestor de orcamento / executivo | §1, §2, §9 (resultados), §10 (framework), §11 | As provas em §4 e §5 — leia apenas as notas de takeaway |
| Analista aplicando o metodo | §1–§3, §6, §7, §9, §10 | A prova via FGM em §5 |
| Leitor auditando a matematica | Todas as secoes em ordem | Nada |

As figuras e a passagem "Como Apresentar Resultados" em §10 sao os pedacos de maior valor para uma leitura rapida.

---

## 1. Introducao

Alguem pede o orcamento do proximo ano. Voce abre uma planilha, multiplica quantidades por custos unitarios, adiciona contingencias, arredonda um pouco para cima — e entrega um numero. Um unico numero.

Mas e se esse numero for apenas uma amostra de uma distribuicao que voce nunca viu?

Toda organizacao que gerencia orcamentos — custos de headcount, despesas de projetos, procurement, marketing — enfrenta o mesmo ritual. O time produz uma estimativa pontual, a lideranca aprova, e o periodo transcorre. Meses depois, durante uma revisao periodica do forecast, os gastos reais divergem. O time ajusta. Outra revisao. Outro ajuste. No final do periodo, o numero original parece pouco mais que um chute educado.

### O Custo Oculto de uma Estimativa Pontual

O problema nao e que a estimativa estava errada. O problema e que um numero unico nao carrega informacao sobre sua propria incerteza — e essa ignorancia tem preco.

- **Capital fica preso como gordura.** Sem conhecer a distribuicao, a saida prudente e super-reservar. Cada milhao retido contra um pior caso imaginado e um milhao que nao pode financiar contratacoes, um projeto ou uma iniciativa de cliente. Esse e o **custo de oportunidade da variancia que voce nao enxerga**.
- **Planos quebram diante de choques que voce nao previu.** Sub-reservar e a falha simetrica: um projeto trava no meio do ano porque a contingencia foi calibrada em "o resultado medio mais 10%", e o resultado real morava na cauda direita de uma distribuicao que ninguem modelou. A estimativa pontual nao avisou — porque ela nao descreve cauda nenhuma.
- **Revisoes de forecast parecem erros.** Cada variancia mensal contra um orcamento deterministico vira "um miss". Com uma distribuicao, a mesma variancia vira "estamos dentro do intervalo de 80%, nenhuma acao necessaria" — ou "cruzamos a linha de 95%, escalar". Os mesmos dados, uma decisao diferente.

Uma estimativa pontual entrega um numero. Uma distribuicao entrega a **politica**: quanto reservar, quando escalar e com que confianca em cada passo.

### O Que Muda com uma Distribuicao

Este artigo substitui o numero unico por uma **distribuicao de probabilidade**. Usando simulacao Monte Carlo fundamentada na Lei dos Grandes Numeros e no Teorema Central do Limite, transformamos "esperamos gastar R$ 11,5M" em "temos 90% de confianca de que os gastos ficarao entre R$ 10,7M e R$ 12,4M, com 3% de probabilidade de ultrapassar o teto."

> **Um orcamento e uma distribuicao, nao um numero.** Essa unica mudanca altera como orcamentos sao *aprovados*, nao apenas como sao *calculados*. O resultado deixa de ser uma meta — passa a ser um perfil de risco que um CFO pode subscrever.

A abordagem e **geral**: aplica-se a qualquer orcamento que possa ser decomposto em componentes estocasticos — headcount, projetos, procurement, licenciamento, infraestrutura. Ilustramos com um orcamento de headcount de TI (salarios, beneficios, horas extras, incidentes) como estudo de caso concreto, mas o framework matematico se transfere diretamente para qualquer dominio.

A jornada segue quatro estagios: formalizamos componentes orcamentarios como variaveis aleatorias (Secao 3), provamos que a media das simulacoes converge para a resposta verdadeira (Secao 4), quantificamos o erro da simulacao (Secao 5), e implementamos o estimador com tecnicas de reducao de variancia (Secoes 6-7). A Secao 9 valida tudo experimentalmente; a Secao 10 transforma a matematica em um framework de decisao que voce entrega a um gestor de orcamento na segunda-feira de manha.

### Notacao

| Simbolo | Significado |
|---------|-------------|
| $X_{\text{total}}$ | Custo orcamentario total (variavel aleatoria) |
| $X_k$ | Custo do componente $k$ |
| $n$ | Numero de unidades (headcount, itens, etc.) |
| $\bar{X}_N$ | Media amostral de $N$ simulacoes |
| $\hat{\theta}_N$ | Estimador Monte Carlo |
| $\sigma$ | Desvio padrao da distribuicao de custos |
| $z_{\alpha/2}$ | Quantil Normal para nivel de confianca $1-\alpha$ |

**Notacao do estudo de caso** (headcount TI):

| Simbolo | Significado |
|---------|-------------|
| $S_i$ | Salario mensal do funcionario $i$ |
| $\beta$ | Multiplicador de beneficios |
| $H_i$ | Horas extras por funcionario por mes |
| $r_{ot}$ | Valor da hora extra |
| $I$ | Numero de incidentes graves por ano |
| $C_j$ | Custo do incidente $j$ |

---

## 2. O Problema da Estimativa Pontual

Uma estimativa pontual e um valor unico usado para aproximar um parametro desconhecido. No planejamento orcamentario, ela toma a forma:

$$
\hat{X} = \sum_{k} (\text{quantidade}_k \times \text{custo unitario}_k) + \text{contingencia}
$$

O resultado e um numero — digamos, R$ 11,5 milhoes. Mas esse numero e $E[X_{\text{total}}]$: o valor esperado de uma variavel aleatoria. Ele nos diz o centro da distribuicao. O que descarta e todo o resto:

- **Variancia:** Quao dispersos sao os resultados possiveis?
- **Assimetria:** A distribuicao e simetrica, ou custos podem ser puxados para cima por eventos extremos?
- **Risco de cauda:** Qual a probabilidade de ultrapassar o teto aprovado?
- **Confianca:** Quao certos estamos de que o custo verdadeiro esta dentro de ±5% da estimativa?

Em termos formais, a estimativa pontual nos da $E[X]$ mas nao a distribuicao $F_X$. A simulacao Monte Carlo recupera $F_X$ — o quadro completo.

### O Que a Planilha Realmente Esta Fazendo

A estimativa pontual nao e um modelo *ausente*. E um modelo com hipoteses escondidas. Para tornar a critica concreta, eis o que uma planilha tipica de FP&A calcula:

> **Box: Modelo tipico de FP&A**
>
> 1. **Melhor estimativa:** $\hat{X} = \sum_k (\text{quantidade}_k \times \text{custo unitario}_k)$
> 2. **Contingencia:** $\hat{X}_{\text{orcado}} = \hat{X} \times (1 + c)$ para algum $c$ escolhido (em geral 5-15%)
> 3. **Cenarios otimista / pessimista:** $\hat{X} \times 0,9$ e $\hat{X} \times 1,1$, definidos por sensacao
>
> O que isso *implicitamente* assume:
>
> - A saida e uma constante (sem distribuicao).
> - Quando pressionada, a contingencia $c$ e um "buffer para incerteza" unilateral — mas quanto risco ela cobre, de fato? A planilha nao diz.
> - Os cenarios otimista/pessimista desenham uma **faixa**, mas sem probabilidade associada. Sao percentis 5 e 95? 1 e 99? A planilha nao diz.
>
> Se te perguntarem "qual a chance de estourarmos o orcamento em mais de 10%?", uma planilha deterministica nao tem resposta — so um chute. Monte Carlo tem.

O fator de contingencia nao e o problema. O problema e que a planilha *teve* que fazer uma hipotese distribucional, fez em silencio, e depois se recusou a dizer qual. Monte Carlo torna a distribuicao explicita, calibrada e falsificavel. Antes de simular a partir de $F_X$, no entanto, precisamos primeiro escreve-la — declarando quais componentes do orcamento sao aleatorios e quais distribuicoes os descrevem. E o que a proxima secao faz.

### O Padrao Geral

Qualquer orcamento com componentes incertos pode ser escrito como:

$$
X_{\text{total}} = \sum_{k=1}^{K} g_k(\mathbf{Z}_k)
$$

onde $g_k$ e uma funcao de custo para o componente $k$ e $\mathbf{Z}_k$ e um vetor de entradas aleatorias. A estimativa pontual colapsa cada $g_k$ para seu valor esperado; Monte Carlo preserva a distribuicao conjunta completa.

---

## 3. Componentes Orcamentarios como Variaveis Aleatorias

Cada componente de um orcamento e potencialmente uma variavel aleatoria. Trata-los como constantes e uma escolha de modelagem que descarta informacao. O insight chave: **identifique quais componentes carregam incerteza significativa, modele-os probabilisticamente, e mantenha o restante deterministico.**

> **Modelo mental:** *se voce nao consegue apontar para o valor real do ano passado e dizer "cravamos exatamente", aquele componente e aleatorio. Modele.*

### A Estrutura Geral

Um modelo orcamentario estocastico tem tres tipos de componentes:

1. **Custos proporcionais:** quantidade × taxa, onde um ou ambos podem ser aleatorios
2. **Custos fixos com incerteza:** estrutura conhecida mas magnitude incerta
3. **Eventos raros:** contagem aleatoria de ocorrencias × custo aleatorio por evento (processo composto)

$$
X_{\text{total}} = \underbrace{\sum_{i=1}^{n} f(Z_i)}_{\text{proporcional}} + \underbrace{\text{componentes fixos}}_{\text{deterministico}} + \underbrace{\sum_{j=1}^{N_{\text{eventos}}} C_j}_{\text{eventos raros}}
$$

### Tabela Operacional de Decisao

A pergunta pratica mais dificil e *quais componentes modelar como aleatorios*. A tabela abaixo e a ferramenta de trabalho — preencha uma linha por componente do orcamento e aplique a regra pratica.

| Componente | Aleatorio? | Distribuicao | Por que |
|------------|-----------|--------------|---------|
| Salario por funcionario | Sim | LogNormal | Estritamente positivo, assimetrico a direita por senioridade |
| Headcount | As vezes | Poisson (se hiring/attrition modelados) | Frequentemente deterministico na v1; expandir depois |
| Multiplicador de beneficios | Nao | Constante | Negociado anualmente, baixa variancia |
| Horas extras | Sim | Poisson | Contagem discreta de eventos independentes |
| Contagem de incidentes | Sim | Poisson | Eventos raros com taxa constante |
| Custo por incidente | Sim | LogNormal | Cauda direita pesada (poucos incidentes grandes) |
| Cambio (se aplicavel) | Sim | Normal ou empirica | Simetrica em torno da taxa forward |

> **Regra pratica:** modele um componente como **aleatorio** se ele satisfaz *qualquer* uma destas condicoes:
>
> - O **coeficiente de variacao** $\text{CV} = \sigma / \mu \gt 10\%$ para esse componente.
> - Ele contribui com mais de ~5% do orcamento total em termos absolutos — mesmo com CV baixo, uma fatia grande com ruido moderado domina a cauda.
>
> Componentes abaixo das duas regras podem ficar deterministicos na v1 com perda desprezivel.

No nosso estudo de caso, salarios e custos de incidente passam folgadamente; o multiplicador de beneficios nao. Horas extras ficam no meio — Poisson com $\lambda_h = 5$ tem $\text{CV} = 1/\sqrt{5} \approx 45\%$, mas sua fatia do orcamento e pequena (~2%), entao a contribuicao para o CV total e modesta.

### Uma Nota Sobre Correlacao

A forma compacta acima assume que os componentes sao mutuamente independentes — e que, dentro de cada componente, as unidades sao i.i.d. Isso raramente e estritamente verdade, e merece flag:

- **Salarios e horas extras podem ser negativamente correlacionados** — funcionarios senior recebem salarios maiores mas podem registrar menos horas extras.
- **Frequencia e severidade de incidentes podem ser positivamente correlacionadas** — um mes caotico com muitos incidentes tambem e um mes em que cada um e mais dificil de conter.
- **Fatores macro propagam** — inflacao eleva salarios, cambio *e* custos contratuais juntos.

Este artigo assume independencia para manter a matematica tratavel e o estudo de caso limpo. O custo e que os ICs simulados podem **subestimar** levemente a variancia real quando correlacoes ignoradas sao positivas, e **superestimar** quando sao negativas. Duas formas de lidar na pratica:

1. **Distribuicoes conjuntas / copulas** — a resposta formal; use uma copula Gaussiana para especificar correlacoes par a par sobre as distribuicoes marginais.
2. **Checagem de sensibilidade** — re-rode a simulacao com a correlacao plausivel mais forte aplicada e observe se o P95 se move materialmente. Se sim, modele a correlacao. Se nao, ignore.

Para um orcamento v1, o default e independencia e correlacao como expansao v2. Em ambiente regulado ou mission-critical, modele correlacao desde o inicio.

### Estudo de Caso: Orcamento de Headcount de TI

Instanciamos essa estrutura com um exemplo concreto — um time de TI com 50 pessoas:

**Salarios (LogNormal).** Salarios sao estritamente positivos e assimetricos a direita:

$$
S_i \sim \text{LogNormal}(\mu_s, \sigma_s^2), \quad \mu_s = 9{,}2, \; \sigma_s = 0{,}3
$$

$$
E[S_i] = e^{\mu_s + \sigma_s^2/2} = e^{9{,}245} \approx R\$ \, 10.362
$$

**Horas Extras (Poisson).** Discretas, nao-negativas, relativamente raras:

$$
H_i \sim \text{Poisson}(\lambda_h), \quad \lambda_h = 5
$$

**Incidentes (Poisson Composto).** Taxa aleatoria com severidade aleatoria:

$$
I \sim \text{Poisson}(\lambda_I), \quad C_j \sim \text{LogNormal}(\mu_I, \sigma_I^2)
$$

**Custo total:**

$$
X_{\text{total}} = \underbrace{\sum_{i=1}^{n} S_i \cdot \beta \cdot 12}_{\text{salarios + beneficios}} + \underbrace{\sum_{i=1}^{n} H_i \cdot r_{ot} \cdot 12}_{\text{horas extras}} + \underbrace{\sum_{j=1}^{I} C_j}_{\text{incidentes}}
$$

Pela linearidade da esperanca:

$$
E[X_{\text{total}}] \approx 11.191.000 + 240.000 + 123.500 \approx R\$ \, 11.554.500
$$

O componente salarial domina com ~97%. Esse padrao — um componente gerando a maior parte da variancia — e comum em diversos tipos de orcamento e sera importante para reducao de variancia.

### Outras Instanciacoes

A mesma estrutura se aplica a:

| Tipo de Orcamento | Proporcional | Fixo | Eventos Raros |
|-------------------|-------------|------|---------------|
| **Headcount TI** | Salarios × headcount | Beneficios | Incidentes |
| **Infra Cloud** | Uso × preco unitario | Instancias reservadas | Remediacao de indisponibilidades |
| **Marketing** | Impressoes × CPC | Taxas de plataforma | Campanhas fracassadas |
| **Construcao** | Materiais × quantidade | Alvaras, seguros | Atrasos climaticos, retrabalho |
| **Projetos de P&D** | Horas × taxa × tamanho do time | Equipamentos | Mudancas de escopo |

Em cada caso: identifique os componentes aleatorios, escolha distribuicoes, e simule.

Uma ressalva curta antes de prosseguir. Tudo o que vem a seguir assume que as distribuicoes escolhidas para cada componente sao *corretas*. Monte Carlo simulara fielmente o que voce alimentar — incluindo um modelo ruim. Uma LogNormal de salarios ajustada a dados que sao, na verdade, de cauda pesada vai gerar um IC que parece estreito e esta errado. O artigo companheiro sobre selecao de distribuicoes e caudas pesadas trata dessa pergunta diretamente — como escolher uma distribuicao a partir de dados, quando suspeitar de uma cauda mais pesada do que a vista sugere, e o que acontece com estimativas de risco quando voce erra. Se so der tempo de ler um, leia este primeiro; o companheiro e o que impede voce de estar precisamente errado.

Com o modelo definido, as proximas duas secoes respondem as duas perguntas que qualquer praticante faz antes de confiar em uma simulacao: *a media vai convergir?* (Secao 4, Lei dos Grandes Numeros) e *quao confiante posso estar apos $N$ rodadas?* (Secao 5, Teorema Central do Limite).

---

## 4. A Media Vai Convergir? A Lei dos Grandes Numeros

Se simularmos o orcamento 10.000 vezes e calcularmos a media, essa media convergira para o verdadeiro $E[X_{\text{total}}]$? A Lei dos Grandes Numeros diz que sim.

### Desigualdade de Chebyshev

Para qualquer variavel aleatoria $X$ com media $\mu$ e variancia $\sigma^2$:

$$
P(|X - \mu| \geq \epsilon) \leq \frac{\sigma^2}{\epsilon^2}
$$

### A Lei Fraca dos Grandes Numeros

Sejam $X_1, \ldots, X_N$ i.i.d. com media $\mu$ e variancia $\sigma^2$. A media amostral satisfaz:

$$
P(|\bar{X}_N - \mu| \geq \epsilon) \leq \frac{\sigma^2}{N\epsilon^2} \to 0 \quad \text{quando } N \to \infty
$$

**Demonstracao.** Como $E[\bar{X}_N] = \mu$ e $\text{Var}(\bar{X}_N) = \sigma^2/N$, aplicar Chebyshev a $\bar{X}_N$ da o resultado. $\blacksquare$

A Lei Forte garante convergencia quase certa (probabilidade 1).

**Para Monte Carlo:** cada simulacao $X_i$ e um cenario possivel. A LGN garante que a media de $N$ cenarios converge para o custo esperado verdadeiro.

![Convergencia LGN](../figures/lln_convergence.png)
*Figura 1: Dez execucoes independentes da media amostral convergindo para $E[X]$, com banda de Chebyshev a 95%.*

A LGN garante que chegamos a resposta certa eventualmente. Ela nao diz quao perto estamos depois de, digamos, $N = 1.000$ rodadas — o limite de Chebyshev e um pior caso entre todas as distribuicoes, nao uma estimativa apertada. Para responder "quao confiante posso estar?", precisamos do *formato* do erro, nao apenas de seu decaimento. E isso que o Teorema Central do Limite oferece.

---

## 5. Quao Errados Podemos Estar? O Teorema Central do Limite

A LGN nos diz que converge. O TCL nos diz **quao rapido** — e da intervalos de confianca.

> ### TL;DR (pule a prova se nao estiver auditando a matematica)
>
> 1. **O que diz:** a media de muitas simulacoes independentes se torna aproximadamente Normal conforme $N$ cresce, *independentemente da distribuicao subjacente*. Custos assimetricos a direita entram, curva sino sai.
> 2. **O que entrega:** um intervalo de confianca $\bar{X}_N \pm z_{\alpha/2} \cdot s / \sqrt{N}$. Com $z_{0.025} = 1{,}96$, e o IC 95% padrao.
> 3. **O que custa:** $N$ escala como $1/\epsilon^2$. Para reduzir a semi-amplitude do IC pela metade, rode 4× mais simulacoes.
>
> A prova abaixo mostra *por que* isso funciona via funcoes geradoras de momento. A conclusao vale de qualquer forma.

### Enunciado

Para variaveis i.i.d. com media $\mu$ e variancia $\sigma^2$:

$$
\frac{\sqrt{N}(\bar{X}_N - \mu)}{\sigma} \xrightarrow{d} N(0, 1)
$$

### Esboco da Demonstracao (via FGM)

Defina $W_i = (X_i - \mu)/\sigma$. A soma padronizada $Z_N = \frac{1}{\sqrt{N}}\sum W_i$ tem FGM:

$$
M_{Z_N}(t) = \left[M_W\left(\frac{t}{\sqrt{N}}\right)\right]^N
$$

Expandindo em Taylor: $\log M_W(s) = s^2/2 + O(s^3)$. Substituindo $s = t/\sqrt{N}$:

$$
\log M_{Z_N}(t) = \frac{t^2}{2} + O\left(\frac{t^3}{\sqrt{N}}\right) \to \frac{t^2}{2}
$$

Como $e^{t^2/2}$ e a FGM de $N(0, 1)$, unicidade da $Z_N \xrightarrow{d} N(0, 1)$. $\blacksquare$

### Intervalos de Confianca

Pelo TCL, o IC $(1-\alpha)$ para $\mu$ e:

$$
\bar{X}_N \pm z_{\alpha/2} \cdot \frac{s_N}{\sqrt{N}}
$$

### Escolhendo N

Para semi-amplitude $\epsilon$:

$$
N \geq \left(\frac{z_{\alpha/2} \cdot \sigma}{\epsilon}\right)^2
$$

Para nosso estudo de caso ($\sigma \approx 493K$, $\epsilon = 100K$, 95%): $N \geq 94$.

![Emergencia de Normalidade](../figures/clt_normality_emergence.png)
*Figura 2: Conforme $n$ aumenta, a media padronizada converge para $N(0,1)$.*

Com a LGN dando convergencia e o TCL dando a taxa de erro, o estimador Monte Carlo esta totalmente especificado. Podemos finalmente enunciar suas propriedades formais — e tratar a pergunta silenciosa de quando, mesmo com tudo isso, o estimador ainda pode produzir respostas confiantemente erradas.

---

## 6. O Estimador Monte Carlo

### Definicao

O estimador Monte Carlo de $\theta = E[g(X)]$ e:

$$
\hat{\theta}_N = \frac{1}{N} \sum_{i=1}^N g(X_i)
$$

onde cada $g(X_i)$ e o custo total de um cenario simulado.

### Propriedades

**Nao-viesado.** $E[\hat{\theta}_N] = \theta$.

**Consistente.** $\hat{\theta}_N \xrightarrow{P} \theta$ (LGN).

**Normalidade assintotica.** $\sqrt{N}(\hat{\theta}_N - \theta)/\sigma_g \xrightarrow{d} N(0, 1)$ (TCL).

**Taxa de convergencia.** $\text{EP} = \sigma_g / \sqrt{N}$, decaindo como $O(1/\sqrt{N})$. **Independente da dimensao** de $X$.

### Lei de Escala

Reduzir a amplitude do IC pela metade requer 4× mais simulacoes.

> **Modelo mental:** *precisao nao e de graca. Voce compra com simulacoes — e o preco dobra cada vez que voce reduz pela metade a barra de erro.*

### Erro Quadratico Medio

$\text{EQM}(\hat{\theta}_N) = \sigma_g^2 / N$ (estimador nao-viesado).

### Quando Monte Carlo Falha

Monte Carlo e um estimador fiel de $E[g(X)]$ *dado* um modelo. Ele *nao* verifica se o modelo esta certo. O estimador pode ser nao-viesado, consistente, e assintoticamente normal — e ainda produzir conclusoes que estao confiantemente erradas. Os modos de falha mais comuns:

1. **Distribuicao mal especificada.** Voce escolheu Normal onde a verdade e cauda pesada, ou usou uma taxa Poisson calibrada num ano calmo. O IC simulado encolhe em torno de um centro que esta errado; tudo a jusante herda o vies. *Mitigacao:* ajuste distribuicoes em dados multi-ano quando possivel, plote Q-Q contra a distribuicao proposta, e rode sensibilidade contra familias alternativas (LogNormal vs Gamma vs Pareto de cauda pesada).

2. **Correlacao ignorada.** Tratar componentes como independentes quando covariam positivamente subestima a variancia. O IC parece estreito — e quebra no primeiro choque conjunto. *Mitigacao:* na duvida, re-rode com uma copula Gaussiana na correlacao plausivel maxima. Se o P95 se mover materialmente, modele; senao, documente a hipotese.

3. **Caudas pesadas que o modelo nao captura.** Fenomenos de cauda pesada (severidade de incidentes, choques cambiais, overruns de projeto) podem violar a hipotese de variancia finita que sustenta o TCL. A media amostral ainda converge, mas o IC baseado em $z_{\alpha/2} \sigma / \sqrt{N}$ fica super-confiante. *Mitigacao:* verifique o decaimento empirico da cauda; se parecer polinomial em vez de exponencial, mude para uma familia de cauda pesada (Pareto, Student-$t$). O artigo companheiro sobre selecao de distribuicoes cobre isso diretamente.

4. **Variancia do piloto subestima a variancia real.** A formula de $N$ minimo $N \geq (z \sigma / \epsilon)^2$ usa um $\sigma$ amostral do piloto. Se o piloto foi pequeno ou azarado, $\sigma$ e viesado para baixo — e o IC real e mais largo do que prometido. *Mitigacao:* sempre re-cheque a semi-amplitude do IC *depois* da rodada completa. Se exceder o alvo, rode mais.

5. **A decisao nao esta no corpo.** Monte Carlo tem melhor precisao no centro da distribuicao e pior nas caudas. Decisoes em torno da mediana ou media (ex.: "custo esperado") sao confiaveis; decisoes em torno de percentis extremos (ex.: "déficit de 1 em 1000 anos") precisam de $N$ muito maior para estimar o mesmo percentil com a mesma precisao. *Mitigacao:* se voce se importa com caudas extremas, mude para amostragem por importancia ou teoria de valores extremos — MC simples nao e a ferramenta certa.

A afirmacao honesta e mais estreita do que "Monte Carlo da a resposta". E: *Monte Carlo da a resposta que o modelo implica*. Falhas a montante da simulacao — distribuicao errada, dependencias erradas, cauda errada — nao sao detectadas pela simulacao em si. Valide separadamente.

Com essas ressalvas reconhecidas, o estimador funciona — mas a taxa $O(1/\sqrt{N})$ e dura. Toda divisao por dois do IC exige quadruplicar as simulacoes, e na precisao necessaria para decisoes orcamentarias serias isso fica caro rapido. A proxima secao mostra como quebrar esse teto sem mexer em $N$.

---

## 7. Tornando Mais Rapido: Reducao de Variancia

A taxa $O(1/\sqrt{N})$ significa que precisao por forca bruta e cara. Tecnicas de reducao de variancia alcancam ICs mais estreitos **para o mesmo custo computacional**.

### Variaveis de Controle

Se conhecemos $E[h(X)]$ para alguma funcao $h$ correlacionada com $g$:

$$
\hat{\theta}_{CV} = \hat{\theta}_N - c^*\left(\bar{h}_N - E[h(X)]\right)
$$

Coeficiente otimo:

$$
c^* = \frac{\text{Cov}(g(X), h(X))}{\text{Var}(h(X))}
$$

Variancia no otimo:

$$
\text{Var}(\hat{\theta}_{CV}) = \frac{\text{Var}(g(X))}{N}(1 - \rho_{g,h}^2)
$$

**No estudo de caso:** usando soma bruta de salarios como controle ($\rho \approx 0,99$) obtem-se aproximadamente **30× de reducao de variancia** — equivalentemente, uma reducao de 5-6× na semi-amplitude do IC 95% para um mesmo $N$. Em qualquer orcamento, o componente dominante com media analitica conhecida e a variavel de controle natural.

### Variaveis Antiteticas

Gere pares espelhados. Se $g$ e monotona, $\text{Cov}(g(X), g(X')) < 0$ e a variancia e reduzida.

### Amostragem Estratificada

Particione o espaco de entrada em $K$ estratos. Pela lei da variancia total:

$$
\text{Var}(\hat{\theta}_{SS}) \leq \text{Var}(\hat{\theta}_{MC})
$$

Sempre. Remove a variancia entre estratos.

![Comparacao de Reducao de Variancia](../figures/variance_reduction_comparison.png)
*Figura 3: Amplitude do IC vs N para MC simples, variaveis antiteticas e variaveis de controle.*

### Por Que Isso Importa Alem da Matematica: ROI de Compute

Uma reducao de variancia de 30× soa como curiosidade matematica. E um resultado de **compute e tempo de resposta**.

Suponha que a simulacao simples precise de $N = 30.000$ rodadas para entregar um intervalo de confianca de ±R$ 50K. Com variaveis de controle, a mesma precisao chega em $N = 1.000$. Traduzindo para a realidade de engenharia:

| Aspecto | MC Simples | Com Variaveis de Controle | Implicacao Pratica |
|---------|-----------|---------------------------|---------------------|
| Rodadas para IC ±R$ 50K | 30.000 | 1.000 | 30× menos cenarios |
| Wall-clock em um laptop | ~18 s | ~0,6 s | **Atualizacao interativa em tempo real** |
| Custo de cloud por refresh | ~30 vCPU-seg | ~1 vCPU-seg | Desprezivel por query |
| Adequado para dashboard | Nao (lento demais) | Sim | Um CFO pode re-rodar durante uma reuniao de board |

O ROI nao e o numero da variancia; e o que esse numero *viabiliza*:

- **Dashboards vivos.** Um CFO arrastando um parametro de headcount e vendo o P95 atualizar em milissegundos e um produto diferente daquele que tira uma pausa de cafe para recalcular.
- **Sensibilidade em escala.** A analise de sensibilidade da Secao 9 roda a simulacao muitas vezes, uma por variacao de parametro. Cortar cada rodada em 50× transforma um batch noturno em uma tela de poucos segundos.
- **A/B barato de hipoteses do modelo.** Quer comparar LogNormal vs Gamma para salarios? MC simples transforma isso em uma reuniao; variaveis de controle transformam em um toggle de parametro.

A matematica justifica a tecnica. A economia de compute e o que faz ela ser entregue.

Ate aqui, a simulacao e construida uma vez, antes do periodo comecar — uma distribuicao estatica que ancora uma decisao unica. Mas orcamentos nao sao artefatos unicos; sao revisitados todo mes a medida que dados reais de gasto chegam. A proxima secao reformula a mesma maquinaria como a *primeira versao* de um orcamento que e atualizado continuamente, uma extensao Bayesiana que transforma o script unico em um forecast vivo.

---

## 8. Fase 2 de Maturidade: Atualizacao Continua do Orcamento

Tudo ate aqui construiu a **primeira versao** do orcamento: uma distribuicao de probabilidade calculada *antes* do periodo comecar, a partir de um modelo fixo. As Secoes 4-7 tornaram essa estimativa convergente, calibrada e eficiente.

Mas um orcamento nao e um artefato unico. Cada mes produz dados de gasto real. Cada trimestre traz revisoes de forecast. A distribuicao estatica de janeiro *nao* e a crenca correta em julho — a essa altura, ja temos evidencia.

O passo natural e **deixar os dados atualizarem a distribuicao**. Essa e a visao Bayesiana da mesma maquinaria, e transforma o orcamento de um calculo unico em um modelo vivo.

### Da Estimativa Frequentista para a Atualizacao Bayesiana

O teorema de Bayes e o mecanismo:

$$
P(\theta \mid \text{dados}) \propto P(\text{dados} \mid \theta) \cdot P(\theta)
$$

Lido em termos orcamentarios:

- **Priori $P(\theta)$** — a distribuicao de janeiro. O resultado da simulacao Monte Carlo da Secao 9, *reformulado como uma crenca sobre o mundo*.
- **Verossimilhanca $P(\text{dados} \mid \theta)$** — quao plausivel o gasto observado e, sob cada valor candidato de $\theta$.
- **Posteriori $P(\theta \mid \text{dados})$** — a distribuicao atualizada apos a chegada dos dados. Vira priori do mes seguinte.

Cada revisao de forecast e, na pratica, uma atualizacao Bayesiana informal. O ganho de maturidade e tornar isso formal — para que a atualizacao seja auditavel, a incerteza encolha coerentemente com a evidencia, e a politica ("escalar se cruzarmos P95") sobreviva entre revisoes em vez de ser re-debatida a cada ciclo.

### Um Exemplo Concreto de Atualizacao

Modele o custo salarial mensal medio do time como $\theta$. O Monte Carlo de janeiro da uma priori $\theta \sim N(\mu_0, \tau_0^2)$ — digamos, $\mu_0 = R\$ 11{,}55M$ com $\tau_0 = R\$ 500K$. Apos tres meses de custos mensais observados $x_1, x_2, x_3$ com variancia amostral $\sigma^2$, a posteriori e:

$$
\theta \mid x_1, x_2, x_3 \sim N\!\left(\frac{\tau_0^{-2} \mu_0 + 3\sigma^{-2} \bar{x}}{\tau_0^{-2} + 3\sigma^{-2}}, \; \frac{1}{\tau_0^{-2} + 3\sigma^{-2}}\right)
$$

A media posteriori e uma **media ponderada por precisao** da media a priori e da media dos dados. A variancia posteriori encolhe — quanto mais meses observados, mais estreita a crenca.

No mes 6, a posteriori e bem mais estreita do que a priori original. No mes 12, o ano acabou e a posteriori colapsa em torno do custo realizado. A trajetoria das posterioris *e* o forecast.

### Frequentista (Fase 1) vs Bayesiano (Fase 2): Quando Cada Um Encaixa

| Aspecto | Fase 1: MC Frequentista (Secoes 1-7) | Fase 2: Atualizacao Bayesiana (esta secao) |
|---------|---------------------------------------|--------------------------------------------|
| Parametros | Constantes fixas do modelo | Variaveis aleatorias com distribuicoes proprias |
| Informacao previa | Codificada implicitamente na escolha de distribuicao | Explicita, auditavel, incorpora historico |
| Saida | Intervalo de confianca | Intervalo de credibilidade (probabilidade direta sobre $\theta$) |
| Atualizacao no periodo | Re-rodar simulacao do zero | Natural: posteriori do mes $m$ vira priori do $m+1$ |
| Melhor quando | Construindo o *primeiro* orcamento; sem historico utilizavel | Atualizando um orcamento *existente* com dados mensais |
| Custo | Uma rodada de Monte Carlo | Uma engine de simulacao **mais** um pipeline de dados |

### Por Que Isso Importa para o Leitor de Portfolio

Um time que entrega apenas a simulacao da Fase 1 construiu um script. Um time que entrega Fase 1 *e* Fase 2 construiu um **produto de dados** — um modelo que vive ao longo do ano fiscal, melhora com dados e gera decisoes, nao apenas numeros.

Este artigo foca na Fase 1 porque a Fase 2 herda seu rigor: uma atualizacao Bayesiana sobre uma priori mal calibrada e apenas uma forma lenta de estar errado. Acerte a simulacao primeiro; a camada de ciclo de vida e, entao, uma adicao pequena. A Secao 10 retorna a essa visao de ciclo de vida no framework pratico.

Teoria e reframings de lado, a pergunta que decide se algo disso importa e: *a engine funciona, na pratica?* A proxima secao responde experimentalmente — cinco estudos controlados cobrindo convergencia, emergencia de normalidade, simulacao completa, reducao de variancia e sensibilidade, cada um com setup, metrica e resultado explicitos.

---

## 9. Experimentos e Resultados

Cada experimento segue o mesmo template — **Objetivo**, **Setup**, **Metrica**, **Resultado** — para que a validacao se leia como um estudo, nao uma demo. Todas as rodadas usam seeds fixas; os scripts correspondentes em `scripts/` reproduzem cada figura exatamente.

### Experimento A — Convergencia da LGN

- **Objetivo:** mostrar que a media amostral converge para o $E[X]$ analitico conforme $N$ cresce, com variancia caindo a taxa $O(1/\sqrt{N})$.
- **Setup:** 10 rodadas independentes de sorteios LogNormal de salarios, $N$ de 1 a 10.000 cada. Banda de Chebyshev 95% sobreposta.
- **Metrica:** desvio absoluto $|\bar{X}_n - E[X]|$ entre rodadas.
- **Resultado:** em $N$ pequeno, as rodadas se espalham; em $N = 5.000$, as 10 rodadas agrupam-se dentro de R$ 200 da media analitica. O decaimento empirico acompanha $\sigma/\sqrt{n}$ em escala log-log.

*Ver Figura 1.*

### Experimento B — Normalidade do TCL

- **Objetivo:** verificar que a media amostral padronizada de sorteios LogNormal converge em distribuicao para $N(0, 1)$.
- **Setup:** 10.000 repeticoes de "sortear $n$ LogNormais, padronizar a media", para $n \in \{1, 5, 10, 30, 100\}$. Histograma + QQ-plot por $n$.
- **Metrica:** linearidade do QQ-plot (regressao $R^2$) e ajuste visual a densidade Normal padrao.
- **Resultado:** visivelmente nao-Normal em $n = 1$; em $n = 30$, o histograma acompanha $N(0,1)$; em $n = 100$, $R^2 \gt 0,999$.

*Ver Figura 2.*

### Experimento C — Simulacao Completa do Orcamento

- **Objetivo:** estimar a distribuicao completa de $X_{\text{total}}$, nao apenas sua media — e quantificar a probabilidade de ultrapassar um teto.
- **Setup:** $N = 50.000$ iteracoes do modelo de headcount de TI com parametros padrao, seed 42. Teto em R$ 12,5M.
- **Metrica:** erro relativo da media MC vs $E[X]$ analitico, semi-amplitude do IC 95%, faixa P5-P95, $P(X \gt \text{teto})$.
- **Resultado:** media MC dentro de 0,1% do analitico. Semi-amplitude do IC 95% aproximadamente R$ 4K. P5-P95 abrange ~R$ 1,6M. A probabilidade de ultrapassar R$ 12,5M e aproximadamente 3%. Distribuicao assimetrica a direita.

![Simulacao do Orcamento](../figures/budget_simulation.png)
*Figura 4: Distribuicao do custo orcamentario (histograma + FDA) com media, P5/P95 e teto anotados.*

### Experimento D — Reducao de Variancia

- **Objetivo:** medir o speedup de variaveis de controle e antiteticas contra MC simples para o mesmo $N$.
- **Setup:** os tres metodos em $N \in \{500, 1.000, 2.000, 5.000, 10.000\}$. Variavel de controle: soma bruta de salarios (media analitica conhecida).
- **Metrica:** semi-amplitude do IC 95% por metodo, plotada contra $N$ em escala log-log.
- **Resultado:** variaveis de controle reduzem a amplitude do IC em aproximadamente **5–6×** em todos os $N$ testados (equivalente a redu&ccedil;ao de ~30× na variancia; $\rho \approx 0,99$ efetivo). A implementacao antitetica se sobrepoe a MC simples — seu ganho modesto reflete que a estrutura Poisson composta do modelo de orcamento e dificil de "espelhar" de forma limpa via pareamento de seeds. A inclinacao log-log e $-1/2$ para todos os metodos, confirmando a taxa $O(1/\sqrt{N})$ — reducao de variancia desloca o *intercepto*, nao a taxa.

*Ver Figura 3.*

### Experimento E — Analise de Sensibilidade

- **Objetivo:** ranquear parametros do modelo pelo impacto em $E[X_{\text{total}}]$ para guiar onde concentrar esforco de modelagem.
- **Setup:** variar a **contribuicao efetiva** de cada um dos 8 parametros em ±20% (para parametros log-media, isso e um deslocamento aditivo de $\ln(1{,}2)$; para parametros lineares, uma escala multiplicativa). Manter os demais fixos. Rodar $N = 10.000$ por variacao.
- **Metrica:** variacao percentual de $E[X_{\text{total}}]$ relativa ao caso base.
- **Resultado:** tres parametros dominam, cada um produzindo aproximadamente o mesmo movimento de ±19-20% em $E[X_{\text{total}}]$: a media salarial ($\mu_s$ via $E[S]$), o multiplicador de beneficios ($\beta$) e o headcount ($n$). Todos os tres atuam linearmente sobre o componente salarial, que e ~97% do orcamento. Parametros de horas extras e incidentes mudam o total em menos de 1%. **Implicacao pratica:** invista esforco de modelagem nas tres alavancas salariais; refinar o modelo de horas extras ou incidentes e ruido.

> **Por que "efetivo ±20%" e nao raw ±20%?** O log-media salarial $\mu_s$ entra em $E[S] = e^{\mu_s + \sigma_s^2/2}$ exponencialmente. Variar $\mu_s$ em ±20% aditivamente multiplicaria $E[S]$ por aproximadamente 6,3× — tornando o grafico visualmente dominado por $\mu_s$ por uma razao nao-comercial. O setup corrigido varia o *valor esperado efetivo* de cada componente, entao o ranking reflete sensibilidade de negocio, nao escala do parametro.

![Tornado de Sensibilidade](../figures/sensitivity_tornado.png)
*Figura 5: Impacto dos parametros em $E[X_{\text{total}}]$.*

### Principais Achados

| Metrica | Valor |
|---------|-------|
| $E[X]$ analitico | R$ 11,55M |
| Media MC (N=50K) | Dentro de 0,1% do analitico |
| Semi-amplitude IC 95% (N=50K) | ~R$ 4K |
| Faixa P5-P95 | ~R$ 1,6M |
| P(X excede R$ 12,5M) | ~3% |
| Parametro mais sensivel | Media do componente dominante |
| Melhor reducao de variancia | Variaveis de controle (~30× na variancia, ~5-6× na amplitude do IC) |

Os experimentos confirmam que a engine funciona. A lacuna restante e operacional: transformar uma simulacao validada em um workflow que um gestor de orcamento possa rodar na segunda-feira de manha, apresentar a lideranca sem perder a audiencia, e aplicar a outros tipos de orcamento alem do estudo de caso. E o que o framework pratico oferece.

---

## 10. Um Framework Pratico para Analistas de Orcamento

### Quando Usar Monte Carlo

- **Use MC** quando o orcamento tem componentes estocasticos e voce precisa quantificar risco.
- **Planilha basta** quando tudo e deterministico ou a incerteza e irrelevante para a decisao.

### Fluxo de Trabalho

1. **Decomponha o orcamento** em componentes. Identifique quais tem incerteza significativa.
2. **Escolha distribuicoes** baseadas em dados historicos, julgamento de especialistas ou analogias.
3. **Calcule momentos analiticos** para validacao.
4. **Execute simulacao piloto** ($N = 100$-$500$) para estimar $\sigma$ e computar $N$ necessario.
5. **Execute simulacao completa** com $N$ calculado. Use variaveis de controle se disponiveis.
6. **Reporte como distribuicao:** media, IC, P(acima do teto), percentis.

### A Camada de Decisao: Da Distribuicao a Politica

Uma distribuicao e dado. Uma *politica* e o que torna esse dado acionavel. A passagem de "temos uma distribuicao" para "temos uma regra de decisao" e o que transforma Monte Carlo em uma ferramenta orcamentaria que conduz o ano, nao em um slide que encerra uma reuniao.

**Tres perguntas de politica, tres percentis:**

| Decisao | Pergunta | Onde olhar |
|---------|----------|------------|
| **Quanto reservar?** | "Que orcamento nos cobre em 90% dos cenarios?" | $P_{90}$ da distribuicao de custo |
| **Quando escalar?** | "Que nivel de gasto sinaliza risco de cauda serio?" | $P_{95}$ — cruza-lo dispara revisao |
| **Qual o pior caso plausivel?** | "Como e um ano ruim com 5% de probabilidade?" | $P_{99}$ — limite do colchao de capital |

**Uma regra concreta de decisao** (substitua os valores pelo que sua organizacao aceita):

> **Politica de alocacao de capital.** Reserve $P_{90}$ como orcamento planejado. Mantenha um colchao adicional igual a $P_{99} - P_{90}$ como capital de risco, disponivel mas nao comprometido. Se o gasto realizado cruzar a trajetoria de $P_{95}$ year-to-date, escale para a lideranca para revisao ativa.

Isso converte a distribuicao em tres numeros acionaveis por qualquer gestor de orcamento — e torna explicito o debate implicito de "quanto risco aceitamos?".

**O trade-off risco vs capital.** Percentis maiores reservam mais capital mas travam caixa; percentis menores liberam capital mas elevam a probabilidade de breach no meio do ano. O percentil certo e uma escolha de *negocio*, nao estatistica — mas Monte Carlo e o que permite escolher com numeros anexados.

| Politica | Capital reservado | Probabilidade de breach | Adequada para |
|----------|-------------------|-------------------------|---------------|
| $P_{75}$ | Baixo | 25% | Times com alta liquidez; podem refinanciar no meio do ano |
| $P_{90}$ | Moderado | 10% | **Default para a maioria dos times** |
| $P_{95}$ | Maior | 5% | Ambientes regulados; custo reputacional de breach |
| $P_{99}$ | Alto | 1% | Mission-critical; breach = morte do projeto |

### Como Apresentar Resultados

O momento de maior alavancagem deste artigo inteiro e a linguagem que um gestor de orcamento usa diante da lideranca. Imprima esta comparacao lado a lado e cole na parede.

> **Antes — estimativa pontual:**
>
> *"O orcamento do proximo ano e R$ 11,55M."*
>
> Uma meta. Sem risco anexado. Toda variancia vira um miss.

> **Depois — distribuicao + politica:**
>
> *"Temos 95% de confianca de que o custo ficara entre R$ 10,7M e R$ 12,4M, com media de R$ 11,55M.*
>
> *Propomos reservar R$ 12,0M como orcamento planejado (P90), com R$ 500K adicionais de capital de risco disponiveis se necessario (P99). A probabilidade de ultrapassar R$ 12,5M e aproximadamente 3%. O principal fator de incerteza e [componente dominante] — investir em melhores forecasts de salario reduz a faixa mais que qualquer outra acao."*
>
> Um perfil de risco que a lideranca pode subscrever. Variancias sao lidas contra o *intervalo*, nao a media.

O script "Depois" nao e mais longo porque e mais verboso — e mais longo porque carrega a **informacao que a planilha teve que descartar**. Pratique falar em voz alta.

### Implementacao Minima Viavel (1 Dia)

Voce nao precisa de um pipeline pronto para comecar. A versao minima util deste metodo cabe em um dia util. Use este checklist:

1. **Escolha os 2-3 componentes que dirigem a maior parte do orcamento.** Para headcount: salarios + horas extras + incidentes. Ignore o resto na v1.
2. **Escolha distribuicoes default:**
   - Custos estritamente positivos e assimetricos a direita → **LogNormal**
   - Contagens de eventos raros (incidentes, contratacoes) → **Poisson**
   - Quantidades simetricas e bem conhecidas → **Normal**
3. **Estime parametros a partir dos dados do ano passado** ou julgamento de especialistas. Para LogNormal: $\mu = \ln(\text{mediana})$, $\sigma = $ dispersao log aproximada (comece em 0,3).
4. **Rode $N = 1.000$** simulacoes em Python com `numpy.random.default_rng(42)`. Cerca de cinquenta linhas de codigo.
5. **Reporte tres numeros:** media, $P_{95}$, $P(X \gt \text{teto})$. Esse e o resumo do orcamento.

Se esses numeros forem uteis, voce acabou de ganhar o direito de investir na v2 — mais componentes, variaveis de controle, atualizacoes Bayesianas mensais. Se nao forem uteis, voce gastou um dia e aprendeu quais componentes precisavam de mais cuidado. De qualquer forma, voce esta a frente da planilha.

### Adaptando ao Seu Contexto

| Seu Orcamento | Componente Dominante | Variavel de Controle Natural | Distribuicao Provavel |
|---------------|---------------------|------------------------------|----------------------|
| Headcount | Salarios | Soma bruta de salarios | LogNormal |
| Cloud/Infra | Uso de computacao | Custo de capacidade reservada | LogNormal ou Gamma |
| Projetos | Horas de trabalho | Horas planejadas × taxa | LogNormal |
| Procurement | Precos unitarios | Baseline contratual | Normal ou Uniforme |
| Marketing | Volume de conversao | CPA historico | Poisson × LogNormal |

---

## 11. Conclusao

Um orcamento de numero unico e um **modelo incompleto**. Ele comprime uma distribuicao em seu centro, descarta toda a cauda, e pede a organizacao que tome decisoes de alocacao de capital sobre o que sobrou.

Essa compressao tem custo. Capital fica super-reservado contra medos que ninguem quantificou, ou sub-reservado contra caudas que ninguem enxergou. Variancias de forecast sao lidas como erros, em vez de sorteios de uma distribuicao. O CFO e convidado a subscrever uma meta, nao um risco.

Este artigo construiu a maquinaria matematica para substituir esse numero unico por uma distribuicao de probabilidade. Provamos que o estimador converge (LGN), quantificamos seu erro (TCL) e tornamos a simulacao eficiente (reducao de variancia). A validacao experimental confirmou: Monte Carlo recupera a media analitica dentro de 0,1%, variaveis de controle dao aproximadamente 30× de reducao de variancia (5-6× de IC mais estreito), e o parametro mais sensivel e exatamente o componente de custo dominante — apontando ao analista onde concentrar esforco de modelagem.

Mas a tese mais profunda nao e tecnica. E esta:

> **Um orcamento e uma distribuicao, nao um numero. Variancia e o que quebra planos, nao a media. Simulacao transforma incerteza em risco mensuravel.**

Tres frases. Imprima acima da planilha.

Qualquer orcamento serio deveria ser expresso como uma distribuicao. Qualquer revisao orcamentaria seria deveria perguntar "em que ponto da distribuicao caimos?", nao "quanto erramos?". E qualquer time serio construindo orcamento hoje deveria estar rodando o tipo de simulacao que este artigo descreve — ate segunda-feira, no laptop, em cem linhas de Python.

Da proxima vez que alguem pedir um numero de orcamento, entregue uma distribuicao.

---

## Referencias

1. Casella, G. & Berger, R. (2002). *Statistical Inference*. Duxbury.
2. Robert, C. & Casella, G. (2004). *Monte Carlo Statistical Methods*. Springer.
3. Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering*. Springer.
4. Gelman, A. et al. (2013). *Bayesian Data Analysis*. CRC Press.

---

## Como Reproduzir

```bash
git clone https://github.com/brunoramosmartins/monte-carlo-budget-article.git
cd monte-carlo-budget-article
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,notebook]"
python scripts/exp_budget_simulation.py
python scripts/exp_sensitivity.py
pytest tests/
```

Todas as figuras geradas com seeds fixas para reprodutibilidade exata.
