# Proceso: post de beehiiv → carrusel de Instagram + TikTok (@elholder_)

Lo ejecuta la tarea programada diaria. Todo en español latino.

## 0. Preparación
- Repo en `/home/claude/elholder-media` (si no existe: `add_repo` adriansanpei/elholder-media con acceso push y `git clone`). Haz `git pull` antes de empezar.
- Lee los docs del proyecto de Claude "EL HOLDER": `claude/guia-diseno-carruseles.md` y `claude/koemmandments-resumen.md`.

## 1. Detectar posts nuevos
- beehiiv, publicación `pub_61ecdd33-f5a7-44ea-8d04-24f232c8c9b9`: `list_posts` con status `published`, `newest_first`.
- Candidatos: publicados desde 2026-10-14 cuyo ID **no** está en `carruseles/procesados.txt`.
- Ignora duplicados del mismo título/tema (procesa solo la versión más reciente y anota la otra como descartada).
- Si no hay candidatos: termina sin notificar nada.
- Máximo **1 carrusel por corrida** (el candidato más antiguo); los demás quedan para el día siguiente.

## 2. Leer el post
- `get_post_content` (formato text). Identifica: tema, dato/idea principal, 3–6 puntos clave, cifras con fuente, conclusión.
- Nunca inventes datos. Si una cifra no está en el post y la necesitas, consúltala en Token Terminal y cita la fuente.

## 3. Elegir el Koemmandment
- Elige el mandamiento que más le acomode (y opcionalmente una estructura de post) según `claude/koemmandments-resumen.md`. Ese define el gancho de la portada.
- Anota cuál usaste y por qué (va en el mensaje de aprobación).

## 4. Armar el carrusel
- 5 a 8 slides: portada (gancho) → 3–6 slides de valor (1 idea por slide, letra gigante, mínimo texto) → CTA final (newsletter, "link en bio").
- Carpeta: `carruseles/<AAAA-MM-DD>-<slug>/src/slide-NN.html`, copiando los tipos de `carruseles/_ejemplo/src/` y usando `plantilla/base.css`.
- Fondos: una foto del banco por slide (excepto CTA, que va en azul liso), sin repetir en el carrusel; elige por tema con `fondos/INDICE.md`. Evita los fondos usados en los últimos 2 carruseles.
- Si ningún fondo del banco encaja con la portada, puedes generar UNO nuevo con Runway (`gpt-image-2`, ratio `1080:1350`, prompt base en `fondos/INDICE.md`) y agrégalo al banco. Máximo 1 por carrusel, para cuidar créditos.
- Mascota (Doggy, Doggy con lentes, el perrillo o Chubby): **a veces, no siempre**. Más o menos en la mitad de los carruseles, en 1–2 slides. Doggy como personaje, nunca para promover el precio de $DOGGY.
- Handle: **@elholder_** (un guion bajo).
- Render: `python3 plantilla/render.py carruseles/<carpeta>` y revisa `preview.jpg` visualmente (que el texto no se encime, que se lea, que nada se corte). Corrige y vuelve a renderizar si hace falta.

## 5. Descripción, hashtags y música
- Descripción: gancho en las 2 primeras líneas, 3–4 bullets de valor, pregunta para comentarios, CTA "📩 suscríbete gratis en el link de la bio", fuente de datos si aplica y aviso de riesgo cuando se hable de inversiones o tokens ("Contenido educativo, no es recomendación de inversión.").
- Hashtags: máximo 5, relevantes al tema. Palabras clave del tema dentro del texto.
- Música: busca en la web qué audios están en tendencia en Instagram esa semana y sugiere 1–2 canciones que encajen con el tono. (Instagram no permite música en carruseles por API: Adrián la agrega al publicar).

## 6. Subir y pedir aprobación
- Agrega una línea a `carruseles/procesados.txt` con el ID, fecha y título, `git add`, commit y `git push` (las imágenes quedan públicas en `https://raw.githubusercontent.com/adriansanpei/elholder-media/main/carruseles/<carpeta>/slide-NN.jpg`).
- Mándale a Adrián con `SendUserMessage` + `SendUserFile` (preview.jpg y los slides): título del post, koemmandment elegido, la descripción completa, hashtags, música sugerida y el horario propuesto (de Metricool, abajo).
- Pregunta: "¿Lo apruebo y lo programo, o qué le cambio?". **No programes nada sin su "aprobado" explícito.**

## 7. Programar en Metricool (solo tras aprobación)
- Marca `blogId` 7622330 (elholder_), zona `America/Hermosillo`.
- Horario: `getBestTimeToPostByNetwork` (instagram) para los próximos 3 días; elige la mejor hora a partir de 2 h desde ahora. Revisa `getScheduledPosts` para no chocar con otro post el mismo día.
- `createScheduledPost` con: `providers [{network: instagram}]`, `instagramData {type: POST, isAiGenerated: true}`, `media` = las URLs raw de GitHub en orden, `text` = descripción + hashtags, **`autoPublish: false`** (Metricool le manda notificación al cel a la hora programada para que Adrián publique desde Instagram y le ponga la música).
- **TikTok (mismo carrusel, misma aprobación):** un segundo `createScheduledPost` aparte (no en el mismo post que Instagram, porque `autoPublish` es distinto):
  - Horario: `getBestTimeToPostByNetwork` con `tiktok`; si no hay datos todavía, usa la misma hora que Instagram.
  - `providers [{network: tiktok}]`, `media` = las mismas URLs en orden, **`autoPublish: true`** (se publica solo).
  - `tiktokData {title: <título corto, máx. 90 caracteres>, autoAddMusic: true, photoCoverIndex: 0, privacyOption: PUBLIC_TO_EVERYONE, disableComment: false, disableDuet: false, disableStitch: false, commercialContentThirdParty: false, commercialContentOwnBrand: false}`. Si el carrusel promueve un producto propio (seminario, Skool, $DOGGY), `commercialContentOwnBrand: true`; si es patrocinado, `commercialContentThirdParty: true`.
  - `text` = descripción versión TikTok: más corta (gancho + 2 líneas de valor + pregunta + "suscríbete gratis, link en perfil" + aviso de riesgo si aplica) y 3–5 hashtags de TikTok.
  - Si TikTok rechaza el post (formato, cuenta personal, etc.), avisa a Adrián con el error exacto; Instagram sigue igual.
- Confirma a Adrián día/hora de cada red y los `plannerUrl`.
- Plan gratis de Metricool: 20 publicaciones al mes. Revisa con `getScheduledPosts` cuántas van en el mes; si cada red cuenta como publicación aparte y se van a pasar, avísale antes de programar.
