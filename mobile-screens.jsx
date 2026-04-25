// mobile-screens.jsx — Mobile app wireframes for PAESapp Lectora
// Phone frame: 300 x 620, tab bar at bottom.

const MOB_W = 300;
const MOB_H = 620;

function Phone({ children, tab = 'home', showNav = true, noPad = false }) {
  return (
    <div style={{ width: MOB_W, height: MOB_H, background: SK.paper, display: 'flex', flexDirection: 'column', position: 'relative', overflow: 'hidden' }}>
      {/* status bar */}
      <div className="sk-mono" style={{ padding: '6px 16px', fontSize: 10, display: 'flex', justifyContent: 'space-between', color: SK.ink }}>
        <span>9:41</span>
        <span>••• ▮</span>
      </div>
      <div className="sk-scroll" style={{ flex: 1, overflow: 'auto', padding: noPad ? 0 : '0 14px' }}>
        {children}
      </div>
      {showNav && <PhoneNav tab={tab} />}
    </div>
  );
}

function PhoneNav({ tab = 'home' }) {
  const tabs = [
    { id: 'home', icon: SKIcon.home, l: 'Inicio' },
    { id: 'hist', icon: SKIcon.history, l: 'Historial' },
    { id: 'avance', icon: SKIcon.chart, l: 'Avance' },
    { id: 'desafios', icon: SKIcon.trophy, l: 'Desafíos' },
  ];
  return (
    <div style={{ borderTop: `1.5px dashed ${SK.ink}`, display: 'flex', padding: '8px 0 10px', background: SK.paper }}>
      {tabs.map(t => {
        const active = t.id === tab;
        const Icon = t.icon;
        return (
          <div key={t.id} style={{ flex: 1, textAlign: 'center', position: 'relative' }}>
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 2 }}>
              <Icon size={20} stroke={active ? SK.ink : SK.mute} />
            </div>
            <div className="sk-label" style={{ fontSize: 10, color: active ? SK.ink : SK.mute, fontWeight: active ? 700 : 400 }}>{t.l}</div>
            {active && <div style={{ position: 'absolute', top: -8, left: '50%', transform: 'translateX(-50%)', width: 24, height: 3, background: SK.ink, borderRadius: 2 }} />}
          </div>
        );
      })}
    </div>
  );
}

// ── M01 HOME ─────────────────────────────────────────────────────
function MobHome() {
  return (
    <Phone tab="home">
      <div style={{ padding: '10px 0 6px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <div className="sk-label" style={{ fontSize: 11, color: SK.mute }}>Hola,</div>
          <div className="sk-h" style={{ fontSize: 22, lineHeight: 1 }}>Martina 👋</div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <div className="sk-label" style={{ fontSize: 11, display: 'flex', alignItems: 'center', gap: 3 }}>
            <SKIcon.flame size={14} stroke={SK.coral} fill={SK.coral} />12d
          </div>
          <SKBox radius={16} strokeWidth={1.4} style={{ width: 32, height: 32 }}>
            <div className="sk-h" style={{ textAlign: 'center', lineHeight: '32px', fontSize: 16 }}>M</div>
          </SKBox>
        </div>
      </div>

      {/* Progress card */}
      <SKBox radius={10} strokeWidth={1.6} style={{ marginTop: 6, marginBottom: 14 }}>
        <div style={{ padding: 12 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
            <div className="sk-body" style={{ fontSize: 13, fontWeight: 700 }}>Nivel 4</div>
            <div className="sk-mono" style={{ fontSize: 10, color: SK.mute }}>2,480 / 3,100 XP</div>
          </div>
          <SKProgress value={0.8} height={8} />
        </div>
      </SKBox>

      <div className="sk-h" style={{ fontSize: 18, marginBottom: 8 }}>¿Qué harás hoy?</div>

      {/* PROMO card — destacada */}
      <div style={{ position: 'relative', marginBottom: 10 }}>
        <SKBox radius={12} fill={SK.coral} strokeWidth={2.2} shadow>
          <div style={{ padding: 14 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 4 }}>
              <SKBadge color={SK.ink}><span style={{ color: SK.paper }}>GRATIS</span></SKBadge>
              <SKIcon.gift size={18} />
            </div>
            <div className="sk-h" style={{ fontSize: 22, lineHeight: 1.05, marginTop: 6 }}>Prueba corta</div>
            <div className="sk-body" style={{ fontSize: 12, lineHeight: 1.3, marginTop: 2, marginBottom: 10 }}>
              5 min · 3 preguntas · sin registro
            </div>
            <SKButton variant="primary" size="sm" style={{ width: '100%' }}>¡Empezar! →</SKButton>
          </div>
        </SKBox>
        <SKAnnotation style={{ position: 'absolute', top: -6, right: -14, fontSize: 11 }} rotate={8}>¡Pruébalo!</SKAnnotation>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 14 }}>
        <SKBox radius={10} strokeWidth={1.6}>
          <div style={{ padding: 12 }}>
            <SKIcon.book size={20} />
            <div className="sk-h" style={{ fontSize: 16, marginTop: 4 }}>Ensayo<br/>DEMRE</div>
            <div className="sk-mono" style={{ fontSize: 9, color: SK.mute, marginTop: 4 }}>65 preg · 150min</div>
          </div>
        </SKBox>
        <SKBox radius={10} strokeWidth={1.6}>
          <div style={{ padding: 12 }}>
            <SKIcon.bolt size={20} fill={SK.hi} />
            <div className="sk-h" style={{ fontSize: 16, marginTop: 4 }}>Práctica<br/>rápida</div>
            <div className="sk-mono" style={{ fontSize: 9, color: SK.mute, marginTop: 4 }}>~10 min</div>
          </div>
        </SKBox>
      </div>

      {/* Scroll-down hint → tabs */}
      <div className="sk-label" style={{ fontSize: 11, color: SK.mute, textAlign: 'center', marginBottom: 8 }}>↓ desliza para ver más</div>

      <div className="sk-h" style={{ fontSize: 18, marginBottom: 8 }}>Tu panel</div>
      {[
        { l: 'Historial', icon: SKIcon.history, d: '28 ejercicios' },
        { l: 'Avance', icon: SKIcon.chart, d: '72% Inferir · 45% Evaluar' },
        { l: 'Desafíos', icon: SKIcon.trophy, d: '2 nuevos · +250 XP', hi: true },
      ].map((t, i) => {
        const Icon = t.icon;
        return (
          <SKBox key={i} radius={8} strokeWidth={1.4} fill={t.hi ? SK.hi : 'transparent'} style={{ marginBottom: 8 }}>
            <div style={{ padding: 12, display: 'flex', alignItems: 'center', gap: 10 }}>
              <Icon size={18} />
              <div style={{ flex: 1 }}>
                <div className="sk-body" style={{ fontSize: 13, fontWeight: 700 }}>{t.l}</div>
                <div className="sk-mono" style={{ fontSize: 10, color: SK.mute }}>{t.d}</div>
              </div>
              <SKIcon.arrow size={16} />
            </div>
          </SKBox>
        );
      })}
      <div style={{ height: 8 }} />
    </Phone>
  );
}

// ── M02 ENSAYOS ──────────────────────────────────────────────────
function MobEnsayos() {
  return (
    <Phone tab="home">
      <div style={{ padding: '10px 0 4px' }}>
        <div className="sk-label" style={{ fontSize: 11, color: SK.mute, marginBottom: 2 }}>← Inicio</div>
        <div className="sk-h" style={{ fontSize: 26 }}>Ensayos DEMRE</div>
        <div className="sk-body" style={{ fontSize: 12, color: SK.ink2 }}>Pruebas completas oficiales</div>
      </div>
      <div style={{ display: 'flex', gap: 4, margin: '10px 0', overflowX: 'auto' }} className="sk-scroll">
        {['Todos', '2024', '2023', '2022', '2021'].map((f, i) => (
          <SKButton key={f} size="sm" variant={i === 0 ? 'primary' : 'ghost'}>{f}</SKButton>
        ))}
      </div>

      {[
        { year: '2024', name: 'PAES Regular', done: true, score: '52/65' },
        { year: '2023', name: 'PAES Invierno', done: false },
        { year: '2023', name: 'PAES Regular', done: false },
        { year: '2022', name: 'PDT Oficial', done: false },
      ].map((e, i) => (
        <SKBox key={i} radius={10} strokeWidth={1.4} style={{ marginBottom: 8 }}>
          <div style={{ padding: 12 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
              <SKBadge color={SK.paper}>{e.year}</SKBadge>
              {e.done && <div className="sk-label" style={{ fontSize: 10, color: SK.mint, display: 'flex', alignItems: 'center', gap: 2 }}><SKIcon.check size={10} stroke={SK.mint}/>Hecho · {e.score}</div>}
            </div>
            <div className="sk-h" style={{ fontSize: 16, marginBottom: 4 }}>{e.name}</div>
            <div className="sk-mono" style={{ fontSize: 10, color: SK.mute, marginBottom: 8 }}>65 preguntas · 150 min</div>
            <SKButton size="sm" variant={e.done ? 'ghost' : 'primary'} style={{ width: '100%' }}>
              {e.done ? 'Ver resultado' : 'Empezar →'}
            </SKButton>
          </div>
        </SKBox>
      ))}
      <div style={{ height: 4 }} />
    </Phone>
  );
}

// ── M03 PRÁCTICAS ────────────────────────────────────────────────
function MobPracticas() {
  return (
    <Phone tab="home">
      <div style={{ padding: '10px 0 4px' }}>
        <div className="sk-label" style={{ fontSize: 11, color: SK.mute }}>← Inicio</div>
        <div className="sk-h" style={{ fontSize: 26 }}>Práctica rápida</div>
        <div className="sk-body" style={{ fontSize: 12, color: SK.ink2 }}>Elige qué entrenar · 5 preg · ~10 min</div>
      </div>
      <div className="sk-h" style={{ fontSize: 14, margin: '12px 0 6px' }}>Por habilidad</div>
      {[
        ['Localizar', 0.85, SK.mint, 'L'],
        ['Interpretar', 0.62, SK.hi, 'I'],
        ['Evaluar', 0.34, SK.coral, 'E'],
      ].map(([n, p, c, l]) => (
        <SKBox key={n} radius={10} strokeWidth={1.4} style={{ marginBottom: 8 }}>
          <div style={{ padding: 10, display: 'flex', alignItems: 'center', gap: 10 }}>
            <SKBox fill={c} radius={6} style={{ width: 32, height: 32, flexShrink: 0 }}>
              <div className="sk-h" style={{ textAlign: 'center', lineHeight: '32px', fontSize: 16 }}>{l}</div>
            </SKBox>
            <div style={{ flex: 1 }}>
              <div className="sk-body" style={{ fontSize: 13, fontWeight: 700 }}>{n}</div>
              <SKProgress value={p} height={4} style={{ marginTop: 4 }} />
            </div>
            <div className="sk-mono" style={{ fontSize: 11 }}>{Math.round(p*100)}%</div>
            <SKIcon.arrow size={14} />
          </div>
        </SKBox>
      ))}

      <div className="sk-h" style={{ fontSize: 14, margin: '14px 0 6px' }}>Por tipo de texto</div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6 }}>
        {['Narrativo', 'Expositivo', 'Noticia', 'Columna', 'Poema', 'Ensayo'].map(t => (
          <SKBox key={t} radius={6} strokeWidth={1.2}>
            <div className="sk-body" style={{ padding: '8px 10px', fontSize: 12 }}>{t}</div>
          </SKBox>
        ))}
      </div>
      <div style={{ height: 4 }} />
    </Phone>
  );
}

// ── M04 SELECCIÓN DE TEXTO ───────────────────────────────────────
function MobSelectText() {
  const texts = [
    { t: 'El valor de la lectura', g: 'Ensayo', d: 'Media' },
    { t: 'Crónica del apagón', g: 'Noticia', d: 'Fácil' },
    { t: 'Pablo Neruda, fragmento', g: 'Poema', d: 'Difícil' },
    { t: 'La crisis del agua', g: 'Argumentativo', d: 'Media' },
  ];
  return (
    <Phone tab="home">
      <div style={{ padding: '10px 0 4px' }}>
        <div className="sk-label" style={{ fontSize: 10, color: SK.mute }}>← Interpretar</div>
        <div className="sk-h" style={{ fontSize: 22 }}>Elige un texto</div>
        <div className="sk-body" style={{ fontSize: 11, color: SK.ink2 }}>6 disponibles · habilidad: Interpretar</div>
      </div>

      <div style={{ marginTop: 10 }}>
        {texts.map((x, i) => (
          <SKBox key={i} radius={10} strokeWidth={1.4} style={{ marginBottom: 8 }}>
            <div style={{ padding: 10, display: 'grid', gridTemplateColumns: '50px 1fr auto', gap: 10, alignItems: 'center' }}>
              <SKHatch style={{ width: 50, height: 60, borderRadius: 4 }} label={x.g} />
              <div>
                <div style={{ display: 'flex', gap: 4, marginBottom: 3 }}>
                  <SKBadge color={x.d === 'Fácil' ? SK.mint : x.d === 'Media' ? SK.hi : SK.coral}>{x.d}</SKBadge>
                </div>
                <div className="sk-h" style={{ fontSize: 14, lineHeight: 1.1 }}>{x.t}</div>
                <div className="sk-mono" style={{ fontSize: 9, color: SK.mute, marginTop: 2 }}>5 preg · ~8 min</div>
              </div>
              <SKIcon.arrow size={16} />
            </div>
          </SKBox>
        ))}
      </div>
    </Phone>
  );
}

// ── M05 PREGUNTA ─────────────────────────────────────────────────
function MobQuestion() {
  return (
    <Phone tab="home">
      {/* Top progress */}
      <div style={{ padding: '8px 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
          <SKIcon.x size={16} />
          <SKProgress value={0.4} height={6} style={{ flex: 1 }} />
          <div className="sk-mono" style={{ fontSize: 10 }}>2/5</div>
        </div>
        <div className="sk-label" style={{ fontSize: 10, color: SK.mute, display: 'flex', justifyContent: 'space-between' }}>
          <span>Interpretar</span><span><SKIcon.clock size={10} /> 07:24</span>
        </div>
      </div>

      {/* Collapsed text */}
      <SKBox radius={8} strokeWidth={1.4} fill="#f7f4ec" style={{ marginTop: 6, marginBottom: 10 }}>
        <div style={{ padding: 10 }}>
          <div className="sk-label" style={{ fontSize: 9, color: SK.mute, textTransform: 'uppercase', letterSpacing: 1 }}>Texto</div>
          <div className="sk-h" style={{ fontSize: 14, marginBottom: 4 }}>El valor de la lectura</div>
          <div className="sk-body" style={{ fontSize: 11, lineHeight: 1.4, color: SK.ink2, maxHeight: 70, overflow: 'hidden', position: 'relative' }}>
            En la era del scroll infinito, <span style={{ background: SK.hi, padding: '0 2px' }}>la lectura profunda es un acto casi subversivo</span>. No produce dopamina rápida. No se comparte fácilmente. Requiere...
            <div style={{ position: 'absolute', bottom: 0, right: 0, background: '#f7f4ec', padding: '0 4px' }} className="sk-label">
              leer todo ↓
            </div>
          </div>
        </div>
      </SKBox>

      <div className="sk-h" style={{ fontSize: 15, lineHeight: 1.2, marginBottom: 10 }}>
        ¿Qué sugiere el autor al llamar a la lectura profunda "un acto casi subversivo"?
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
        {[
          { l: 'A', t: 'Que leer está prohibido en la era digital' },
          { l: 'B', t: 'Que leer desafía los hábitos de atención', sel: true },
          { l: 'C', t: 'Que los lectores son rebeldes' },
          { l: 'D', t: 'Que genera controversia política' },
        ].map(o => (
          <SKBox key={o.l} radius={8} strokeWidth={o.sel ? 2 : 1.4} fill={o.sel ? SK.hi : 'transparent'}>
            <div className="sk-body" style={{ padding: 9, fontSize: 12, display: 'flex', alignItems: 'center', gap: 8 }}>
              <SKBox radius={10} strokeWidth={1.4} fill={o.sel ? SK.ink : 'transparent'} style={{ width: 22, height: 22, flexShrink: 0 }}>
                <div className="sk-h" style={{ textAlign: 'center', lineHeight: '22px', fontSize: 11, color: o.sel ? SK.paper : SK.ink }}>{o.l}</div>
              </SKBox>
              <span>{o.t}</span>
            </div>
          </SKBox>
        ))}
      </div>

      <div style={{ marginTop: 12, marginBottom: 8 }}>
        <SKButton variant="primary" size="md" style={{ width: '100%' }}>Responder →</SKButton>
      </div>
    </Phone>
  );
}

// ── M06 RESULTADO CORRECTO ───────────────────────────────────────
function MobResultCorrect() {
  return (
    <Phone tab="home">
      <div style={{ paddingTop: 14, textAlign: 'center' }}>
        <SKBox radius={40} fill={SK.mint} strokeWidth={2.4} style={{ width: 80, height: 80, margin: '0 auto 10px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
            <SKIcon.check size={44} stroke={SK.ink} />
          </div>
        </SKBox>
        <div className="sk-h" style={{ fontSize: 32 }}>¡Correcto!</div>
        <div className="sk-body" style={{ fontSize: 13, color: SK.ink2 }}>+15 XP · racha de 4 🔥</div>
      </div>

      <SKDivider style={{ margin: '14px 0' }} />

      <div className="sk-label" style={{ fontSize: 10, textTransform: 'uppercase', letterSpacing: 1, color: SK.mute, marginBottom: 4 }}>Tu respuesta</div>
      <SKBox radius={8} strokeWidth={1.6} fill={SK.mint} style={{ marginBottom: 10 }}>
        <div className="sk-body" style={{ padding: 10, fontSize: 12, display: 'flex', alignItems: 'center', gap: 8 }}>
          <SKIcon.check size={14} /> <b>B.</b> Desafía hábitos de atención
        </div>
      </SKBox>

      <div className="sk-label" style={{ fontSize: 10, textTransform: 'uppercase', letterSpacing: 1, color: SK.mute, marginBottom: 4 }}>Explicación</div>
      <SKBox radius={8} strokeWidth={1.4}>
        <div style={{ padding: 10 }}>
          <div className="sk-body" style={{ fontSize: 12, lineHeight: 1.4 }}>
            "Subversivo" es figurado. Fíjate en: <span style={{ background: SK.hi }}>"No produce dopamina rápida"</span> — la lectura va <b>contra</b> los hábitos digitales.
          </div>
          <SKHatch style={{ height: 60, borderRadius: 4, marginTop: 8 }} label="Video · 45s" />
        </div>
      </SKBox>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 6, marginTop: 10 }}>
        {[['0:42', 'tiempo'], ['72%', 'acierto'], ['4', 'racha']].map(([v, l]) => (
          <SKBox key={l} radius={6} strokeWidth={1.2}>
            <div style={{ padding: 6, textAlign: 'center' }}>
              <div className="sk-h" style={{ fontSize: 16 }}>{v}</div>
              <div className="sk-label" style={{ fontSize: 9, color: SK.mute }}>{l}</div>
            </div>
          </SKBox>
        ))}
      </div>

      <div style={{ marginTop: 10, display: 'flex', gap: 6 }}>
        <SKButton variant="ghost" size="sm" icon={<SKIcon.share size={12} />} style={{ flex: '0 0 auto' }}>Compartir</SKButton>
        <SKButton variant="primary" size="sm" style={{ flex: 1 }}>Siguiente →</SKButton>
      </div>
      <div style={{ height: 6 }} />
    </Phone>
  );
}

// ── M07 RESULTADO INCORRECTO ─────────────────────────────────────
function MobResultWrong() {
  return (
    <Phone tab="home">
      <div style={{ paddingTop: 14, textAlign: 'center' }}>
        <SKBox radius={40} fill={SK.coral} strokeWidth={2.4} style={{ width: 80, height: 80, margin: '0 auto 10px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
            <SKIcon.x size={44} stroke={SK.ink} />
          </div>
        </SKBox>
        <div className="sk-h" style={{ fontSize: 26 }}>Casi lo tenías</div>
        <div className="sk-body" style={{ fontSize: 12, color: SK.ink2 }}>Vas a aprender de esta ✏️</div>
      </div>

      <div className="sk-label" style={{ fontSize: 10, textTransform: 'uppercase', letterSpacing: 1, color: SK.mute, marginTop: 12, marginBottom: 4 }}>Tú elegiste</div>
      <SKBox radius={8} strokeWidth={1.6} fill={SK.coral} style={{ marginBottom: 8, opacity: 0.8 }}>
        <div className="sk-body" style={{ padding: 8, fontSize: 12, textDecoration: 'line-through' }}>
          <SKIcon.x size={12} /> <b>A.</b> Está prohibido en la era digital
        </div>
      </SKBox>
      <div className="sk-label" style={{ fontSize: 10, textTransform: 'uppercase', letterSpacing: 1, color: SK.mute, marginBottom: 4 }}>Respuesta correcta</div>
      <SKBox radius={8} strokeWidth={1.6} fill={SK.mint} style={{ marginBottom: 10 }}>
        <div className="sk-body" style={{ padding: 8, fontSize: 12 }}>
          <SKIcon.check size={12} /> <b>B.</b> Desafía hábitos de atención
        </div>
      </SKBox>

      <div className="sk-label" style={{ fontSize: 10, textTransform: 'uppercase', letterSpacing: 1, color: SK.mute, marginBottom: 4 }}>Paso a paso</div>
      <SKBox radius={8} strokeWidth={1.4}>
        <div style={{ padding: 10 }}>
          {[
            ['1', 'Lee "subversivo" en contexto'],
            ['2', 'Separa literal de figurado'],
            ['3', 'Elimina palabras absolutas'],
          ].map(([n, t]) => (
            <div key={n} style={{ display: 'flex', gap: 8, marginBottom: 6 }}>
              <SKBox radius={10} fill={SK.hi} strokeWidth={1.2} style={{ width: 20, height: 20, flexShrink: 0 }}>
                <div className="sk-h" style={{ textAlign: 'center', lineHeight: '20px', fontSize: 11 }}>{n}</div>
              </SKBox>
              <div className="sk-body" style={{ fontSize: 12 }}>{t}</div>
            </div>
          ))}
          <SKHatch style={{ height: 50, borderRadius: 4, marginTop: 6 }} label="Video · 60s resolución" />
        </div>
      </SKBox>

      <div style={{ marginTop: 10 }}>
        <SKButton variant="primary" size="sm" style={{ width: '100%' }}>Entendido, siguiente →</SKButton>
      </div>
      <div style={{ height: 6 }} />
    </Phone>
  );
}

// ── M08 HISTORIAL ───────────────────────────────────────────────
function MobHistory() {
  return (
    <Phone tab="hist">
      <div style={{ padding: '10px 0' }}>
        <div className="sk-h" style={{ fontSize: 24 }}>Historial</div>
      </div>

      {[
        { d: 'Hoy', items: [
          { t: 'El valor de la lectura', s: '4/5', r: 'good' },
          { t: 'Crónica del apagón', s: '3/5', r: 'mid' },
        ]},
        { d: 'Ayer', items: [
          { t: 'PAES 2024 Regular', s: '52/65', r: 'good' },
        ]},
        { d: 'Lun 21', items: [
          { t: 'Neruda fragmento', s: '2/5', r: 'bad' },
          { t: 'Crisis del agua', s: '5/5', r: 'good' },
        ]},
      ].map(day => (
        <div key={day.d} style={{ marginBottom: 14 }}>
          <div className="sk-h" style={{ fontSize: 13, marginBottom: 6, color: SK.ink2 }}>{day.d}</div>
          {day.items.map((it, i) => {
            const c = it.r === 'good' ? SK.mint : it.r === 'mid' ? SK.hi : SK.coral;
            return (
              <SKBox key={i} radius={8} strokeWidth={1.2} style={{ marginBottom: 6 }}>
                <div style={{ padding: 10, display: 'grid', gridTemplateColumns: '6px 1fr auto', gap: 10, alignItems: 'center' }}>
                  <div style={{ width: 6, height: 28, background: c, borderRadius: 3 }} />
                  <div>
                    <div className="sk-body" style={{ fontSize: 12, fontWeight: 700 }}>{it.t}</div>
                    <div className="sk-mono" style={{ fontSize: 9, color: SK.mute }}>Práctica rápida</div>
                  </div>
                  <div className="sk-h" style={{ fontSize: 16 }}>{it.s}</div>
                </div>
              </SKBox>
            );
          })}
        </div>
      ))}
    </Phone>
  );
}

// ── M09 AVANCE ──────────────────────────────────────────────────
function MobProgress() {
  return (
    <Phone tab="avance">
      <div style={{ padding: '10px 0 4px' }}>
        <div className="sk-h" style={{ fontSize: 24 }}>Tu avance</div>
        <div className="sk-body" style={{ fontSize: 11, color: SK.ink2 }}>Últimas 4 semanas</div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6, marginTop: 10 }}>
        {[['Nivel', '4'], ['Racha', '12d'], ['%', '68%'], ['Ejerc.', '143']].map(([l, v]) => (
          <SKBox key={l} radius={8} strokeWidth={1.4}>
            <div style={{ padding: 8 }}>
              <div className="sk-label" style={{ fontSize: 10, color: SK.mute }}>{l}</div>
              <div className="sk-h" style={{ fontSize: 22 }}>{v}</div>
            </div>
          </SKBox>
        ))}
      </div>

      <div className="sk-h" style={{ fontSize: 14, marginTop: 14, marginBottom: 6 }}>% acierto semanal</div>
      <SKBox radius={8} strokeWidth={1.4}>
        <div style={{ padding: 10 }}>
          <SKChartMobile />
        </div>
      </SKBox>

      <div className="sk-h" style={{ fontSize: 14, marginTop: 12, marginBottom: 6 }}>Por habilidad</div>
      {[['Localizar', 0.85, SK.mint], ['Interpretar', 0.62, SK.hi], ['Evaluar', 0.34, SK.coral]].map(([n, v, c]) => (
        <div key={n} style={{ marginBottom: 8 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <div className="sk-body" style={{ fontSize: 12, fontWeight: 700 }}>{n}</div>
            <div className="sk-mono" style={{ fontSize: 11 }}>{Math.round(v*100)}%</div>
          </div>
          <SKProgress value={v} height={8} color={c} />
        </div>
      ))}
      <SKAnnotation style={{ marginTop: 10 }} rotate={-2}>💡 Refuerza "Evaluar"</SKAnnotation>
      <div style={{ height: 8 }} />
    </Phone>
  );
}

function SKChartMobile() {
  const data = [0.45, 0.52, 0.58, 0.51, 0.63, 0.68, 0.72];
  return (
    <svg viewBox="0 0 260 100" style={{ width: '100%', height: 90 }} preserveAspectRatio="none">
      {[0, 1, 2].map(i => (
        <line key={i} x1="10" y1={20 + i * 28} x2="250" y2={20 + i * 28} stroke={SK.ink} strokeWidth="0.5" strokeDasharray="2 3" opacity="0.3" />
      ))}
      <polyline
        points={data.map((v, i) => `${15 + i * 38},${90 - v * 70}`).join(' ')}
        fill="none" stroke={SK.ink} strokeWidth="2" strokeLinecap="round"
      />
      {data.map((v, i) => (
        <circle key={i} cx={15 + i * 38} cy={90 - v * 70} r="3" fill={SK.hi} stroke={SK.ink} strokeWidth="1.2" />
      ))}
    </svg>
  );
}

// ── M10 DESAFÍOS ────────────────────────────────────────────────
function MobChallenges() {
  return (
    <Phone tab="desafios">
      <div style={{ padding: '10px 0' }}>
        <div className="sk-h" style={{ fontSize: 24 }}>Desafíos</div>
        <div className="sk-body" style={{ fontSize: 11, color: SK.ink2 }}>Gana XP · sube de nivel</div>
      </div>

      <div className="sk-h" style={{ fontSize: 14, marginTop: 10, marginBottom: 6, display: 'flex', gap: 4, alignItems: 'center' }}>
        <SKIcon.flame size={14} /> Hoy
      </div>
      {[
        { t: 'Racha diaria', d: '3 ejercicios', p: 0.66, xp: 50, i: SKIcon.flame },
        { t: 'Top Evaluar', d: '5 preg de Evaluar', p: 0.2, xp: 80, i: SKIcon.target },
      ].map((c, i) => {
        const I = c.i;
        return (
          <SKBox key={i} radius={8} strokeWidth={1.4} style={{ marginBottom: 6 }}>
            <div style={{ padding: 10, display: 'flex', alignItems: 'center', gap: 8 }}>
              <SKBox radius={14} fill={SK.hi} strokeWidth={1.4} style={{ width: 28, height: 28, flexShrink: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}><I size={14} /></div>
              </SKBox>
              <div style={{ flex: 1 }}>
                <div className="sk-body" style={{ fontSize: 12, fontWeight: 700 }}>{c.t}</div>
                <div className="sk-mono" style={{ fontSize: 9, color: SK.mute, marginBottom: 3 }}>{c.d}</div>
                <SKProgress value={c.p} height={4} />
              </div>
              <div className="sk-h" style={{ fontSize: 14 }}>+{c.xp}</div>
            </div>
          </SKBox>
        );
      })}

      <div className="sk-h" style={{ fontSize: 14, marginTop: 12, marginBottom: 6, display: 'flex', gap: 4, alignItems: 'center' }}>
        <SKIcon.trophy size={14} /> Logros
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8 }}>
        {[['✓', SK.mint], ['✓', SK.hi], ['✓', SK.hi], ['?', null], ['?', null], ['?', null], ['?', null], ['?', null]].map(([s, c], i) => (
          <div key={i} style={{ textAlign: 'center', opacity: c ? 1 : 0.4 }}>
            <SKBox radius={24} fill={c || 'transparent'} strokeWidth={1.4} style={{ width: 44, height: 44, margin: '0 auto' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                <SKIcon.trophy size={20} />
              </div>
            </SKBox>
          </div>
        ))}
      </div>
      <div style={{ height: 6 }} />
    </Phone>
  );
}

Object.assign(window, {
  MobHome, MobEnsayos, MobPracticas, MobSelectText,
  MobQuestion, MobResultCorrect, MobResultWrong,
  MobHistory, MobProgress, MobChallenges,
});
