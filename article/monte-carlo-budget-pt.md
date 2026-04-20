# Por Que o Seu Orcamento Nunca Crava o Valor Exato

## Simulacao Monte Carlo para Planejamento Orcamentario — de Estimativas Pontuais a Distribuicoes de Probabilidade

---

## 1. Introducao

Alguem pede o orcamento do proximo ano. Voce abre uma planilha, multiplica quantidades por custos unitarios, adiciona contingencias, arredonda um pouco para cima — e entrega um numero. Um unico numero.

Mas e se esse numero for apenas uma amostra de uma distribuicao que voce nunca viu?

Toda organizacao que gerencia orcamentos — custos de headcount, despesas de projetos, procurement, marketing — enfrenta o mesmo ritual. O time produz uma estimativa pontual, a lideranca aprova, e o periodo transcorre. Meses depois, durante uma revisao periodica do forecast, os gastos reais divergem. O time ajusta. Outra revisao. Outro ajuste. No final do periodo, o numero original parece pouco mais que um chute educado.

O problema nao e que a estimativa estava errada. O problema e que um numero unico nao carrega informacao sobre sua propria incerteza. Era uma estimativa conservadora? Otimista? Qual a probabilidade de ultrapassar o teto aprovado? A estimativa pontual nao responde — porque descarta tudo exceto o centro da distribuicao.

Este artigo substitui o numero unico por uma **distribuicao de probabilidade**. Usando simulacao Monte Carlo fundamentada na Lei dos Grandes Numeros e no Teorema Central do Limite, transformamos "esperamos gastar R$ 11,5M" em "temos 90% de confianca de que os gastos ficarao entre R$ 10,7M e R$ 12,4M, com 7% de probabilidade de ultrapassar o teto."

A abordagem e **geral**: aplica-se a qualquer orcamento que possa ser decomposto em componentes estocasticos — headcount, projetos, procurement, licenciamento, infraestrutura. Ilustramos com um orcamento de headcount de TI (salarios, beneficios, horas extras, incidentes) como estudo de caso concreto, mas o framework matematico se transfere diretamente para qualquer dominio.

A jornada segue quatro estagios: formalizamos componentes orcamentarios como variaveis aleatorias (Secao 3), provamos que a media das simulacoes converge para a resposta verdadeira (Secao 4), quantificamos o erro da simulacao (Secao 5), e implementamos o estimador com tecnicas de reducao de variancia (Secoes 6-7). A Secao 9 valida tudo experimentalmente.

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

### O Padrao Geral

Qualquer orcamento com componentes incertos pode ser escrito como:

$$
X_{\text{total}} = \sum_{k=1}^{K} g_k(\mathbf{Z}_k)
$$

onde $g_k$ e uma funcao de custo para o componente $k$ e $\mathbf{Z}_k$ e um vetor de entradas aleatorias. A estimativa pontual colapsa cada $g_k$ para seu valor esperado; Monte Carlo preserva a distribuicao conjunta completa.

---

## 3. Componentes Orcamentarios como Variaveis Aleatorias

Cada componente de um orcamento e potencialmente uma variavel aleatoria. Trata-los como constantes e uma escolha de modelagem que descarta informacao. O insight chave: **identifique quais componentes carregam incerteza significativa, modele-os probabilisticamente, e mantenha o restante deterministico.**

### A Estrutura Geral

Um modelo orcamentario estocastico tem tres tipos de componentes:

1. **Custos proporcionais:** quantidade × taxa, onde um ou ambos podem ser aleatorios
2. **Custos fixos com incerteza:** estrutura conhecida mas magnitude incerta
3. **Eventos raros:** contagem aleatoria de ocorrencias × custo aleatorio por evento (processo composto)

$$
X_{\text{total}} = \underbrace{\sum_{i=1}^{n} f(Z_i)}_{\text{proporcional}} + \underbrace{\text{componentes fixos}}_{\text{deterministico}} + \underbrace{\sum_{j=1}^{N_{\text{eventos}}} C_j}_{\text{eventos raros}}
$$

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

---

## 5. Quao Errados Podemos Estar? O Teorema Central do Limite

A LGN nos diz que converge. O TCL nos diz **quao rapido** — e da intervalos de confianca.

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

### Erro Quadratico Medio

$\text{EQM}(\hat{\theta}_N) = \sigma_g^2 / N$ (estimador nao-viesado).

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

**No estudo de caso:** usando soma bruta de salarios como controle ($\rho \approx 0,99$) da ~50× de reducao. Em qualquer orcamento, o componente dominante com media analitica conhecida e a variavel de controle natural.

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

---

## 8. Uma Alternativa Bayesiana

A abordagem frequentista assume um modelo fixo e simula. A Bayesiana trata parametros como variaveis aleatorias e atualiza crencas com dados:

$$
P(\theta \mid \text{dados}) \propto P(\text{dados} \mid \theta) \cdot P(\theta)
$$

No orcamento: **priori** = distribuicao do periodo anterior, **verossimilhanca** = gastos observados, **posteriori** = forecast atualizado. Cada revisao periodica e atualizacao Bayesiana informal.

| Aspecto | MC Frequentista | Bayesiano |
|---------|----------------|-----------|
| Parametros | Constantes fixas | Variaveis aleatorias |
| Informacao previa | Nao usada | Codificada explicitamente |
| Saida | Intervalo de confianca | Intervalo de credibilidade |
| Atualizacao no periodo | Requer re-especificacao | Natural (posteriori → nova priori) |
| Melhor quando | Sem dados historicos; exploracao de cenarios | Dados historicos disponiveis; revisao sequencial |

Este artigo usa a abordagem frequentista por generalidade, clareza pedagogica e simplicidade pratica. A extensao Bayesiana e o proximo passo natural para equipes com historico.

---

## 9. Experimentos e Resultados

### Experimento A: Convergencia da LGN

Dez execucoes convergem para $E[X]$ (Figura 1). Em $N$ pequeno, ampla dispersao; em $N = 5.000$, todas agrupadas dentro de R$ 200 da media analitica.

### Experimento B: Normalidade do TCL

Media padronizada visivelmente nao-Normal em $n = 1$, proxima de $N(0,1)$ em $n = 30$ (Figura 2). QQ-plots: $R^2 > 0,999$ em $n = 100$.

### Experimento C: Simulacao Completa

$N = 50.000$ iteracoes:

![Simulacao do Orcamento](../figures/budget_simulation.png)
*Figura 4: Distribuicao (histograma + FDA) com media, P5/P95 e teto anotados.*

Recupera $E[X]$ analitico dentro de 0,1%. Distribuicao assimetrica a direita, faixa P5-P95 de ~R$ 1,6M.

### Experimento D: Reducao de Variancia

Variaveis de controle reduzem amplitude do IC em ~10× vs MC simples (Figura 3).

### Experimento E: Analise de Sensibilidade

![Tornado de Sensibilidade](../figures/sensitivity_tornado.png)
*Figura 5: Impacto dos parametros em $E[X_{\text{total}}]$.*

Parametros do componente dominante (log-media salarial, headcount) geram a maior parte da variancia. **Implicacao pratica:** invista esforco em estimar os parametros do seu maior componente de custo.

### Principais Achados

| Metrica | Valor |
|---------|-------|
| $E[X]$ analitico | R$ 11,55M |
| Media MC (N=50K) | Dentro de 0,1% do analitico |
| Semi-amplitude IC 95% (N=50K) | ~R$ 4K |
| Faixa P5-P95 | ~R$ 1,6M |
| Parametro mais sensivel | Media do componente dominante |
| Melhor reducao de variancia | Variaveis de controle (~10-50×) |

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

### Como Apresentar

Substitua:

> "O orcamento do proximo ano e R$ 11,55M."

Por:

> "Temos 95% de confianca de que o custo ficara entre R$ 10,7M e R$ 12,4M (media R$ 11,55M). Ha ~7% de probabilidade de ultrapassar o teto de R$ 12,5M. O principal fator de incerteza e [componente dominante]."

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

Uma estimativa pontual de orcamento e uma unica amostra de uma distribuicao desconhecida. Nao carrega informacao sobre sua propria incerteza.

Este artigo construiu a maquinaria matematica para substituir esse numero unico por uma distribuicao de probabilidade completa. Partindo da definicao de variaveis aleatorias, provamos convergencia (LGN), quantificamos a taxa de convergencia (TCL), formalizamos o estimador Monte Carlo e aplicamos reducao de variancia.

O framework e geral: qualquer orcamento decomponivel em componentes estocasticos — headcount, projetos, infraestrutura, procurement — pode ser modelado assim. A validacao experimental confirmou que Monte Carlo recupera valores analiticos, o TCL fornece ICs calibrados, e variaveis de controle dao melhoria de ordem de grandeza.

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
