// web-screens.jsx — Desktop/web wireframes for PAESapp Lectora
// Each screen exported as a named component for DCArtboard children.

const WEB_W = 1100;
const WEB_H = 720;

// ── Shared web chrome ───────────────────────────────────────────
function WebChrome({ children, page = 'home' }) {
  return (
    <div style={{ width: WEB_W, height: WEB_H, background: SK.paper, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <WebNav page={page} />
      <div className="sk-scroll" style={{ flex: 1, overflow: 'auto' }}>{children}</div>
    </div>
  );
}

function WebNav({ page = 'home' }) {
  const tabs = [
    { id: 'home', label: 'Inicio', icon: SKIcon.home },
    { id: 'ensayos', label: 'Ensayos', icon: SKIcon.book },
    { id: 'avance', label: 'Avance', icon: SKIcon.chart },
    { id: 'desafios', label: 'Desafíos', icon: SKIcon.trophy },
    { id: 'historial', label: 'Historial', icon: SKIcon.history },
  ];
  return (
    <div style={{ display: 'flex', alignItems: 'center', padding: '14px 32px', borderBottom: `1.5px dashed ${SK.ink}`, gap: 28 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <SKBox fill={SK.ink} radius={6} style={{ width: 32, height: 32 }}>
          <div className="sk-h" style={{ fontSize: 22, color: SK.paper, textAlign: 'center', lineHeight: '32px' }}>L</div>
        </SKBox>
        <div className="sk-h" style={{ fontSize: 24 }}>LectoPAES</div>
      </div>
      <div style={{ display: 'flex', gap: 4, flex: 1 }}>
        {tabs.map(t => {
          const active = t.id === page;
          const Icon = t.icon;
          return (
            <div key={t.id} className="sk-body" style={{
              padding: '6px 12px', fontSize: 15, display: 'flex', alignItems: 'center', gap: 6,
              position: 'relative',
              color: active ? SK.ink : SK.ink2,
              fontWeight: active ? 700 : 400,
            }}>
              <Icon size={16} />
              {t.label}
              {active && <SKUnderline color={SK.hi} style={{ bottom: 0 }} />}
            </div>
          );
        })}
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div className="sk-label" style={{ fontSize: 13, display: 'flex', alignItems: 'center', gap: 4 }}>
          <SKIcon.flame size={16} stroke={SK.coral} fill={SK.coral} />
          <span>12 días</span>
        </div>
        <div className="sk-label" style={{ fontSize: 13, display: 'flex', alignItems: 'center', gap: 4 }}>
          <SKIcon.star size={16} stroke={SK.ink} fill={SK.hi} />
          <span>2,480 XP</span>
        </div>
        <SKBox radius={18} strokeWidth={1.4} style={{ width: 36, height: 36 }}>
          <div className="sk-h" style={{ textAlign: 'center', lineHeight: '36px', fontSize: 18 }}>M</div>
        </SKBox>
      </div>
    </div>
  );
}

// ── 01. HOME / Landing ───────────────────────────────────────────
function WebHome() {
  return (
    <WebChrome page="home">
      {/* HERO */}
      <div style={{ padding: '40px 48px 32px', display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: 40, alignItems: 'center' }}>
        <div>
          <div className="sk-label" style={{ fontSize: 14, color: SK.ink2, marginBottom: 8, letterSpacing: 1, textTransform: 'uppercase' }}>
            Preparación PAES · Competencia Lectora
          </div>
          <div className="sk-h" style={{ fontSize: 56, lineHeight: 1, marginBottom: 4, position: 'relative', display: 'inline-block' }}>
            Lee. Practica.
          </div>
          <div className="sk-h" style={{ fontSize: 56, lineHeight: 1, marginBottom: 20, position: 'relative', display: 'inline-block' }}>
            <span style={{ position: 'relative' }}>Entra a la U.<SKUnderline color={SK.hi} /></span>
          </div>
          <div className="sk-body" style={{ fontSize: 18, lineHeight: 1.5, color: SK.ink2, marginBottom: 24, maxWidth: 440 }}>
            Ejercicios reales tipo DEMRE. Soluciones explicadas paso a paso. Sin presión.
          </div>
          <div style={{ display: 'flex', gap: 12 }}>
            <SKButton variant="primary" size="lg">Empezar ahora →</SKButton>
            <SKButton variant="ghost" size="lg">Ver cómo funciona</SKButton>
          </div>
        </div>
        {/* Mascot / illustration placeholder */}
        <SKHatch style={{ height: 280, borderRadius: 12 }} label="Ilustración · Estudiante leyendo" />
      </div>

      <SKDivider style={{ margin: '0 48px' }} />

      {/* 3 MODES */}
      <div style={{ padding: '40px 48px 32px' }}>
        <div className="sk-h" style={{ fontSize: 28, marginBottom: 4 }}>¿Qué quieres hacer hoy?</div>
        <div className="sk-body" style={{ fontSize: 15, color: SK.ink2, marginBottom: 24 }}>Elige tu modo. Todos guardan progreso.</div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1.15fr', gap: 20 }}>
          {/* Ensayo DEMRE */}
          <SKBox radius={12} strokeWidth={1.8} shadow style={{ minHeight: 260 }}>
            <div style={{ padding: 24, display: 'flex', flexDirection: 'column', gap: 10, height: '100%' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <SKIcon.book size={22} />
                <div className="sk-h" style={{ fontSize: 24 }}>Ensayo DEMRE</div>
              </div>
              <div className="sk-body" style={{ fontSize: 14, color: SK.ink2, lineHeight: 1.4, flex: 1 }}>
                Prueba completa tipo oficial. 65 preguntas · 2h 30min. Textos reales de años anteriores.
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
                <SKBadge color={SK.mint}>Largo</SKBadge>
                <div className="sk-mono" style={{ fontSize: 11, color: SK.mute }}>150 min</div>
              </div>
              <SKButton variant="default">Elegir ensayo →</SKButton>
            </div>
          </SKBox>

          {/* Práctica rápida */}
          <SKBox radius={12} strokeWidth={1.8} shadow style={{ minHeight: 260 }}>
            <div style={{ padding: 24, display: 'flex', flexDirection: 'column', gap: 10, height: '100%' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <SKIcon.bolt size={22} fill={SK.hi} />
                <div className="sk-h" style={{ fontSize: 24 }}>Práctica rápida</div>
              </div>
              <div className="sk-body" style={{ fontSize: 14, color: SK.ink2, lineHeight: 1.4, flex: 1 }}>
                Un texto, 5 preguntas. Perfecto para un break. Feedback inmediato con explicación.
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
                <SKBadge color={SK.lav}>Corto</SKBadge>
                <div className="sk-mono" style={{ fontSize: 11, color: SK.mute }}>~10 min</div>
              </div>
              <SKButton variant="default">Practicar ahora →</SKButton>
            </div>
          </SKBox>

          {/* PROMO — Prueba corta gratis */}
          <div style={{ position: 'relative' }}>
            <SKBox radius={12} strokeWidth={2.4} fill={SK.coral} shadow style={{ minHeight: 260 }}>
              <div style={{ padding: 24, display: 'flex', flexDirection: 'column', gap: 10, height: '100%' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <SKIcon.gift size={22} />
                    <div className="sk-h" style={{ fontSize: 24 }}>Prueba corta GRATIS</div>
                  </div>
                  <SKBadge color={SK.ink} style={{ }}>
                    <span style={{ color: SK.paper }}>NUEVO</span>
                  </SKBadge>
                </div>
                <div className="sk-body" style={{ fontSize: 15, lineHeight: 1.4, flex: 1 }}>
                  Prueba tu nivel <b>en 5 minutos</b>. Sin registro. Mira dónde estás parado antes de la PAES.
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
                  <div className="sk-mono" style={{ fontSize: 11 }}>5 min · 3 preguntas · 100% gratis</div>
                </div>
                <SKButton variant="primary" size="lg">¡Empezar ahora!</SKButton>
              </div>
            </SKBox>
            <SKAnnotation style={{ position: 'absolute', top: -20, right: -24, zIndex: 5 }} rotate={6}>
              ¡Pruébalo! sin crear cuenta ✨
            </SKAnnotation>
          </div>
        </div>
      </div>

      <SKDivider style={{ margin: '0 48px' }} />

      {/* QUICK TABS / SHORTCUTS BAJANDO */}
      <div style={{ padding: '40px 48px 48px' }}>
        <div className="sk-h" style={{ fontSize: 28, marginBottom: 4 }}>Tu panel</div>
        <div className="sk-body" style={{ fontSize: 15, color: SK.ink2, marginBottom: 24 }}>Accede rápido a tus secciones →</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
          {[
            { label: 'Historial', icon: SKIcon.history, desc: '28 ejercicios hechos', color: null },
            { label: 'Avance', icon: SKIcon.chart, desc: '72% Inferir · 45% Evaluar', color: null },
            { label: 'Desafíos', icon: SKIcon.trophy, desc: '2 nuevos esta semana', color: SK.hi },
            { label: 'Tu perfil', icon: SKIcon.user, desc: 'Nivel 4 · 2,480 XP', color: null },
          ].map((t, i) => {
            const Icon = t.icon;
            return (
              <SKBox key={i} radius={10} fill={t.color || 'transparent'} style={{ minHeight: 110 }}>
                <div style={{ padding: 16, display: 'flex', flexDirection: 'column', gap: 6, height: '100%' }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Icon size={22} />
                    <SKIcon.arrow size={16} />
                  </div>
                  <div className="sk-h" style={{ fontSize: 22 }}>{t.label}</div>
                  <div className="sk-body" style={{ fontSize: 13, color: SK.ink2 }}>{t.desc}</div>
                </div>
              </SKBox>
            );
          })}
        </div>
      </div>

      <SKDivider style={{ margin: '0 48px' }} />

      {/* ── SEGUNDA PÁGINA (scroll) · Videos testimoniales ────── */}
      <div style={{ padding: '56px 48px 56px', background: '#f7f4ec' }}>
        <div style={{ textAlign: 'center', marginBottom: 36 }}>
          <SKBadge color={SK.hi} style={{ marginBottom: 10 }}>Así usan LectoPAES</SKBadge>
          <div className="sk-h" style={{ fontSize: 44, lineHeight: 1, marginBottom: 8 }}>
            Practica donde <span style={{ position: 'relative' }}>estés<SKUnderline color={SK.coral} /></span>
          </div>
          <div className="sk-body" style={{ fontSize: 16, color: SK.ink2, maxWidth: 520, margin: '0 auto' }}>
            En el bolsillo o en tu escritorio. Mismos ejercicios, mismo avance, sincronizados.
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 28 }}>
          {/* Video 1 · En el metro */}
          <div style={{ position: 'relative' }}>
            <SKBox radius={14} strokeWidth={2} shadow style={{ minHeight: 320 }}>
              <div style={{ padding: 18 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
                  <SKBox fill={SK.coral} radius={14} strokeWidth={1.4} style={{ width: 28, height: 28 }}>
                    <div className="sk-h" style={{ textAlign: 'center', lineHeight: '28px', fontSize: 14 }}>C</div>
                  </SKBox>
                  <div>
                    <div className="sk-body" style={{ fontSize: 13, fontWeight: 700 }}>Catalina, 17</div>
                    <div className="sk-mono" style={{ fontSize: 10, color: SK.mute }}>Línea 1 · 8:42 AM</div>
                  </div>
                  <div style={{ flex: 1 }} />
                  <SKBadge color={SK.paper}>📱 Móvil</SKBadge>
                </div>
                {/* Video placeholder */}
                <div style={{ position: 'relative' }}>
                  <SKHatch style={{ height: 200, borderRadius: 10 }} label="Video · suscriptor ejercitando en el metro">
                    <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <SKBox fill={SK.paper} radius={30} strokeWidth={2} shadow style={{ width: 60, height: 60 }}>
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                          <SKIcon.play size={26} fill={SK.ink} stroke={SK.ink} />
                        </div>
                      </SKBox>
                    </div>
                    <div className="sk-mono" style={{ position: 'absolute', bottom: 8, right: 10, fontSize: 10, background: 'rgba(42,38,34,0.8)', color: SK.paper, padding: '2px 6px', borderRadius: 3 }}>
                      0:47
                    </div>
                  </SKHatch>
                </div>
                <div className="sk-body" style={{ fontSize: 14, lineHeight: 1.4, marginTop: 12, color: SK.ink }}>
                  "En el viaje al colegio hago 2 prácticas rápidas. Cuando llego, ya gané mi XP del día." 🚇
                </div>
                <div style={{ display: 'flex', gap: 12, marginTop: 10 }}>
                  <div className="sk-mono" style={{ fontSize: 10, color: SK.mute }}>⏱ 10 min/día</div>
                  <div className="sk-mono" style={{ fontSize: 10, color: SK.mute }}>🔥 34 días</div>
                  <div className="sk-mono" style={{ fontSize: 10, color: SK.mute }}>📚 +180 ejerc.</div>
                </div>
              </div>
            </SKBox>
            <SKAnnotation style={{ position: 'absolute', top: -16, right: -18 }} rotate={6}>
              camino al cole 🚇
            </SKAnnotation>
          </div>

          {/* Video 2 · En el escritorio */}
          <div style={{ position: 'relative' }}>
            <SKBox radius={14} strokeWidth={2} shadow style={{ minHeight: 320 }}>
              <div style={{ padding: 18 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
                  <SKBox fill={SK.mint} radius={14} strokeWidth={1.4} style={{ width: 28, height: 28 }}>
                    <div className="sk-h" style={{ textAlign: 'center', lineHeight: '28px', fontSize: 14 }}>T</div>
                  </SKBox>
                  <div>
                    <div className="sk-body" style={{ fontSize: 13, fontWeight: 700 }}>Tomás, 18</div>
                    <div className="sk-mono" style={{ fontSize: 10, color: SK.mute }}>Casa · 19:30 PM</div>
                  </div>
                  <div style={{ flex: 1 }} />
                  <SKBadge color={SK.paper}>💻 Escritorio</SKBadge>
                </div>
                {/* Video placeholder */}
                <div style={{ position: 'relative' }}>
                  <SKHatch style={{ height: 200, borderRadius: 10 }} label="Video · estudiante en el escritorio">
                    <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <SKBox fill={SK.paper} radius={30} strokeWidth={2} shadow style={{ width: 60, height: 60 }}>
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                          <SKIcon.play size={26} fill={SK.ink} stroke={SK.ink} />
                        </div>
                      </SKBox>
                    </div>
                    <div className="sk-mono" style={{ position: 'absolute', bottom: 8, right: 10, fontSize: 10, background: 'rgba(42,38,34,0.8)', color: SK.paper, padding: '2px 6px', borderRadius: 3 }}>
                      1:12
                    </div>
                  </SKHatch>
                </div>
                <div className="sk-body" style={{ fontSize: 14, lineHeight: 1.4, marginTop: 12, color: SK.ink }}>
                  "Después de clases me hago un ensayo DEMRE cronometrado. El feedback paso a paso me salvó." ✏️
                </div>
                <div style={{ display: 'flex', gap: 12, marginTop: 10 }}>
                  <div className="sk-mono" style={{ fontSize: 10, color: SK.mute }}>⏱ 2h/sesión</div>
                  <div className="sk-mono" style={{ fontSize: 10, color: SK.mute }}>📈 65 → 82%</div>
                  <div className="sk-mono" style={{ fontSize: 10, color: SK.mute }}>🏆 Nivel 7</div>
                </div>
              </div>
            </SKBox>
            <SKAnnotation style={{ position: 'absolute', top: -16, left: -16 }} rotate={-5}>
              ensayo completo ✏️
            </SKAnnotation>
          </div>
        </div>

        {/* Stat strip */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginTop: 36, textAlign: 'center' }}>
          {[
            ['+12k', 'estudiantes activos'],
            ['1.2M', 'ejercicios resueltos'],
            ['+68pt', 'promedio de mejora'],
            ['4.8★', 'rating en la store'],
          ].map(([v, l]) => (
            <div key={l}>
              <div className="sk-h" style={{ fontSize: 32, lineHeight: 1 }}>{v}</div>
              <div className="sk-label" style={{ fontSize: 11, color: SK.ink2, marginTop: 2 }}>{l}</div>
            </div>
          ))}
        </div>

        <div style={{ textAlign: 'center', marginTop: 32 }}>
          <SKButton variant="primary" size="lg">Empezar como Catalina →</SKButton>
        </div>
      </div>

      {/* FOOTER */}
      <div style={{ padding: '24px 48px', borderTop: `1.5px dashed ${SK.ink}`, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div className="sk-label" style={{ fontSize: 12, color: SK.mute }}>LectoPAES · Preparación gratuita · 2026</div>
        <div className="sk-label" style={{ fontSize: 12, color: SK.mute, display: 'flex', gap: 16 }}>
          <span>Contacto</span><span>Acerca de</span><span>Términos</span>
        </div>
      </div>
    </WebChrome>
  );
}

// ── 02. ENSAYOS DEMRE — selección ────────────────────────────────
function WebEnsayos() {
  const ensayos = [
    { year: '2024', name: 'PAES Regular', n: 65, min: 150, done: true },
    { year: '2023', name: 'PAES Invierno', n: 65, min: 150, done: false },
    { year: '2023', name: 'PAES Regular', n: 65, min: 150, done: false },
    { year: '2022', name: 'PDT', n: 60, min: 150, done: false },
    { year: '2022', name: 'Oficial DEMRE', n: 65, min: 150, done: false },
    { year: '2021', name: 'PDT Invierno', n: 60, min: 150, done: false },
  ];
  return (
    <WebChrome page="ensayos">
      <div style={{ padding: '32px 48px' }}>
        <div className="sk-label" style={{ fontSize: 13, color: SK.mute, marginBottom: 6 }}>← Volver · Inicio / Ensayos DEMRE</div>
        <div className="sk-h" style={{ fontSize: 40, marginBottom: 4 }}>Ensayos tipo DEMRE</div>
        <div className="sk-body" style={{ fontSize: 16, color: SK.ink2, marginBottom: 24 }}>
          Pruebas completas oficiales de años anteriores. Mismo formato, mismo tiempo. <b>Ideal para cronometrarte.</b>
        </div>

        {/* Filtros */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 24, alignItems: 'center' }}>
          <div className="sk-label" style={{ fontSize: 13, color: SK.ink2 }}>Filtrar:</div>
          {['Todos', '2024', '2023', '2022', '2021'].map((f, i) => (
            <SKButton key={f} size="sm" variant={i === 0 ? 'primary' : 'ghost'}>{f}</SKButton>
          ))}
          <div style={{ flex: 1 }} />
          <SKButton size="sm" variant="ghost">Ordenar: Más recientes ↓</SKButton>
        </div>

        {/* Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {ensayos.map((e, i) => (
            <SKBox key={i} radius={10} strokeWidth={1.8} style={{ minHeight: 200 }}>
              <div style={{ padding: 18, display: 'flex', flexDirection: 'column', gap: 8, height: '100%' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <SKBadge color={SK.paper}>{e.year}</SKBadge>
                  {e.done && <div className="sk-label" style={{ fontSize: 11, color: SK.mint, display: 'flex', alignItems: 'center', gap: 3 }}><SKIcon.check size={12} stroke={SK.mint}/> Hecho</div>}
                </div>
                <div className="sk-h" style={{ fontSize: 22, lineHeight: 1.1 }}>{e.name}</div>
                <div className="sk-mono" style={{ fontSize: 11, color: SK.mute }}>
                  {e.n} preguntas · {e.min} min
                </div>
                {e.done && (
                  <div style={{ marginTop: 'auto', marginBottom: 4 }}>
                    <div className="sk-label" style={{ fontSize: 12, marginBottom: 4 }}>Tu resultado: 52/65 (80%)</div>
                    <SKProgress value={0.8} height={6} />
                  </div>
                )}
                <div style={{ marginTop: e.done ? 0 : 'auto' }}>
                  <SKButton size="sm" variant={e.done ? 'ghost' : 'primary'} style={{ width: '100%' }}>
                    {e.done ? 'Ver resultados' : 'Empezar ensayo →'}
                  </SKButton>
                </div>
              </div>
            </SKBox>
          ))}
        </div>
      </div>
    </WebChrome>
  );
}

// ── 03. PRÁCTICAS RÁPIDAS — selección por habilidad ──────────────
function WebPracticas() {
  const skills = [
    { name: 'Localizar', desc: 'Encontrar información explícita en el texto', progress: 0.85, done: 12, color: SK.mint },
    { name: 'Interpretar', desc: 'Inferir significados, relaciones e ideas', progress: 0.62, done: 8, color: SK.hi },
    { name: 'Evaluar', desc: 'Reflexionar sobre forma y contenido', progress: 0.34, done: 4, color: SK.coral },
  ];
  return (
    <WebChrome page="ensayos">
      <div style={{ padding: '32px 48px' }}>
        <div className="sk-label" style={{ fontSize: 13, color: SK.mute, marginBottom: 6 }}>← Volver · Inicio / Práctica rápida</div>
        <div className="sk-h" style={{ fontSize: 40, marginBottom: 4 }}>Práctica rápida</div>
        <div className="sk-body" style={{ fontSize: 16, color: SK.ink2, marginBottom: 28 }}>
          Elige qué quieres entrenar. <b>Un texto, 5 preguntas, ~10 min.</b>
        </div>

        {/* Habilidades */}
        <div className="sk-h" style={{ fontSize: 22, marginBottom: 12 }}>Por habilidad</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 32 }}>
          {skills.map((s, i) => (
            <SKBox key={i} radius={10} strokeWidth={1.8} shadow style={{ minHeight: 190 }}>
              <div style={{ padding: 18, display: 'flex', flexDirection: 'column', gap: 10, height: '100%' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <SKBox fill={s.color} radius={6} style={{ width: 36, height: 36 }}>
                    <div className="sk-h" style={{ textAlign: 'center', lineHeight: '36px', fontSize: 20 }}>{s.name[0]}</div>
                  </SKBox>
                  <div className="sk-h" style={{ fontSize: 22 }}>{s.name}</div>
                </div>
                <div className="sk-body" style={{ fontSize: 13, color: SK.ink2, lineHeight: 1.4, flex: 1 }}>{s.desc}</div>
                <div>
                  <div className="sk-label" style={{ fontSize: 11, color: SK.mute, marginBottom: 4, display: 'flex', justifyContent: 'space-between' }}>
                    <span>{s.done} ejercicios</span><span>{Math.round(s.progress*100)}%</span>
                  </div>
                  <SKProgress value={s.progress} height={6} />
                </div>
                <SKButton size="sm" variant="primary" style={{ width: '100%' }}>Practicar →</SKButton>
              </div>
            </SKBox>
          ))}
        </div>

        {/* Tipos de texto */}
        <div className="sk-h" style={{ fontSize: 22, marginBottom: 12 }}>Por tipo de texto</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
          {['Narrativo', 'Expositivo', 'Argumentativo', 'Noticia', 'Columna', 'Ensayo', 'Poema', 'Divulgación'].map((t, i) => (
            <SKBox key={t} radius={8} strokeWidth={1.4} style={{ }}>
              <div className="sk-body" style={{ padding: '14px 14px', fontSize: 14, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span>{t}</span>
                <SKIcon.arrow size={14} />
              </div>
            </SKBox>
          ))}
        </div>
      </div>
    </WebChrome>
  );
}

// ── 04. PROMO — Prueba corta gratis (landing / onboarding modal) ──
function WebPromo() {
  return (
    <WebChrome page="home">
      <div style={{ padding: '60px 80px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 48, alignItems: 'center' }}>
        <div>
          <SKBadge color={SK.coral} style={{ marginBottom: 14 }}>100% gratis · sin registro</SKBadge>
          <div className="sk-h" style={{ fontSize: 62, lineHeight: 0.95, marginBottom: 10 }}>
            Descubre tu nivel<br/>en <span style={{ position: 'relative' }}>5 minutos<SKUnderline color={SK.coral} /></span>
          </div>
          <div className="sk-body" style={{ fontSize: 18, lineHeight: 1.5, color: SK.ink2, marginBottom: 28, maxWidth: 440 }}>
            3 preguntas rápidas basadas en textos reales de la PAES. Te mostramos qué dominas y qué conviene reforzar.
          </div>
          <div style={{ display: 'flex', gap: 12, marginBottom: 24 }}>
            <SKButton variant="promo" size="lg">¡Empezar prueba gratis! →</SKButton>
            <SKButton variant="ghost" size="lg">Más info</SKButton>
          </div>
          <div style={{ display: 'flex', gap: 24 }}>
            {[['3', 'preguntas'], ['5', 'minutos'], ['0$', 'costo']].map(([n, l]) => (
              <div key={l}>
                <div className="sk-h" style={{ fontSize: 36, lineHeight: 1 }}>{n}</div>
                <div className="sk-label" style={{ fontSize: 12, color: SK.ink2 }}>{l}</div>
              </div>
            ))}
          </div>
        </div>
        <div style={{ position: 'relative' }}>
          <SKBox radius={14} fill={SK.hi} strokeWidth={2} shadow style={{ minHeight: 380 }}>
            <div style={{ padding: 32 }}>
              <div className="sk-label" style={{ fontSize: 11, letterSpacing: 1, textTransform: 'uppercase', marginBottom: 12 }}>Pregunta 1 de 3</div>
              <div className="sk-h" style={{ fontSize: 22, marginBottom: 16, lineHeight: 1.2 }}>¿Cuál es la idea principal del texto?</div>
              <SKBox radius={8} style={{ marginBottom: 8 }}><div className="sk-body" style={{ padding: 10, fontSize: 14 }}>a) El autor critica la educación tradicional</div></SKBox>
              <SKBox radius={8} fill={SK.paper} style={{ marginBottom: 8 }}><div className="sk-body" style={{ padding: 10, fontSize: 14 }}>b) Reflexiona sobre la lectura como herramienta</div></SKBox>
              <SKBox radius={8} style={{ marginBottom: 8 }}><div className="sk-body" style={{ padding: 10, fontSize: 14 }}>c) Describe una biblioteca</div></SKBox>
              <SKBox radius={8} style={{ }}><div className="sk-body" style={{ padding: 10, fontSize: 14 }}>d) Narra una anécdota personal</div></SKBox>
            </div>
          </SKBox>
          <SKAnnotation style={{ position: 'absolute', bottom: -16, left: -20 }} rotate={-4}>
            así se ven las preguntas ✏️
          </SKAnnotation>
        </div>
      </div>
    </WebChrome>
  );
}

// ── 05. SELECCIÓN DE TEXTO / TEMA ────────────────────────────────
function WebSelectText() {
  const texts = [
    { title: 'El valor de la lectura', genre: 'Ensayo', words: 420, diff: 'Media', time: 8 },
    { title: 'Crónica del apagón de 2019', genre: 'Noticia', words: 380, diff: 'Fácil', time: 6 },
    { title: 'Pablo Neruda, fragmento', genre: 'Poema', words: 180, diff: 'Difícil', time: 10 },
    { title: 'La crisis del agua en Chile', genre: 'Argumentativo', words: 520, diff: 'Media', time: 10 },
    { title: 'El origen de los volcanes', genre: 'Divulgación', words: 340, diff: 'Fácil', time: 7 },
    { title: 'Mi planta de naranja lima', genre: 'Narrativo', words: 460, diff: 'Media', time: 9 },
  ];
  return (
    <WebChrome page="ensayos">
      <div style={{ padding: '32px 48px' }}>
        <div className="sk-label" style={{ fontSize: 13, color: SK.mute, marginBottom: 6 }}>← Inicio / Práctica rápida / Elige texto</div>
        <div className="sk-h" style={{ fontSize: 36, marginBottom: 4 }}>Elige un texto</div>
        <div className="sk-body" style={{ fontSize: 15, color: SK.ink2, marginBottom: 24 }}>6 textos disponibles · filtrados por "Interpretar" · ordena por el que más te llame la atención</div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16 }}>
          {texts.map((t, i) => (
            <SKBox key={i} radius={10} strokeWidth={1.6} style={{ }}>
              <div style={{ padding: 18, display: 'grid', gridTemplateColumns: '80px 1fr auto', gap: 14, alignItems: 'center' }}>
                <SKHatch style={{ width: 80, height: 90, borderRadius: 6 }} label={t.genre} />
                <div>
                  <div style={{ display: 'flex', gap: 6, marginBottom: 4 }}>
                    <SKBadge color={t.diff === 'Fácil' ? SK.mint : t.diff === 'Media' ? SK.hi : SK.coral}>{t.diff}</SKBadge>
                    <SKBadge color={SK.paper}>{t.genre}</SKBadge>
                  </div>
                  <div className="sk-h" style={{ fontSize: 20, lineHeight: 1.1, marginBottom: 4 }}>{t.title}</div>
                  <div className="sk-mono" style={{ fontSize: 11, color: SK.mute }}>{t.words} palabras · ~{t.time} min · 5 preguntas</div>
                </div>
                <SKButton size="sm" variant="primary">Leer →</SKButton>
              </div>
            </SKBox>
          ))}
        </div>
      </div>
    </WebChrome>
  );
}

// ── 06. PREGUNTA ─────────────────────────────────────────────────
function WebQuestion() {
  return (
    <WebChrome page="ensayos">
      <div style={{ padding: '20px 48px', borderBottom: `1.5px dashed ${SK.ink}`, display: 'flex', alignItems: 'center', gap: 16 }}>
        <SKButton size="sm" variant="ghost">← Salir</SKButton>
        <div style={{ flex: 1 }}>
          <div className="sk-label" style={{ fontSize: 12, color: SK.mute, marginBottom: 4 }}>Texto: "El valor de la lectura" · Pregunta 2 de 5</div>
          <SKProgress value={0.4} height={8} />
        </div>
        <div className="sk-label" style={{ fontSize: 14, display: 'flex', alignItems: 'center', gap: 4 }}>
          <SKIcon.clock size={16} /> 07:24
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 0, height: 'calc(100% - 65px)' }}>
        {/* Text panel */}
        <div className="sk-scroll" style={{ padding: '24px 32px 24px 48px', overflow: 'auto', borderRight: `1.5px dashed ${SK.ink}` }}>
          <div className="sk-label" style={{ fontSize: 11, letterSpacing: 1, textTransform: 'uppercase', color: SK.mute, marginBottom: 6 }}>Texto</div>
          <div className="sk-h" style={{ fontSize: 24, marginBottom: 12 }}>El valor de la lectura</div>
          <div className="sk-body" style={{ fontSize: 14, lineHeight: 1.7, color: SK.ink, columnGap: 20 }}>
            <p style={{ marginBottom: 12 }}><span className="sk-mono" style={{ fontSize: 11, color: SK.mute, marginRight: 8 }}>1</span>Leer no es solo decodificar signos. Es una conversación silenciosa con alguien que puede estar a miles de kilómetros, o muerto hace siglos. Cuando un lector abre un libro, acepta un pacto: prestar su atención a cambio de ser transportado.</p>
            <p style={{ marginBottom: 12 }}><span className="sk-mono" style={{ fontSize: 11, color: SK.mute, marginRight: 8 }}>2</span>En la era del scroll infinito, <span style={{ background: SK.hi, padding: '0 2px' }}>la lectura profunda es un acto casi subversivo</span>. No produce dopamina rápida. No se comparte fácilmente. Requiere tiempo, silencio, paciencia.</p>
            <p style={{ marginBottom: 12 }}><span className="sk-mono" style={{ fontSize: 11, color: SK.mute, marginRight: 8 }}>3</span>Y sin embargo, los estudios son claros: quienes leen regularmente desarrollan mayor capacidad de concentración, mejor comprensión emocional y un vocabulario sustancialmente más rico que quienes no lo hacen.</p>
            <p style={{ marginBottom: 12 }}><span className="sk-mono" style={{ fontSize: 11, color: SK.mute, marginRight: 8 }}>4</span>La pregunta, entonces, no es si debemos leer. Es qué estamos dispuestos a silenciar para poder hacerlo.</p>
          </div>
        </div>

        {/* Question panel */}
        <div className="sk-scroll" style={{ padding: '24px 48px 24px 32px', overflow: 'auto' }}>
          <div className="sk-label" style={{ fontSize: 11, letterSpacing: 1, textTransform: 'uppercase', color: SK.mute, marginBottom: 6 }}>Pregunta 2 de 5 · Interpretar</div>
          <div className="sk-h" style={{ fontSize: 22, marginBottom: 20, lineHeight: 1.2 }}>
            ¿Qué sugiere el autor al llamar a la lectura profunda "un acto casi subversivo"?
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {[
              { l: 'A', t: 'Que leer está prohibido en la era digital.' },
              { l: 'B', t: 'Que leer desafía los hábitos de atención actuales.', sel: true },
              { l: 'C', t: 'Que los lectores son rebeldes por naturaleza.' },
              { l: 'D', t: 'Que la lectura genera controversia política.' },
            ].map(o => (
              <SKBox key={o.l} radius={8} strokeWidth={o.sel ? 2.4 : 1.6} fill={o.sel ? SK.hi : 'transparent'}>
                <div className="sk-body" style={{ padding: 12, fontSize: 15, display: 'flex', alignItems: 'center', gap: 12 }}>
                  <SKBox radius={14} strokeWidth={1.6} fill={o.sel ? SK.ink : 'transparent'} style={{ width: 28, height: 28, flexShrink: 0 }}>
                    <div className="sk-h" style={{ textAlign: 'center', lineHeight: '28px', fontSize: 14, color: o.sel ? SK.paper : SK.ink }}>{o.l}</div>
                  </SKBox>
                  <span>{o.t}</span>
                </div>
              </SKBox>
            ))}
          </div>

          <div style={{ marginTop: 28, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <SKButton variant="ghost">← Anterior</SKButton>
            <div style={{ display: 'flex', gap: 8 }}>
              <SKButton variant="ghost" size="sm" icon={<SKIcon.heart size={14} />}>Guardar</SKButton>
              <SKButton variant="primary" size="md">Responder →</SKButton>
            </div>
          </div>
        </div>
      </div>
    </WebChrome>
  );
}

// ── 07. RESULTADO — CORRECTO ─────────────────────────────────────
function WebResultCorrect() {
  return (
    <WebChrome page="ensayos">
      <div style={{ padding: '32px 48px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
        <div>
          {/* Big correct banner */}
          <SKBox radius={12} fill={SK.mint} strokeWidth={2.4} shadow style={{ marginBottom: 20 }}>
            <div style={{ padding: 24, display: 'flex', alignItems: 'center', gap: 16 }}>
              <SKBox radius={28} fill={SK.ink} style={{ width: 56, height: 56, flexShrink: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                  <SKIcon.check size={32} stroke={SK.paper} />
                </div>
              </SKBox>
              <div>
                <div className="sk-h" style={{ fontSize: 34, lineHeight: 1 }}>¡Correcto!</div>
                <div className="sk-body" style={{ fontSize: 14, color: SK.ink2 }}>+15 XP · 4 correctas seguidas 🔥</div>
              </div>
            </div>
          </SKBox>

          {/* Your answer */}
          <div className="sk-label" style={{ fontSize: 12, color: SK.mute, marginBottom: 6, textTransform: 'uppercase', letterSpacing: 1 }}>Tu respuesta</div>
          <SKBox radius={8} strokeWidth={2} fill={SK.mint} style={{ marginBottom: 16 }}>
            <div className="sk-body" style={{ padding: 14, fontSize: 15, display: 'flex', alignItems: 'center', gap: 10 }}>
              <SKIcon.check size={18} /> <b>B.</b> Que leer desafía los hábitos de atención actuales.
            </div>
          </SKBox>

          {/* Stats */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 10, marginBottom: 20 }}>
            {[
              ['Tiempo', '0:42', SKIcon.clock],
              ['% acierto', '72%', SKIcon.target],
              ['Racha', '4', SKIcon.flame],
            ].map(([l, v, I]) => (
              <SKBox key={l} radius={8} strokeWidth={1.4}>
                <div style={{ padding: 12, textAlign: 'center' }}>
                  <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 4 }}><I size={18} /></div>
                  <div className="sk-h" style={{ fontSize: 22 }}>{v}</div>
                  <div className="sk-label" style={{ fontSize: 11, color: SK.mute }}>{l}</div>
                </div>
              </SKBox>
            ))}
          </div>

          <div style={{ display: 'flex', gap: 8 }}>
            <SKButton variant="primary" size="lg" style={{ flex: 1 }}>Siguiente pregunta →</SKButton>
            <SKButton variant="ghost" size="lg" icon={<SKIcon.share size={16} />}>Compartir</SKButton>
          </div>
        </div>

        {/* Explanation */}
        <div>
          <div className="sk-label" style={{ fontSize: 12, color: SK.mute, marginBottom: 8, textTransform: 'uppercase', letterSpacing: 1 }}>Explicación</div>
          <SKBox radius={10} strokeWidth={1.6}>
            <div style={{ padding: 20 }}>
              <div className="sk-h" style={{ fontSize: 20, marginBottom: 12 }}>¿Por qué esta respuesta?</div>
              <div className="sk-body" style={{ fontSize: 14, lineHeight: 1.6, marginBottom: 14, color: SK.ink }}>
                El autor usa "subversivo" de forma figurada. Fíjate en la frase clave del párrafo 2: <span style={{ background: SK.hi }}>"No produce dopamina rápida. No se comparte fácilmente."</span> — describe cómo la lectura profunda <b>va en contra</b> de los hábitos digitales de atención.
              </div>
              <SKDivider style={{ margin: '14px 0' }} />
              <div className="sk-label" style={{ fontSize: 11, color: SK.mute, marginBottom: 6, textTransform: 'uppercase', letterSpacing: 1 }}>Por qué NO las otras</div>
              <ul className="sk-body" style={{ fontSize: 13, lineHeight: 1.5, margin: 0, paddingLeft: 18 }}>
                <li style={{ marginBottom: 4 }}><b>A:</b> "Subversivo" no significa prohibido — es interpretación literal.</li>
                <li style={{ marginBottom: 4 }}><b>C:</b> El autor habla del acto de leer, no de los lectores.</li>
                <li><b>D:</b> No hay referencia a controversia política.</li>
              </ul>

              <SKDivider style={{ margin: '14px 0' }} />
              <SKHatch style={{ height: 100, borderRadius: 6 }} label="Video · 45 seg · explicación rápida" />
            </div>
          </SKBox>

          <div style={{ marginTop: 12, display: 'flex', gap: 8 }}>
            <SKButton size="sm" variant="ghost">Habilidad: Interpretar ↗</SKButton>
            <SKButton size="sm" variant="ghost">Guardar nota</SKButton>
          </div>
        </div>
      </div>
    </WebChrome>
  );
}

// ── 08. RESULTADO — INCORRECTO ───────────────────────────────────
function WebResultWrong() {
  return (
    <WebChrome page="ensayos">
      <div style={{ padding: '32px 48px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
        <div>
          <SKBox radius={12} fill={SK.coral} strokeWidth={2.4} shadow style={{ marginBottom: 20 }}>
            <div style={{ padding: 24, display: 'flex', alignItems: 'center', gap: 16 }}>
              <SKBox radius={28} fill={SK.ink} style={{ width: 56, height: 56, flexShrink: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                  <SKIcon.x size={32} stroke={SK.paper} />
                </div>
              </SKBox>
              <div>
                <div className="sk-h" style={{ fontSize: 34, lineHeight: 1 }}>Casi lo tenías</div>
                <div className="sk-body" style={{ fontSize: 14, color: SK.ink2 }}>Sin XP esta vez · Vas a aprender de esta ✏️</div>
              </div>
            </div>
          </SKBox>

          <div className="sk-label" style={{ fontSize: 12, color: SK.mute, marginBottom: 6, textTransform: 'uppercase', letterSpacing: 1 }}>Tu respuesta</div>
          <SKBox radius={8} strokeWidth={2} fill={SK.coral} style={{ marginBottom: 10, opacity: 0.85 }}>
            <div className="sk-body" style={{ padding: 14, fontSize: 15, display: 'flex', alignItems: 'center', gap: 10, textDecoration: 'line-through', textDecorationColor: SK.ink }}>
              <SKIcon.x size={18} /> <b>A.</b> Que leer está prohibido en la era digital.
            </div>
          </SKBox>
          <div className="sk-label" style={{ fontSize: 12, color: SK.mute, marginBottom: 6, textTransform: 'uppercase', letterSpacing: 1 }}>Respuesta correcta</div>
          <SKBox radius={8} strokeWidth={2} fill={SK.mint} style={{ marginBottom: 20 }}>
            <div className="sk-body" style={{ padding: 14, fontSize: 15, display: 'flex', alignItems: 'center', gap: 10 }}>
              <SKIcon.check size={18} /> <b>B.</b> Que leer desafía los hábitos de atención actuales.
            </div>
          </SKBox>

          <div style={{ display: 'flex', gap: 8 }}>
            <SKButton variant="primary" size="lg" style={{ flex: 1 }}>Entendido, siguiente →</SKButton>
            <SKButton variant="ghost" size="lg">Revisar de nuevo</SKButton>
          </div>
        </div>

        <div>
          <div className="sk-label" style={{ fontSize: 12, color: SK.mute, marginBottom: 8, textTransform: 'uppercase', letterSpacing: 1 }}>Solución paso a paso</div>
          <SKBox radius={10} strokeWidth={1.6}>
            <div style={{ padding: 20 }}>
              <div className="sk-h" style={{ fontSize: 20, marginBottom: 12 }}>¿Qué falló y cómo mejorar?</div>

              {[
                ['1', 'Lee "subversivo" en contexto', 'En el párrafo 2 no aparece solo — sigue con "No produce dopamina rápida". Busca pistas cercanas.'],
                ['2', 'Separa literal de figurado', '"Prohibido" (A) es literal. El autor usa metáfora.'],
                ['3', 'Elimina extremos', 'Las opciones con palabras absolutas ("prohibido", "rebeldes") rara vez son correctas en Interpretar.'],
              ].map(([n, t, d]) => (
                <div key={n} style={{ display: 'flex', gap: 12, marginBottom: 14 }}>
                  <SKBox radius={14} strokeWidth={1.6} fill={SK.hi} style={{ width: 28, height: 28, flexShrink: 0 }}>
                    <div className="sk-h" style={{ textAlign: 'center', lineHeight: '28px', fontSize: 14 }}>{n}</div>
                  </SKBox>
                  <div>
                    <div className="sk-h" style={{ fontSize: 16, marginBottom: 2 }}>{t}</div>
                    <div className="sk-body" style={{ fontSize: 13, color: SK.ink2, lineHeight: 1.5 }}>{d}</div>
                  </div>
                </div>
              ))}

              <SKDivider style={{ margin: '10px 0' }} />
              <SKHatch style={{ height: 100, borderRadius: 6 }} label="Video · 60 seg · resolución guiada" />
            </div>
          </SKBox>
          <div style={{ marginTop: 12, display: 'flex', gap: 8, alignItems: 'center' }}>
            <SKAnnotation rotate={-2}>consejo: marca frases clave al leer ✏️</SKAnnotation>
            <div style={{ flex: 1 }} />
            <SKButton size="sm" variant="ghost">Practicar Interpretar ↗</SKButton>
          </div>
        </div>
      </div>
    </WebChrome>
  );
}

// ── 09. HISTORIAL ────────────────────────────────────────────────
function WebHistory() {
  const entries = [
    { d: 'Hoy', items: [
      { t: 'El valor de la lectura', type: 'Práctica rápida', score: '4/5', time: '8 min', result: 'good' },
      { t: 'Crónica del apagón', type: 'Práctica rápida', score: '3/5', time: '9 min', result: 'mid' },
    ]},
    { d: 'Ayer', items: [
      { t: 'PAES 2024 · Regular', type: 'Ensayo DEMRE', score: '52/65', time: '2h 22min', result: 'good' },
    ]},
    { d: 'Lun 21 Abr', items: [
      { t: 'Pablo Neruda, fragmento', type: 'Práctica rápida', score: '2/5', time: '11 min', result: 'bad' },
      { t: 'La crisis del agua', type: 'Práctica rápida', score: '5/5', time: '7 min', result: 'good' },
    ]},
  ];
  return (
    <WebChrome page="historial">
      <div style={{ padding: '32px 48px' }}>
        <div className="sk-h" style={{ fontSize: 40, marginBottom: 4 }}>Tu historial</div>
        <div className="sk-body" style={{ fontSize: 15, color: SK.ink2, marginBottom: 24 }}>Todo lo que has practicado. Clic en cualquier ítem para revisar.</div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 280px', gap: 24 }}>
          <div>
            {entries.map(day => (
              <div key={day.d} style={{ marginBottom: 24 }}>
                <div className="sk-h" style={{ fontSize: 18, marginBottom: 10, display: 'flex', alignItems: 'center', gap: 8 }}>
                  {day.d} <div style={{ flex: 1, borderTop: `1px dashed ${SK.ink}`, opacity: 0.3 }} />
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                  {day.items.map((it, i) => {
                    const fill = it.result === 'good' ? SK.mint : it.result === 'mid' ? SK.hi : SK.coral;
                    return (
                      <SKBox key={i} radius={8} strokeWidth={1.4}>
                        <div style={{ padding: 14, display: 'grid', gridTemplateColumns: '8px 1fr auto auto', gap: 14, alignItems: 'center' }}>
                          <SKBox fill={fill} radius={4} style={{ width: 8, height: 32 }} strokeWidth={0}/>
                          <div>
                            <div className="sk-body" style={{ fontSize: 15, fontWeight: 700 }}>{it.t}</div>
                            <div className="sk-mono" style={{ fontSize: 11, color: SK.mute }}>{it.type} · {it.time}</div>
                          </div>
                          <div className="sk-h" style={{ fontSize: 22 }}>{it.score}</div>
                          <SKIcon.arrow size={18} />
                        </div>
                      </SKBox>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          {/* Sidebar filters */}
          <div>
            <SKBox radius={10} strokeWidth={1.4}>
              <div style={{ padding: 16 }}>
                <div className="sk-h" style={{ fontSize: 18, marginBottom: 10 }}>Filtros</div>
                <div className="sk-label" style={{ fontSize: 12, marginBottom: 4 }}>Tipo</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 4, marginBottom: 14 }}>
                  {['Todos', 'Ensayos DEMRE', 'Prácticas rápidas', 'Prueba gratis'].map((x, i) => (
                    <div key={x} className="sk-body" style={{ fontSize: 13, display: 'flex', alignItems: 'center', gap: 8 }}>
                      <SKBox radius={3} strokeWidth={1.4} fill={i === 0 ? SK.ink : 'transparent'} style={{ width: 14, height: 14 }}>
                        {i === 0 && <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}><SKIcon.check size={10} stroke={SK.paper}/></div>}
                      </SKBox>
                      {x}
                    </div>
                  ))}
                </div>
                <div className="sk-label" style={{ fontSize: 12, marginBottom: 4 }}>Resultado</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                  {['Todos', 'Buenos (70%+)', 'A mejorar'].map((x, i) => (
                    <div key={x} className="sk-body" style={{ fontSize: 13, display: 'flex', alignItems: 'center', gap: 8 }}>
                      <SKBox radius={3} strokeWidth={1.4} style={{ width: 14, height: 14 }} />{x}
                    </div>
                  ))}
                </div>
              </div>
            </SKBox>
          </div>
        </div>
      </div>
    </WebChrome>
  );
}

// ── 10. AVANCE / PROGRESO ────────────────────────────────────────
function WebProgress() {
  return (
    <WebChrome page="avance">
      <div style={{ padding: '32px 48px' }}>
        <div className="sk-h" style={{ fontSize: 40, marginBottom: 4 }}>Tu avance</div>
        <div className="sk-body" style={{ fontSize: 15, color: SK.ink2, marginBottom: 24 }}>Las últimas 4 semanas. Vas subiendo 📈</div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 14, marginBottom: 28 }}>
          {[
            ['Nivel', '4', 'próx: 620 XP', SKIcon.star],
            ['Racha', '12 días', 'récord: 18', SKIcon.flame],
            ['% acierto', '68%', '+12% vs mes', SKIcon.target],
            ['Ejercicios', '143', 'esta semana: 28', SKIcon.book],
          ].map(([l, v, sub, I]) => (
            <SKBox key={l} radius={10} strokeWidth={1.6}>
              <div style={{ padding: 16 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <div className="sk-label" style={{ fontSize: 12, color: SK.mute }}>{l}</div>
                  <I size={18} />
                </div>
                <div className="sk-h" style={{ fontSize: 32, lineHeight: 1 }}>{v}</div>
                <div className="sk-mono" style={{ fontSize: 10, color: SK.mute, marginTop: 4 }}>{sub}</div>
              </div>
            </SKBox>
          ))}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: 20 }}>
          <SKBox radius={10} strokeWidth={1.6}>
            <div style={{ padding: 18 }}>
              <div className="sk-h" style={{ fontSize: 20, marginBottom: 14 }}>% acierto por semana</div>
              <SKChart />
            </div>
          </SKBox>

          <SKBox radius={10} strokeWidth={1.6}>
            <div style={{ padding: 18 }}>
              <div className="sk-h" style={{ fontSize: 20, marginBottom: 14 }}>Por habilidad</div>
              {[
                ['Localizar', 0.85, SK.mint],
                ['Interpretar', 0.62, SK.hi],
                ['Evaluar', 0.34, SK.coral],
              ].map(([n, v, c]) => (
                <div key={n} style={{ marginBottom: 14 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <div className="sk-body" style={{ fontSize: 14, fontWeight: 700 }}>{n}</div>
                    <div className="sk-mono" style={{ fontSize: 12 }}>{Math.round(v*100)}%</div>
                  </div>
                  <SKProgress value={v} height={12} color={c} />
                </div>
              ))}
              <SKDivider style={{ margin: '14px 0' }} />
              <SKAnnotation rotate={-1}>💡 Enfócate en "Evaluar" esta semana</SKAnnotation>
            </div>
          </SKBox>
        </div>
      </div>
    </WebChrome>
  );
}

// Simple sketchy bar chart
function SKChart() {
  const data = [0.45, 0.52, 0.58, 0.51, 0.63, 0.68, 0.72];
  const labels = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7'];
  return (
    <div style={{ position: 'relative', height: 180 }}>
      <svg viewBox="0 0 300 180" style={{ width: '100%', height: '100%' }} preserveAspectRatio="none">
        {/* Grid lines */}
        {[0, 1, 2, 3].map(i => (
          <line key={i} x1="20" y1={30 + i * 35} x2="290" y2={30 + i * 35} stroke={SK.ink} strokeWidth="0.6" strokeDasharray="2 3" opacity="0.3" />
        ))}
        {/* Line */}
        <polyline
          points={data.map((v, i) => `${25 + i * 40},${160 - v * 120}`).join(' ')}
          fill="none" stroke={SK.ink} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"
        />
        {/* Dots */}
        {data.map((v, i) => (
          <circle key={i} cx={25 + i * 40} cy={160 - v * 120} r="4" fill={SK.hi} stroke={SK.ink} strokeWidth="1.5" />
        ))}
        {/* Labels */}
        {labels.map((l, i) => (
          <text key={l} x={25 + i * 40} y="175" fontSize="10" fontFamily="JetBrains Mono, monospace" textAnchor="middle" fill={SK.mute}>{l}</text>
        ))}
      </svg>
    </div>
  );
}

// ── 11. DESAFÍOS ─────────────────────────────────────────────────
function WebChallenges() {
  const daily = [
    { t: 'Racha diaria', d: 'Practica 3 ejercicios hoy', p: 0.66, xp: 50, icon: SKIcon.flame, status: 'ongoing' },
    { t: 'Top Evaluar', d: 'Responde 5 preguntas de Evaluar', p: 0.2, xp: 80, icon: SKIcon.target, status: 'ongoing' },
  ];
  const weekly = [
    { t: 'Maratón semanal', d: 'Completa 20 ejercicios en 7 días', p: 0.45, xp: 200, icon: SKIcon.bolt, status: 'ongoing' },
    { t: 'Ensayista', d: 'Termina 1 ensayo DEMRE completo', p: 1, xp: 300, icon: SKIcon.book, status: 'done' },
  ];
  return (
    <WebChrome page="desafios">
      <div style={{ padding: '32px 48px' }}>
        <div className="sk-h" style={{ fontSize: 40, marginBottom: 4 }}>Desafíos</div>
        <div className="sk-body" style={{ fontSize: 15, color: SK.ink2, marginBottom: 24 }}>
          Metas semanales y diarias. Gana XP y sube de nivel.
        </div>

        {/* Daily */}
        <div className="sk-h" style={{ fontSize: 22, marginBottom: 10, display: 'flex', alignItems: 'center', gap: 8 }}>
          <SKIcon.flame size={22} /> Hoy
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 14, marginBottom: 28 }}>
          {daily.map((c, i) => <ChallengeCard key={i} c={c} />)}
        </div>

        {/* Weekly */}
        <div className="sk-h" style={{ fontSize: 22, marginBottom: 10, display: 'flex', alignItems: 'center', gap: 8 }}>
          <SKIcon.trophy size={22} /> Esta semana
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 14, marginBottom: 28 }}>
          {weekly.map((c, i) => <ChallengeCard key={i} c={c} />)}
        </div>

        {/* Achievements */}
        <div className="sk-h" style={{ fontSize: 22, marginBottom: 10, display: 'flex', alignItems: 'center', gap: 8 }}>
          <SKIcon.star size={22} fill={SK.hi} /> Logros
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 12 }}>
          {[
            { n: 'Primer paso', u: true, c: SK.mint },
            { n: 'Racha 7d', u: true, c: SK.hi },
            { n: '100 correctas', u: true, c: SK.hi },
            { n: 'Racha 14d', u: false, c: null },
            { n: 'Maestro Evaluar', u: false, c: null },
            { n: '1er ensayo 80%+', u: false, c: null },
          ].map((a, i) => (
            <div key={i} style={{ textAlign: 'center', opacity: a.u ? 1 : 0.4 }}>
              <SKBox radius={40} strokeWidth={1.8} fill={a.c || 'transparent'} style={{ width: 72, height: 72, margin: '0 auto 6px' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                  <SKIcon.trophy size={30} />
                </div>
              </SKBox>
              <div className="sk-label" style={{ fontSize: 11 }}>{a.n}</div>
            </div>
          ))}
        </div>
      </div>
    </WebChrome>
  );
}

function ChallengeCard({ c }) {
  const Icon = c.icon;
  const done = c.status === 'done';
  return (
    <SKBox radius={10} strokeWidth={1.6} fill={done ? SK.mint : 'transparent'}>
      <div style={{ padding: 16, display: 'grid', gridTemplateColumns: '44px 1fr auto', gap: 12, alignItems: 'center' }}>
        <SKBox radius={22} strokeWidth={1.6} fill={done ? SK.ink : SK.hi} style={{ width: 44, height: 44 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
            <Icon size={22} stroke={done ? SK.paper : SK.ink} />
          </div>
        </SKBox>
        <div>
          <div className="sk-h" style={{ fontSize: 18 }}>{c.t}</div>
          <div className="sk-body" style={{ fontSize: 13, color: SK.ink2, marginBottom: 6 }}>{c.d}</div>
          <SKProgress value={c.p} height={6} />
        </div>
        <div style={{ textAlign: 'right' }}>
          <div className="sk-h" style={{ fontSize: 18, color: SK.ink }}>+{c.xp}</div>
          <div className="sk-label" style={{ fontSize: 10, color: SK.mute }}>XP</div>
        </div>
      </div>
    </SKBox>
  );
}

Object.assign(window, {
  WebHome, WebEnsayos, WebPracticas, WebPromo, WebSelectText,
  WebQuestion, WebResultCorrect, WebResultWrong,
  WebHistory, WebProgress, WebChallenges,
});
