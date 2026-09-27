# DCA + diseño del portafolio (base $10,000)

Simulación educativa del mix de largo plazo usado en eToro (@Andalejo1109): cómo un portafolio **no elimina** la volatilidad, la **suaviza**. El día rojo hace ruido. El plan no debería.

Curva: **buy & hold** de $10,000 el 3 de enero de 2022, **sin aportes extra**.  
El DCA entra en el proceso (aporte quincenal), no en esta línea. Así se ve solo el camino de los precios.

![Frame final](portafolio_dca_suaviza.png)

[GIF animado (2022 → 2026)](portafolio_dca_suaviza.gif)

---

## Qué muestra el gráfico

Arriba: $10,000 iniciales caminando hasta el 25-sep-2026.  
Abajo: boxplot de **retornos diarios**. SMH tiene la caja más ancha y las colas más largas. El mix recorta esa cola **hacia abajo y hacia arriba**.

| Activo | Rol | De $10,000 a |
| :--- | :--- | ---: |
| SMH | Motor (semiconductores) | **$39,405** |
| **Portafolio** | Mix buy & hold | **$21,717** |
| SPYG | Crecimiento USA | $17,649 |
| VOO | Referencia S&P 500 (no entra al mix) | $17,250 |
| BRK.B | Valor / disciplina de capital | $16,805 |
| VTI | Mercado total USA | $16,653 |
| IEMG | Emergentes | $15,506 |

Piso de 2022 (aprox.): SMH ~$5,500 · portafolio ~$7,100.

---

## Pesos del mix

Publicados el 18-sep-2026. VOO no pondera.

| Ticker | Peso |
| :---: | ---: |
| SPYG | 32% |
| SMH | 21% |
| IEMG | 20% |
| BRK.B | 20% |
| VTI | 8% |

Regla de la curva: buy & hold con esos pesos **iniciales**. No hay rebalanceo diario.

---

## Conclusiones del post

1. **El día no decide.** Un martes en rojo no cambia el aporte quincenal. El DCA compra cuando duele y cuando sobra euforia. Quita la peor pregunta: “¿entro ahora o espero?”.
2. **Suavizar también recorta los días buenos.** SMH gana la foto ($39,405). El mix no. A cambio, la cola diaria es más corta y 2022 se vuelve habitable.
3. **Diversificar no es “evitar volatilidad”.** Es que un solo ticker no defina el ánimo ni el plan.
4. **Cinco años es el mínimo para juzgar la tesis.** Lo que pasa en una semana es ruido. El gráfico parte de 2022 justo por eso: incluye el año feo, no solo el rally.
5. **La tesis operativa se mantiene:** cero apalancamiento, cero vender por un titular, el aporte sale igual.

---

## Cómo regenerar

```bash
python3 -m pip install yfinance pandas matplotlib pillow numpy
python3 make_portfolio_gif.py
```

Salida en la misma carpeta:

- `portafolio_dca_suaviza.gif` — la curva se dibuja en el tiempo
- `portafolio_dca_suaviza.png` — frame final (útil si eToro congela el GIF)
- `data/prices_clean.csv` — cache de precios ajustados (Yahoo)

---

## Aviso

Material educativo. Rentabilidades pasadas no predicen las futuras. No es una recomendación personal ni una oferta de inversión.
