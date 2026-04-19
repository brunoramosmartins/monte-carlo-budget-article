# Por Que o Seu Orcamento Nunca Crava o Valor Exato

## Simulacao Monte Carlo para Planejamento Orcamentario de TI — de Estimativas Pontuais a Distribuicoes de Probabilidade

---

## 1. Introducao

Seu CFO pede o orcamento de headcount de TI para o proximo ano. Voce abre uma planilha, multiplica o numero de funcionarios pelo salario medio, soma o multiplicador de beneficios, joga uma estimativa de horas extras, arredonda para cima por conta de incidentes — e entrega um numero. Um unico numero. R$ 11,5 milhoes.

Mas e se esse numero for apenas uma amostra de uma distribuicao que voce nunca viu?

Toda organizacao que gerencia orcamentos de headcount — salarios, beneficios, horas extras, custos nao planejados — enfrenta o mesmo ritual. O time produz uma estimativa pontual, a lideranca aprova, e o ano transcorre. Meses depois, durante uma revisao de FYF (Forecast Year-end Financial), os gastos reais divergem da previsao. O time ajusta. Outra revisao. Outro ajuste. No final do ano, o numero original parece pouco mais que um chute educado.

O problema nao e que a estimativa estava errada. O problema e que um numero unico nao carrega informacao sobre sua propria incerteza. R$ 11,5M era uma estimativa conservadora? Otimista? Qual a probabilidade de ultrapassarmos R$ 12,5M? A estimativa pontual nao consegue responder essas perguntas — porque ela descarta tudo exceto o centro da distribuicao.

Este artigo substitui o numero unico por uma **distribuicao de probabilidade**. Usando simulacao Monte Carlo fundamentada na Lei dos Grandes Numeros e no Teorema Central do Limite, transformamos "esperamos gastar R$ 11,5M" em "temos 90% de confianca de que os gastos ficarao entre R$ 10,7M e R$ 12,4M, com 7% de probabilidade de ultrapassar o teto de R$ 12,5M."

A jornada matematica segue quatro estagios: formalizamos os componentes do orcamento como variaveis aleatorias (Secao 3), provamos que a media das simulacoes converge para a resposta verdadeira (Secao 4), quantificamos o erro da simulacao (Secao 5) e implementamos o estimador com tecnicas de reducao de variancia (Secoes 6-7). A Secao 9 valida tudo experimentalmente.

### Notacao

| Simbolo | Significado |
|---------|-------------|
| $S_i$ | Salario mensal do funcionario $i$ |
| $\beta$ | Multiplicador de beneficios (encargos) |
| $n$ | Numero de funcionarios (headcount) |
| $H_i$ | Horas extras por funcionario por mes |
| $r_{ot}$ | Valor da hora extra |
| $I$ | Numero de incidentes graves por ano |
| $C_j$ | Custo do incidente $j$ |
| $X_{\text{total}}$ | Custo orcamentario total anual |
| $\bar{X}_N$ | Media amostral de $N$ simulacoes |
| $\hat{\theta}_N$ | Estimador Monte Carlo |

---

## 2. O Problema da Estimativa Pontual

Uma estimativa pontual e um valor unico usado para aproximar um parametro desconhecido. No planejamento orcamentario, ela toma a forma:

$$
\hat{X} = n \times \bar{S} \times \beta \times 12 + \text{horas extras} + \text{incidentes}
$$

onde $\bar{S}$ e o salario medio e todo o resto e constante. O resultado e um numero — digamos, R$ 11.554.473.

Mas esse numero e $E[X_{\text{total}}]$: o valor esperado de uma variavel aleatoria. Ele nos diz o centro da distribuicao. O que ele descarta e todo o resto:

- **Variancia:** Quao dispersos sao os resultados possiveis?
- **Assimetria:** A distribuicao e simetrica, ou custos podem ser puxados para cima por alguns salarios extremos?
- **Risco de cauda:** Qual a probabilidade de ultrapassar o orcamento aprovado?
- **Confianca:** Quao certos estamos de que o custo verdadeiro esta dentro de ±R$ 500K da nossa estimativa?

Em termos formais, a estimativa pontual nos da $E[X]$ mas nao a distribuicao $F_X$. A simulacao Monte Carlo recupera $F_X$ — o quadro completo.

---

## 3. Variaveis Aleatorias Disfarcadas

Cada componente do orcamento e uma variavel aleatoria. Trata-los como constantes e uma escolha de modelagem que descarta informacao.

### Salarios: LogNormal

Salarios em um time de TI com senioridades mistas sao estritamente positivos e assimetricos a direita: a maioria dos funcionarios ganha perto da mediana, mas alguns engenheiros senior ou gestores ganham significativamente mais. A distribuicao LogNormal captura isso:

$$
S_i \sim \text{LogNormal}(\mu_s, \sigma_s^2)
$$

Com parametros $\mu_s = 9,2$ e $\sigma_s = 0,3$, o salario mensal esperado e:

$$
E[S_i] = e^{\mu_s + \sigma_s^2/2} = e^{9,245} \approx R\$ \, 10.362
$$

A variancia e:

$$
\text{Var}(S_i) = (e^{\sigma_s^2} - 1) \cdot e^{2\mu_s + \sigma_s^2} \approx 10.117.947
$$

### Horas Extras: Poisson

Horas extras por funcionario por mes sao discretas, nao-negativas e relativamente raras — um ajuste natural para a distribuicao de Poisson:

$$
H_i \sim \text{Poisson}(\lambda_h), \quad \lambda_h = 5
$$

Propriedade chave: para Poisson, $E[H_i] = \text{Var}(H_i) = \lambda_h$.

### Incidentes: Poisson Composto

Incidentes graves — indisponibilidades, falhas de seguranca, deployments emergenciais — ocorrem a uma taxa aleatoria com severidade aleatoria:

$$
I \sim \text{Poisson}(\lambda_I), \quad C_j \sim \text{LogNormal}(\mu_I, \sigma_I^2)
$$

O custo total de incidentes e uma **soma aleatoria de variaveis aleatorias**: $\sum_{j=1}^I C_j$.

### O Modelo de Custo Total

Combinando todos os componentes:

$$
X_{\text{total}} = \underbrace{\sum_{i=1}^{n} S_i \cdot \beta \cdot 12}_{\text{salarios + beneficios}} + \underbrace{\sum_{i=1}^{n} H_i \cdot r_{ot} \cdot 12}_{\text{horas extras}} + \underbrace{\sum_{j=1}^{I} C_j}_{\text{incidentes}}
$$

Usando linearidade da esperanca (que vale independentemente de correlacao):

$$
E[X_{\text{total}}] = n \cdot \beta \cdot 12 \cdot E[S_i] + n \cdot r_{ot} \cdot 12 \cdot E[H_i] + E[I] \cdot E[C_j]
$$

Com parametros padrao ($n = 50$, $\beta = 1,80$, $r_{ot} = 80$, $\lambda_I = 3$):

$$
E[X_{\text{total}}] \approx 11.191.000 + 240.000 + 123.500 \approx R\$ \, 11.554.500
$$

O componente salarial domina com ~97% do total. Isso sera importante para reducao de variancia mais adiante.

---

## 4. A Media Vai Convergir? A Lei dos Grandes Numeros

Se simularmos o orcamento 10.000 vezes e calcularmos a media dos resultados, essa media convergira para o verdadeiro $E[X_{\text{total}}]$? A Lei dos Grandes Numeros diz que sim.

### Desigualdade de Chebyshev

Para qualquer variavel aleatoria $X$ com media $\mu$ e variancia $\sigma^2$:

$$
P(|X - \mu| \geq \epsilon) \leq \frac{\sigma^2}{\epsilon^2}
$$

Derivada da desigualdade de Markov aplicada a $(X - \mu)^2$.

### A Lei Fraca dos Grandes Numeros

Sejam $X_1, \ldots, X_N$ i.i.d. com media $\mu$ e variancia $\sigma^2$. A media amostral $\bar{X}_N = \frac{1}{N}\sum X_i$ satisfaz:

$$
P(|\bar{X}_N - \mu| \geq \epsilon) \leq \frac{\sigma^2}{N\epsilon^2} \to 0 \quad \text{quando } N \to \infty
$$

**Demonstracao.** Como $E[\bar{X}_N] = \mu$ e $\text{Var}(\bar{X}_N) = \sigma^2/N$, aplicar Chebyshev a $\bar{X}_N$ da o resultado imediatamente. $\blacksquare$

A Lei Forte dos Grandes Numeros oferece garantia ainda mais forte: $\bar{X}_N \to \mu$ quase certamente, significando que a convergencia ocorre com probabilidade 1.

**Para Monte Carlo:** cada simulacao $X_i$ e um "ano possivel." A LGN garante que a media de $N$ anos simulados converge para o custo esperado verdadeiro. A Figura 1 demonstra isso visualmente.

![Convergencia LGN](../figures/lln_convergence.png)
*Figura 1: Dez execucoes independentes da media amostral convergindo para $E[S]$, com banda de confianca de Chebyshev a 95%.*

---

## 5. Quao Errados Podemos Estar? O Teorema Central do Limite

A LGN nos diz que o estimador converge. O TCL nos diz **quao rapido** — e nos da intervalos de confianca.

### Enunciado

Para variaveis i.i.d. com media $\mu$ e variancia $\sigma^2$:

$$
\frac{\sqrt{N}(\bar{X}_N - \mu)}{\sigma} \xrightarrow{d} N(0, 1)
$$

### Esboco da Demonstracao (via FGM)

Defina $W_i = (X_i - \mu)/\sigma$ de modo que $E[W_i] = 0$ e $\text{Var}(W_i) = 1$. A soma padronizada e $Z_N = \frac{1}{\sqrt{N}}\sum W_i$. Sua FGM e:

$$
M_{Z_N}(t) = \left[M_W\left(\frac{t}{\sqrt{N}}\right)\right]^N
$$

Expandindo $\log M_W(s) = s^2/2 + O(s^3)$ em Taylor e substituindo $s = t/\sqrt{N}$:

$$
\log M_{Z_N}(t) = N \cdot \left[\frac{t^2}{2N} + O\left(\frac{t^3}{N^{3/2}}\right)\right] = \frac{t^2}{2} + O\left(\frac{t^3}{\sqrt{N}}\right) \to \frac{t^2}{2}
$$

Como $e^{t^2/2}$ e a FGM de $N(0, 1)$, o teorema de unicidade da $Z_N \xrightarrow{d} N(0, 1)$. $\blacksquare$

### Intervalos de Confianca

Pelo TCL, o intervalo de confianca $(1-\alpha)$ para $\mu$ e:

$$
\bar{X}_N \pm z_{\alpha/2} \cdot \frac{s_N}{\sqrt{N}}
$$

onde $s_N$ e o desvio padrao amostral e $z_{\alpha/2}$ e o quantil da Normal (1,96 para 95%).

### Escolhendo N

Para obter um intervalo com semi-amplitude $\epsilon$:

$$
N \geq \left(\frac{z_{\alpha/2} \cdot \sigma}{\epsilon}\right)^2
$$

Para nosso orcamento ($\sigma \approx 493K$, $\epsilon = 100K$, 95% de confianca): $N \geq (1,96 \times 493.000 / 100.000)^2 \approx 94$. O TCL e notavelmente eficiente.

![Emergencia de Normalidade - TCL](../figures/clt_normality_emergence.png)
*Figura 2: Conforme $n$ aumenta, a media padronizada de salarios LogNormal converge para $N(0,1)$.*

---

## 6. O Estimador Monte Carlo

### Definicao

O estimador Monte Carlo de $\theta = E[g(X)]$ e:

$$
\hat{\theta}_N = \frac{1}{N} \sum_{i=1}^N g(X_i)
$$

onde cada $g(X_i)$ e o custo total de um ano simulado.

### Propriedades

**Nao-viesado.** $E[\hat{\theta}_N] = \frac{1}{N}\sum E[g(X_i)] = \theta$. O estimador nao tem vies sistematico.

**Consistente.** Pela LGN Fraca: $\hat{\theta}_N \xrightarrow{P} \theta$. Mais simulacoes significa mais precisao.

**Normalidade assintotica.** Pelo TCL: $\sqrt{N}(\hat{\theta}_N - \theta)/\sigma_g \xrightarrow{d} N(0, 1)$. Podemos construir intervalos de confianca.

**Taxa de convergencia.** O erro padrao e $\text{EP} = \sigma_g / \sqrt{N}$, que decai como $O(1/\sqrt{N})$. Crucialmente, essa taxa e **independente da dimensao** de $X$ — diferente de metodos de integracao deterministica que sofrem da maldicao da dimensionalidade.

### A Lei de Escala

Reduzir pela metade a amplitude do IC requer 4× mais simulacoes. Ir de ±R$ 100K para ±R$ 50K significa quadruplicar $N$. Esse trade-off fundamental motiva a reducao de variancia.

### Erro Quadratico Medio

Como o estimador e nao-viesado:

$$
\text{EQM}(\hat{\theta}_N) = \text{Var}(\hat{\theta}_N) = \frac{\sigma_g^2}{N}
$$

---

## 7. Tornando Mais Rapido: Reducao de Variancia

A taxa $O(1/\sqrt{N})$ significa que precisao por forca bruta e cara. Tecnicas de reducao de variancia alcancam intervalos de confianca mais estreitos **para o mesmo custo computacional**.

### Variaveis de Controle

Se conhecemos $E[h(X)]$ analiticamente para alguma funcao $h$ correlacionada com $g$, podemos corrigir nosso estimador:

$$
\hat{\theta}_{CV} = \hat{\theta}_N - c^*\left(\bar{h}_N - E[h(X)]\right)
$$

O coeficiente otimo minimiza a variancia:

$$
c^* = \frac{\text{Cov}(g(X), h(X))}{\text{Var}(h(X))}
$$

No coeficiente otimo $c^*$, a variancia se torna:

$$
\text{Var}(\hat{\theta}_{CV}) = \frac{\text{Var}(g(X))}{N}(1 - \rho_{g,h}^2)
$$

onde $\rho_{g,h}$ e a correlacao entre $g$ e $h$.

**Para nosso modelo de orcamento:** usando $h(X) = \sum S_i$ (soma bruta de salarios, com media analitica conhecida) como variavel de controle, obtemos $\rho \approx 0,99$, reduzindo a variancia por um fator de ~$(1 - 0,99^2) \approx 0,02$ — uma melhoria de aproximadamente **50×**.

### Variaveis Antiteticas

Gere pares $(X_i, X_i')$ onde $X_i' = F^{-1}(1 - F(X_i))$ e o "espelho" de $X_i$. O estimador usa medias par a par:

$$
\hat{\theta}_{AV} = \frac{1}{N/2}\sum_{i=1}^{N/2} \frac{g(X_i) + g(X_i')}{2}
$$

Se $g$ e monotona, $\text{Cov}(g(X), g(X')) < 0$, e a variancia e reduzida.

### Amostragem Estratificada

Particione o espaco de entrada em $K$ estratos, amostre proporcionalmente dentro de cada um e combine. Pela lei da variancia total:

$$
\text{Var}(\hat{\theta}_{SS}) = \frac{1}{N}\sum_k p_k \sigma_k^2 \leq \frac{\sigma^2}{N} = \text{Var}(\hat{\theta}_{MC})
$$

A estratificacao remove a variancia entre estratos, que e sempre nao-negativa.

![Comparacao de Reducao de Variancia](../figures/variance_reduction_comparison.png)
*Figura 3: Amplitude do IC vs N para MC simples, variaveis antiteticas e variaveis de controle. Variaveis de controle dominam.*

---

## 8. Uma Alternativa Bayesiana

A abordagem frequentista de Monte Carlo assume um modelo fixo e simula a partir dele. A abordagem Bayesiana trata parametros desconhecidos como variaveis aleatorias e atualiza crencas conforme dados chegam:

$$
P(\theta \mid \text{dados}) \propto P(\text{dados} \mid \theta) \cdot P(\theta)
$$

No contexto orcamentario: a **priori** e a distribuicao de custos do ano passado, a **verossimilhanca** sao os dados de gastos deste ano, e a **posteriori** e a previsao atualizada. Cada revisao de FYF e, na pratica, uma atualizacao Bayesiana informal.

| Aspecto | MC Frequentista | Bayesiano |
|---------|----------------|-----------|
| Parametros | Constantes fixas | Variaveis aleatorias |
| Informacao a priori | Nao utilizada | Explicitamente codificada |
| Saida | Intervalo de confianca | Intervalo de credibilidade |
| Interpretacao | Frequencia de longo prazo | Probabilidade sobre $\theta$ |
| Atualizacao no meio do ano | Requer re-especificacao | Natural (posteriori → nova priori) |

Este artigo utiliza a abordagem frequentista por sua generalidade (nao requer elicitacao de priori), clareza pedagogica e simplicidade pratica. A extensao Bayesiana e um proximo passo natural para equipes com dados historicos de orcamento.

---

## 9. Experimentos e Resultados

### Experimento A: Convergencia da LGN

Dez execucoes independentes da media amostral de salarios convergem para $E[S]$ conforme $N$ cresce (Figura 1). Em $N$ pequeno, as execucoes se espalham amplamente; em $N = 5.000$, todas se agrupam dentro de R$ 200 da media analitica.

### Experimento B: Normalidade do TCL

A media padronizada de salarios LogNormal e visivelmente nao-Normal em $n = 1$ mas se aproxima de $N(0,1)$ em $n = 30$ (Figura 2). Graficos QQ confirmam: $R^2 > 0,999$ em $n = 100$.

### Experimento C: Simulacao Completa do Orcamento

Executando $N = 50.000$ iteracoes com parametros padrao:

![Simulacao do Orcamento](../figures/budget_simulation.png)
*Figura 4: Distribuicao do custo orcamentario (esquerda: histograma, direita: FDA) com media, P5/P95 e teto orcamentario anotados.*

A simulacao recupera o $E[X_{\text{total}}] \approx R\$ \, 11,55M$ analitico dentro de 0,1%. A distribuicao e assimetrica a direita (puxada pelos salarios LogNormal), com amplitude de 90% abrangendo aproximadamente R$ 1,6M.

### Experimento D: Reducao de Variancia

Em $N = 5.000$, variaveis de controle reduzem a amplitude do IC de 95% em aproximadamente 10× comparado ao MC simples (Figura 3). O poder das variaveis de controle vem da alta correlacao ($\rho \approx 0,99$) entre custo total e soma bruta de salarios.

### Experimento E: Analise de Sensibilidade

Quais parametros importam mais? Variando cada parametro em ±20%:

![Grafico Tornado de Sensibilidade](../figures/sensitivity_tornado.png)
*Figura 5: Grafico tornado mostrando impacto dos parametros em $E[X_{\text{total}}]$.*

O log-media salarial $\mu_s$ e o headcount $n$ dominam. O multiplicador de beneficios $\beta$ tem impacto proporcional. Parametros de horas extras e incidentes tem efeito negligenciavel no total esperado — consistente com sua participacao de ~3% no orcamento.

**Implicacao pratica:** melhorar a estimativa do salario medio importa muito mais do que refinar premissas de horas extras ou incidentes.

### Principais Achados

| Metrica | Valor |
|---------|-------|
| $E[X_{\text{total}}]$ analitico | R$ 11,55M |
| Media MC (N=50K) | Dentro de 0,1% do analitico |
| Semi-amplitude do IC 95% (N=50K) | ~R$ 4K |
| Faixa P5-P95 | ~R$ 1,6M |
| Parametro mais sensivel | $\mu_s$ (log-media salarial) |
| Melhor reducao de variancia | Variaveis de controle (~10-50×) |

---

## 10. Um Framework Pratico para Analistas de Orcamento

### Quando Usar Monte Carlo

- **Use MC** quando o orcamento tem componentes estocasticos (headcount variavel, horas extras incertas, incidentes imprevisiveis) e voce precisa quantificar risco.
- **Uma planilha basta** quando todos os componentes sao verdadeiramente deterministicos ou quando a incerteza e irrelevante para a decisao.

### Fluxo de Trabalho Recomendado

1. **Defina o modelo.** Identifique quais componentes do orcamento sao aleatorios e escolha distribuicoes baseadas em dados historicos ou julgamento de especialistas.
2. **Calcule momentos analiticos.** Calcule $E[X]$ e $\text{Var}(X)$ para validacao.
3. **Execute uma simulacao piloto** ($N = 100$-$500$) para estimar $\sigma$ e determinar o $N$ necessario para a precisao desejada.
4. **Execute a simulacao completa** com o $N$ calculado. Use variaveis de controle se uma boa variavel de controle existir.
5. **Reporte resultados** como uma distribuicao: media, IC, P(acima do teto) e percentis chave.

### Como Apresentar Resultados

Substitua:

> "O orcamento de headcount de TI para o proximo ano e R$ 11,55M."

Por:

> "Temos 95% de confianca de que o custo de headcount de TI ficara entre R$ 10,7M e R$ 12,4M, com media de R$ 11,55M. Ha aproximadamente 7% de probabilidade de ultrapassar o teto de R$ 12,5M. O principal direcionador de incerteza e a variancia salarial."

---

## 11. Conclusao

Uma estimativa pontual de orcamento e uma unica amostra de uma distribuicao desconhecida. Ela nao carrega informacao sobre sua propria incerteza.

Este artigo construiu a maquinaria matematica para substituir esse numero unico por uma distribuicao de probabilidade completa. Partindo da definicao de variaveis aleatorias, provamos que a media de simulacoes independentes converge para o custo esperado verdadeiro (Lei dos Grandes Numeros), quantificamos a taxa de convergencia (Teorema Central do Limite), formalizamos o estimador Monte Carlo e suas propriedades, e aplicamos tecnicas de reducao de variancia para tornar a simulacao eficiente.

A validacao experimental confirmou: Monte Carlo recupera o valor esperado analitico, o TCL fornece intervalos de confianca calibrados, e variaveis de controle proporcionam uma melhoria de ordem de grandeza na precisao.

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

Todas as figuras sao geradas com seeds fixas para reprodutibilidade exata.
