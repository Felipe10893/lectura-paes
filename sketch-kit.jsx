// sketch-kit.jsx — low-fi sketch UI primitives shared across wireframes
// Handwritten fonts, wobbly borders, hatched placeholders. All black/white
// with tiny accents.

const SK = {
  paper: '#fdfcf7',
  ink: '#2a2622',
  ink2: '#4a4238',
  mute: '#8a8278',
  line: '#2a2622',
  hi: '#ffe66b',     // highlighter yellow
  coral: '#ff8b6b',  // promo / CTA
  mint: '#9fd8c2',   // secondary accent
  lav: '#c8b6e8',    // tertiary accent
};

// Inject global sketch styles once
if (typeof document !== 'undefined' && !document.getElementById('sk-styles')) {
  const s = document.createElement('style');
  s.id = 'sk-styles';
  s.textContent = `
    @import url('https://fonts.googleapis.com/css2?family=Kalam:wght@300;400;700&family=Caveat:wght@400;600;700&family=Architects+Daughter&family=JetBrains+Mono:wght@400;600&display=swap');
    .sk-h, .sk-body, .sk-label, .sk-mono { color: ${SK.ink}; }
    .sk-h { font-family: 'Caveat', cursive; font-weight: 700; letter-spacing: 0.5px; }
    .sk-body { font-family: 'Kalam', cursive; font-weight: 400; }
    .sk-label { font-family: 'Architects Daughter', cursive; }
    .sk-mono { font-family: 'JetBrains Mono', monospace; font-weight: 400; }
    .sk-scroll { scrollbar-width: none; }
    .sk-scroll::-webkit-scrollbar { display: none; }
  `;
  document.head.appendChild(s);
}

// Wobbly border box (SVG rough rect)
function SKBox({ children, style = {}, fill = 'transparent', stroke = SK.ink, strokeWidth = 1.8, radius = 8, dashed = false, shadow = false, className = '' }) {
  // Slight random offsets for hand-drawn feel — seeded per mount
  const seed = React.useMemo(() => Math.random(), []);
  const wob = (n) => (Math.sin(seed * 100 + n) * 1.2);
  return (
    <div className={className} style={{ position: 'relative', ...style }}>
      <svg style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', pointerEvents: 'none', overflow: 'visible' }} preserveAspectRatio="none">
        <rect
          x={1 + wob(1)} y={1 + wob(2)}
          width={`calc(100% - ${2 + wob(3)}px)`} height={`calc(100% - ${2 + wob(4)}px)`}
          rx={radius} ry={radius}
          fill={fill} stroke={stroke} strokeWidth={strokeWidth}
          strokeDasharray={dashed ? '6 4' : 'none'}
          strokeLinejoin="round"
        />
        {shadow && (
          <rect
            x={3 + wob(5)} y={3 + wob(6)}
            width={`calc(100% - ${6 + wob(7)}px)`} height={`calc(100% - ${6 + wob(8)}px)`}
            rx={radius} ry={radius}
            fill="none" stroke={stroke} strokeWidth="0.8" opacity="0.3"
            transform="translate(3, 3)"
          />
        )}
      </svg>
      <div style={{ position: 'relative', zIndex: 1, width: '100%', height: '100%' }}>{children}</div>
    </div>
  );
}

// Hatched placeholder (for images / illustrations)
function SKHatch({ style = {}, label, children, stroke = SK.ink }) {
  return (
    <div style={{ position: 'relative', overflow: 'hidden', background: 'transparent', ...style }}>
      <svg style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
        <defs>
          <pattern id={`hatch-${stroke.replace('#','')}`} patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)">
            <line x1="0" y1="0" x2="0" y2="8" stroke={stroke} strokeWidth="0.8" opacity="0.25" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill={`url(#hatch-${stroke.replace('#','')})`} />
        <rect width="100%" height="100%" fill="none" stroke={stroke} strokeWidth="1.5" strokeDasharray="4 3" />
      </svg>
      {label && (
        <div className="sk-mono" style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 10, color: SK.mute, textAlign: 'center', padding: 8, textTransform: 'uppercase', letterSpacing: 1 }}>
          {label}
        </div>
      )}
      {children}
    </div>
  );
}

// Sketchy button
function SKButton({ children, variant = 'default', size = 'md', style = {}, onClick, icon }) {
  const sizes = {
    sm: { px: 10, py: 5, fs: 14 },
    md: { px: 14, py: 8, fs: 16 },
    lg: { px: 22, py: 14, fs: 20 },
  };
  const s = sizes[size];
  const fills = {
    default: 'transparent',
    primary: SK.ink,
    promo: SK.coral,
    hi: SK.hi,
    ghost: 'transparent',
  };
  const txts = {
    default: SK.ink,
    primary: SK.paper,
    promo: SK.ink,
    hi: SK.ink,
    ghost: SK.ink,
  };
  return (
    <SKBox fill={fills[variant]} radius={6} strokeWidth={variant === 'ghost' ? 1.2 : 1.8}
      style={{ display: 'inline-block', cursor: 'pointer', ...style }}>
      <div onClick={onClick} className="sk-body" style={{ padding: `${s.py}px ${s.px}px`, fontSize: s.fs, color: txts[variant], display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6, whiteSpace: 'nowrap' }}>
        {icon}{children}
      </div>
    </SKBox>
  );
}

// Scribble underline
function SKUnderline({ color = SK.hi, style = {} }) {
  return (
    <svg style={{ position: 'absolute', left: 0, right: 0, bottom: -4, height: 10, width: '100%', ...style }} viewBox="0 0 100 10" preserveAspectRatio="none">
      <path d="M 1 5 Q 25 2, 50 5 T 99 5" stroke={color} strokeWidth="4" fill="none" strokeLinecap="round" opacity="0.8" />
    </svg>
  );
}

// Arrow (hand-drawn)
function SKArrow({ direction = 'right', size = 24, color = SK.ink, style = {} }) {
  const rotations = { right: 0, down: 90, left: 180, up: 270 };
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" style={{ transform: `rotate(${rotations[direction]}deg)`, ...style }}>
      <path d="M 3 12 Q 10 11, 20 12" stroke={color} strokeWidth="1.8" strokeLinecap="round" />
      <path d="M 15 7 Q 18 11, 20 12 Q 18 13, 15 17" stroke={color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" fill="none" />
    </svg>
  );
}

// Icon set (minimal sketchy)
const SKIcon = {
  star: ({ size = 16, fill = 'none', stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth="1.6" strokeLinejoin="round"><path d="M12 3l2.5 6 6.5.5-5 4.5 1.5 6.5L12 17l-5.5 3.5L8 14 3 9.5 9.5 9z"/></svg>
  ),
  flame: ({ size = 16, fill = 'none', stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth="1.6" strokeLinejoin="round"><path d="M12 3s2 3 2 6-3 3-3 6 2 5 2 5-6-1-6-6c0-4 5-7 5-11z"/><path d="M14 14s3 1 3 4-4 4-4 4"/></svg>
  ),
  trophy: ({ size = 16, stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="1.6" strokeLinejoin="round"><path d="M6 4h12v4a6 6 0 01-12 0z"/><path d="M6 6H3v2a3 3 0 003 3M18 6h3v2a3 3 0 01-3 3M10 14h4v3h-4zM8 20h8"/></svg>
  ),
  book: ({ size = 16, stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="1.6" strokeLinejoin="round"><path d="M4 5v14l8-2 8 2V5l-8 2z"/><path d="M12 7v12"/></svg>
  ),
  bolt: ({ size = 16, stroke = SK.ink, fill = 'none' }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth="1.6" strokeLinejoin="round"><path d="M13 2L4 14h7l-1 8 9-12h-7z"/></svg>
  ),
  clock: ({ size = 16, stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="1.6"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
  ),
  check: ({ size = 16, stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 12l5 5L20 6"/></svg>
  ),
  x: ({ size = 16, stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2" strokeLinecap="round"><path d="M5 5l14 14M19 5L5 19"/></svg>
  ),
  chart: ({ size = 16, stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="1.6" strokeLinecap="round"><path d="M4 20V6M4 20h16M8 16v-4M12 16V9M16 16v-7M20 16v-2"/></svg>
  ),
  user: ({ size = 16, stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="1.6"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-5 4-7 8-7s8 2 8 7"/></svg>
  ),
  home: ({ size = 16, stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="1.6" strokeLinejoin="round"><path d="M3 11l9-7 9 7v9a1 1 0 01-1 1h-5v-6h-6v6H4a1 1 0 01-1-1z"/></svg>
  ),
  history: ({ size = 16, stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="1.6" strokeLinecap="round"><path d="M3 12a9 9 0 109-9c-3 0-5 1-7 3M3 3v4h4M12 7v5l3 2"/></svg>
  ),
  target: ({ size = 16, stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="1.6"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill={stroke}/></svg>
  ),
  heart: ({ size = 16, stroke = SK.ink, fill = 'none' }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth="1.6" strokeLinejoin="round"><path d="M12 20s-7-4.5-7-10a4 4 0 017-2.5A4 4 0 0119 10c0 5.5-7 10-7 10z"/></svg>
  ),
  share: ({ size = 16, stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="1.6" strokeLinejoin="round"><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8 11l8-4M8 13l8 4"/></svg>
  ),
  play: ({ size = 16, stroke = SK.ink, fill = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth="1.6" strokeLinejoin="round"><path d="M7 4v16l13-8z"/></svg>
  ),
  gift: ({ size = 16, stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="1.6" strokeLinejoin="round"><path d="M3 9h18v4H3zM5 13v9h14v-9M12 9v13M8 9a3 3 0 110-6c2 0 4 3 4 6-2 0-4-1-4-6zM16 9a3 3 0 100-6c-2 0-4 3-4 6 2 0 4-1 4-6z"/></svg>
  ),
  menu: ({ size = 16, stroke = SK.ink }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="1.8" strokeLinecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
  ),
  arrow: ({ size = 16, stroke = SK.ink, dir = 'right' }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" style={{ transform: `rotate(${{right:0,down:90,left:180,up:270}[dir]}deg)` }}>
      <path d="M5 12h14M13 6l6 6-6 6"/>
    </svg>
  ),
};

// Progress bar (sketchy)
function SKProgress({ value = 0.5, height = 10, style = {}, color = SK.ink }) {
  return (
    <div style={{ position: 'relative', height, ...style }}>
      <SKBox radius={height/2} strokeWidth={1.4} style={{ width: '100%', height: '100%' }}>
        <div style={{ width: `${Math.max(0, Math.min(1, value)) * 100}%`, height: '100%', position: 'relative' }}>
          <svg style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
            <defs>
              <pattern id="prog-hatch" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(45)">
                <line x1="0" y1="0" x2="0" y2="6" stroke={color} strokeWidth="2.5" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#prog-hatch)" rx={height/2} />
          </svg>
        </div>
      </SKBox>
    </div>
  );
}

// Badge
function SKBadge({ children, color = SK.coral, style = {} }) {
  return (
    <SKBox fill={color} radius={10} strokeWidth={1.4} style={{ display: 'inline-block', ...style }}>
      <div className="sk-label" style={{ padding: '2px 8px', fontSize: 11, color: SK.ink, fontWeight: 700, letterSpacing: 0.5, textTransform: 'uppercase' }}>{children}</div>
    </SKBox>
  );
}

// Dotted divider
function SKDivider({ style = {} }) {
  return <div style={{ height: 1, borderTop: `1.5px dashed ${SK.ink}`, opacity: 0.4, ...style }} />;
}

// Annotation callout — post-it style note pointing at something
function SKAnnotation({ children, style = {}, rotate = -1.5 }) {
  return (
    <div className="sk-body" style={{
      background: SK.hi, padding: '8px 12px', fontSize: 13, color: SK.ink,
      transform: `rotate(${rotate}deg)`,
      boxShadow: '1px 2px 6px rgba(0,0,0,.1)',
      maxWidth: 200, lineHeight: 1.3,
      ...style,
    }}>{children}</div>
  );
}

Object.assign(window, { SK, SKBox, SKHatch, SKButton, SKUnderline, SKArrow, SKIcon, SKProgress, SKBadge, SKDivider, SKAnnotation });
