# EXPERIMENTO 154 — Guia de Personagens no Leonardo AI
## Como criar e manter consistência visual de personagens

---

## COMO FUNCIONA O CHARACTER REFERENCE NO LEONARDO AI

O Character Reference é uma função do Leonardo AI que permite fixar a aparência de um personagem. Você gera uma imagem de referência e depois usa ela como âncora para todas as outras cenas.

**Fluxo de trabalho:**
1. Gerar o **Hero Shot** de cada personagem (imagem de referência definitiva)
2. Nas cenas seguintes, carregar essa imagem em **Character Reference**
3. Ajustar a força (strength) entre 60–80%
4. Escrever o prompt da cena específica

**Modelo recomendado:** Phoenix ou Flux Dev (ambos disponíveis no Leonardo)

---

## ZACK ALVAREZ — 14 ANOS

### Descrição visual completa (base de todos os prompts)
```
Latino teenage boy, 14 years old, medium height slim build for his age, 
messy black hair in social cut style (neat but disheveled as if quickly fixed), 
warm brown eyes, light olive skin, small scar on chin, 
slightly serious expression, determined look
```

---

### PASSO 1 — Hero Shot (imagem de referência)

Gere esta imagem primeiro. Ela vai ser o rosto fixo do Zack para toda a série.

```
Latino teenage boy, 14 years old, medium height slim build, 
messy black hair in social cut style neat but disheveled, warm brown eyes, 
light olive skin, small scar on chin, wearing dark t-shirt, 
neutral determined expression, facing camera slightly turned three-quarter angle, 
clean simple background, soft natural lighting, 
sharp focus on face, photorealistic, cinematic portrait, ultra-detailed, 
no watermark, no text
```

**Configurações no Leonardo:**
- Modelo: Phoenix
- Proporção: 3:4 (retrato)
- Guidance: 7
- Gerar 4 variações → escolher a melhor → salvar como referência

---

### PASSO 2 — Prompts de cena com Character Reference

**Após gerar o Hero Shot, carregue-o em "Character Reference" com strength 70%.**

---

#### ZACK — Cena: Pedalando para casa (Ep 01, Cena 3)
```
[CHARACTER REF: Zack hero shot, strength 70%]

Latino teenage boy on simple bicycle riding on tree-lined sidewalk of small 
Brazilian city, wearing dark t-shirt and school backpack, one earbud in, 
relaxed confident posture, afternoon golden hour sunlight, 
wide cinematic shot, muted warm tones, photorealistic, ultra-detailed, 16:9
```

---

#### ZACK — Cena: Pedalando perto do lago (Ep 01, Cena 4)
```
[CHARACTER REF: Zack hero shot, strength 70%]

Latino teenage boy riding bicycle slowly on dirt road alongside 
a calm blue lake, looking toward the water with peaceful expression, 
wearing dark t-shirt and backpack, afternoon golden light reflecting on lake, 
white heron on shore in background, wide cinematic shot, 
muted warm golden tones, photorealistic, ultra-detailed, 16:9
```

---

#### ZACK — Cena: Vendo TV alarmado (Ep 01, Cena 7)
```
[CHARACTER REF: Zack hero shot, strength 70%]

Latino teenage boy sitting upright on old sofa leaning toward television, 
expression shifting from relaxed to alarmed and confused, 
wearing dark t-shirt, TV blue light illuminating his face in darkening room, 
forgotten biscuit in hand, close-up portrait shot, 
cool blue TV light mixed with warm ambient room light, 
cinematic, photorealistic, ultra-detailed
```

---

#### ZACK — Cena: Flash de luz na janela (Ep 01, Cena 8)
```
[CHARACTER REF: Zack hero shot, strength 70%]

Latino teenage boy standing at window of rustic wooden cabin, 
looking out at dense forest, expression of confusion and unease, 
wearing dark t-shirt, intense white-blue silent flash light coming through 
the window illuminating his face from outside, 
medium shot from inside the room, 
muted tones with stark white light contrast, cinematic, photorealistic, ultra-detailed
```

---

#### ZACK — Cena: Rádio na mão olhando fumaça (Ep 01, Cena 12 — CENA FINAL)
```
[CHARACTER REF: Zack hero shot, strength 70%]

Latino teenage boy 14 years old standing in backyard of rustic wooden cabin 
at dusk, holding radio communicator pressed to his chest with both hands, 
looking toward forest horizon where dark smoke rises slowly, 
wearing dark t-shirt, expression of fear crystallizing into decision, 
bicycle visible leaning against cabin porch in background, 
wide cinematic shot from slightly behind and to the side, 
dusk purple-orange light fading to cool, 
muted cool tones, photorealistic, ultra-detailed, 16:9
```

---

#### ZACK — Cena: Chegando ao posto destruído (Ep 02)
```
[CHARACTER REF: Zack hero shot, strength 70%]

Latino teenage boy on bicycle arriving at forest ranger surveillance post, 
stopping at entrance with shocked expression, old car crashed into burning tree 
visible in background, smoke in air, dark bloodstain trail on ground, 
late afternoon light turning red, wide shot, 
muted dark warm tones, post-apocalyptic atmosphere, photorealistic, ultra-detailed
```

---

#### ZACK — Cena: Segurando a mão de Mariluz (Ep 02 — cena mais emocional)
```
[CHARACTER REF: Zack hero shot, strength 75%]

Latino teenage boy kneeling beside wounded Latina woman in forest ranger 
uniform slumped against wall of rustic interior, holding her hand with both his, 
expression of devastation and desperate love, 
three guards' bodies visible blurred in background, 
low dramatic lighting from one window source, 
extreme emotional close-up, tears on his face, 
muted dark tones, cinematic, photorealistic, ultra-detailed
```

---

## NINA — 15 ANOS

### Descrição visual completa
```
Black Latina teenage girl, 15 years old, medium height slim build, 
dark curly hair with purple highlights in ponytail with loose curls framing face, 
dark brown sharp intelligent eyes, dark skin, sharp angular facial features, 
controlled cold expression, calculating gaze
```

---

### PASSO 1 — Hero Shot de Nina
```
Black Latina teenage girl, 15 years old, medium height slim build, 
dark curly hair with purple highlights pulled back in ponytail with loose curls 
framing face, dark brown eyes behind thin dark-framed prescription glasses, 
sharp intelligent gaze, dark skin, sharp angular facial features, 
wearing black jacket over dark shirt, 
neutral controlled cold expression, facing camera slightly turned three-quarter angle, 
clean simple dark background, soft natural lighting, sharp focus on face, 
photorealistic, cinematic portrait, ultra-detailed, no watermark, no text
```

---

### PASSO 2 — Prompts de cena com Character Reference

---

#### NINA — Cena: Jogando videogame em casa (Ep 05 — antes do surto atingir ela)
```
[CHARACTER REF: Nina hero shot, strength 70%]

Black Latina teenage girl sitting cross-legged on bedroom floor playing video game, 
controller in hands, intense focused expression on screen, 
wearing black jacket over dark shirt, hair in ponytail, 
bedroom with gaming setup visible, multiple monitors, gaming posters, 
comfortable but messy room, late afternoon light, 
medium shot, muted warm tones, photorealistic, ultra-detailed
```

---

#### NINA — Cena: Olhando para os pais (Ep 05 — momento de perda)
```
[CHARACTER REF: Nina hero shot, strength 75%]

Black Latina teenage girl standing alone in crashed car aftermath, 
looking at two adult figures collapsed in the distance, 
expression cracking slightly from control to grief but immediately locking back, 
wearing black jacket, night scene with red emergency light, 
wide shot showing her small against the tragedy, 
muted cold dark tones, photorealistic, ultra-detailed
```

---

#### NINA — Cena: Avaliando a situação com Zack (Ep 07)
```
[CHARACTER REF: Nina hero shot, strength 70%]

Black Latina teenage girl and Latino teenage boy standing together studying 
a distant alien structure through dense forest at night, 
girl on left with calculating expression pointing ahead, 
boy on right looking where she points with wide eyes, 
both wearing dark practical clothes, 
cold blue alien light in far background illuminating their faces slightly, 
medium wide shot, muted dark tones with cold blue accent, 
photorealistic, ultra-detailed
```

---

#### NINA — Cena: Dentro da nave alienígena (Ep 08)
```
[CHARACTER REF: Nina hero shot, strength 70%]

Black Latina teenage girl crouching behind cover inside alien base, 
wearing black jacket, hair in ponytail, 
intense alert expression scanning environment, 
surrounding: sleek black walls with blue glowing reentrant lights, 
semi-transparent alien technology, cold white-blue lighting, 
medium shot, muted cold blue-white palette, 
photorealistic, ultra-detailed
```

---

## JUAN ÁLVAREZ — 19 ANOS

### Descrição visual completa
```
Latino young man, 19 years old, tall athletic build, 
short dark brown hair, slight stubble beard, warm brown eyes, 
light olive skin, calm steady expression, protective demeanor
```

---

### PASSO 1 — Hero Shot de Juan
```
Latino young man, 19 years old, tall athletic build, 
short dark brown hair, slight stubble beard, warm brown eyes, 
light olive skin, wearing casual jeans and plaid shirt, 
calm confident expression with warm steadiness, 
facing camera three-quarter angle, clean simple background, 
soft natural lighting, sharp focus on face, 
photorealistic, cinematic portrait, ultra-detailed, no watermark, no text
```

---

### PASSO 2 — Prompts de cena com Character Reference

---

#### JUAN — Cena: No avião olhando pela janela (Ep 03)
```
[CHARACTER REF: Juan hero shot, strength 70%]

Latino young man seated in airplane window seat, looking out at chaotic sky 
visible below, two aircraft collision visible in distance through window, 
expression shifting from calm to alarmed, 
wearing casual shirt, backpack in overhead compartment, 
interior airplane lighting mixed with dramatic exterior light through window, 
medium close shot, muted tones, photorealistic, ultra-detailed
```

---

#### JUAN — Cena: Ligando o carro velho no estacionamento (Ep 03)
```
[CHARACTER REF: Juan hero shot, strength 70%]

Latino young man crouched under dashboard of old beat-up 4x4 truck, 
hotwiring the ignition with a pocketknife, 
intense focused expression, sparks visible from wires, 
chaotic airport parking lot visible through windows with people running, 
smoke on horizon, medium shot, 
muted warm tones shifting darker, photorealistic, ultra-detailed
```

---

#### JUAN — Cena: Acordando na plataforma alienígena (Ep 10)
```
[CHARACTER REF: Juan hero shot, strength 75%]

Latino young man lying on floating alien examination platform, 
semi-conscious, eyes barely opening, 
wearing gray alien examination suit covering body except head, 
wound on left forearm partially healed visible, 
cold clinical alien lab environment around him, 
blue-white light from central luminaire above reflecting on pale skin, 
medium close shot from slightly above, 
muted cold blue-white tones, photorealistic, ultra-detailed
```

---

## GUIA RÁPIDO DE CONFIGURAÇÕES NO LEONARDO AI

### Para gerar o Hero Shot:
| Configuração | Valor |
|---|---|
| Modelo | Phoenix ou Flux Dev |
| Proporção | 3:4 |
| Guidance Scale | 7 |
| Steps | 30 |
| Negative prompt | `cartoon, anime, 3D render, text, watermark, blurry, deformed face, extra fingers, bad anatomy` |

### Para cenas com Character Reference:
| Configuração | Valor |
|---|---|
| Character Reference Strength | 65–75% |
| Proporção | 16:9 |
| Guidance Scale | 7 |
| Steps | 30 |
| Style Reference (opcional) | Carregar uma cena de referência da série para manter paleta |

### Dica de consistência:
Gere sempre **4 variações** por prompt e escolha a melhor. 
Depois use essa imagem escolhida como **nova referência** para a próxima cena — assim a consistência cresce gradualmente ao longo dos episódios.

---

## ESTILO VISUAL DA SÉRIE — Style Reference

Para manter a paleta e atmosfera consistentes em todos os episódios, criar também uma **imagem de estilo de referência** com este prompt:

```
Dark atmospheric cinematic digital painting concept art, 
post-apocalyptic Brazilian landscape, 
muted desaturated color palette, 
warm amber and cold blue contrast, 
dramatic natural lighting, 
photorealistic texture, ultra-detailed, 
no characters visible, just environment
```

Carregar esta imagem como **Style Reference** em todas as gerações com strength 30–40%.
```
