const { SerieButton, Chip, RangeRow, ToggleSwitch, StudioButton, CoverSlide, QuoteSlide, CTASlide } = window.UneDeuxDesignSystem_8067cc;

const SERIES = {
  cejourla:   { name: 'Ce jour-là',    description: 'Éphéméride · carrousel',  swatch: 'var(--sig-cejourla)',   onSig: 'var(--on-sig-cejourla)',   label: 'N°1 · CE JOUR LÀ …', ratio: '3:4' },
  oublies:    { name: 'Les oubliés',   description: 'Injustices · carrousel',  swatch: 'var(--sig-oublies)',    onSig: 'var(--on-sig-oublies)',    label: 'N°1 · LES OUBLIÉS', ratio: '3:4' },
  portraits:  { name: 'Portraits',     description: 'Visages · reel',          swatch: 'var(--swatch-portraits)', onSig: 'var(--ink)',              label: 'PORTRAITS', ratio: '9:16' },
  arretdejeu: { name: "L'arrêt de jeu", description: 'Enquête · carrousel',     swatch: 'var(--sig-arretdejeu)', onSig: 'var(--on-sig-arretdejeu)', label: "N°1 · L'ARRÊT DE JEU", ratio: '3:4' }
};

const TEMPLATES = ['cover', 'titre', 'corps', 'citation', 'cta'];

function StudioApp() {
  const [serie, setSerie] = React.useState('cejourla');
  const [tpl, setTpl] = React.useState('cover');
  const [title, setTitle] = React.useState('28 JUIN 1958 IMAGINE TU AS 17 ANS');
  const [greenWord, setGreenWord] = React.useState('IMAGINE');
  const [body, setBody] = React.useState("Tu t'apprêtes à jouer une demi-finale de Coupe du monde.\nEt à la fin du match…");
  const [cur, setCur] = React.useState('01');
  const [tot, setTot] = React.useState('09');
  const [zoom, setZoom] = React.useState(100);
  const [dark, setDark] = React.useState(78);
  const [safeOn, setSafeOn] = React.useState(true);
  const [quote, setQuote] = React.useState("Sur le terrain, tout s'est joué en deux passes.");
  const [quoteAccent, setQuoteAccent] = React.useState("tout s'est joué en deux passes.");
  const [quoteAuthor, setQuoteAuthor] = React.useState('');
  const [caption, setCaption] = React.useState("L'ANALYSE");
  const [btnlabel, setBtnlabel] = React.useState('ENREGISTRE');

  const s = SERIES[serie];
  const words = [...new Set(title.trim().split(/\s+/).filter(Boolean))];

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--ink)', color: 'var(--cream)', fontFamily: 'var(--font-body)' }}>
      {/* ===== left panel ===== */}
      <div style={{ width: 420, flex: '0 0 420px', padding: '22px 22px 60px', borderRight: '1px solid var(--border-editor)', overflowY: 'auto', maxHeight: '100vh', boxSizing: 'border-box' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 11, paddingBottom: 16, marginBottom: 18, borderBottom: '1px solid var(--border-editor)' }}>
          <div style={{ width: 30, height: 30, border: '2px solid var(--cream)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'var(--font-label)', fontWeight: 700, fontSize: 14 }}>1·2</div>
          <div style={{ fontFamily: 'var(--font-display)', fontSize: 22 }}>une<span style={{ color: 'var(--sig-oublies)' }}>·</span>deux</div>
          <div style={{ marginLeft: 'auto', fontFamily: 'var(--font-label)', fontWeight: 700, fontSize: 11, letterSpacing: '0.1em', color: s.swatch }}>{s.name.toUpperCase()}</div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 20 }}>
          {Object.keys(SERIES).map(k => (
            <SerieButton key={k} name={SERIES[k].name} description={SERIES[k].description} swatch={SERIES[k].swatch} active={serie === k} onClick={() => setSerie(k)} />
          ))}
        </div>

        <div style={{ marginBottom: 13 }}>
          <label style={fieldLabelStyle}>Type de slide</label>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 7 }}>
            {TEMPLATES.map(t => <Chip key={t} active={tpl === t} onClick={() => setTpl(t)}>{t}</Chip>)}
          </div>
        </div>

        <div style={sectionHeadStyle}>Contenu de la cover</div>

        {(tpl === 'cover' || tpl === 'titre') && (
          <>
            <div style={fieldWrapStyle}>
              <label style={fieldLabelStyle}>Titre</label>
              <textarea value={title} onChange={e => setTitle(e.target.value)} style={textareaStyle} />
            </div>
            <div style={fieldWrapStyle}>
              <label style={fieldLabelStyle}>Mot-clé coloré</label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 7 }}>
                <Chip active={greenWord === ''} onClick={() => setGreenWord('')}>Aucun</Chip>
                {words.map(w => <Chip key={w} active={w.toUpperCase() === greenWord.toUpperCase()} onClick={() => setGreenWord(w)}>{w}</Chip>)}
              </div>
            </div>
          </>
        )}

        {(tpl === 'cover' || tpl === 'corps') && (
          <div style={fieldWrapStyle}>
            <label style={fieldLabelStyle}>{tpl === 'corps' ? 'Corps (plein cadre)' : 'Sous-titre (corps)'}</label>
            <textarea value={body} onChange={e => setBody(e.target.value)} style={textareaStyle} />
          </div>
        )}

        {tpl === 'citation' && (
          <>
            <div style={fieldWrapStyle}><label style={fieldLabelStyle}>Citation</label><textarea value={quote} onChange={e => setQuote(e.target.value)} style={textareaStyle} /></div>
            <div style={fieldWrapStyle}>
              <label style={fieldLabelStyle}>Segment coloré</label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 7 }}>
                <Chip active={!quoteAccent} onClick={() => setQuoteAccent('')}>Aucun</Chip>
                {[...new Set(quote.trim().split(/\s+/).filter(Boolean))].map(w => (
                  <Chip key={w} active={quoteAccent.trim().toLowerCase() === w.toLowerCase()} onClick={() => setQuoteAccent(w)}>{w}</Chip>
                ))}
              </div>
            </div>
            <div style={fieldWrapStyle}><label style={fieldLabelStyle}>Auteur</label><input value={quoteAuthor} onChange={e => setQuoteAuthor(e.target.value)} style={inputStyle} placeholder="Ex : Zinédine Zidane" /></div>
            <div style={fieldWrapStyle}><label style={fieldLabelStyle}>Légende bas</label><input value={caption} onChange={e => setCaption(e.target.value)} style={inputStyle} /></div>
          </>
        )}

        {tpl === 'cta' && (
          <>
            <div style={fieldWrapStyle}><label style={fieldLabelStyle}>Titre</label><textarea value={title} onChange={e => setTitle(e.target.value)} style={textareaStyle} /></div>
            <div style={fieldWrapStyle}><label style={fieldLabelStyle}>Sous-titre</label><textarea value={body} onChange={e => setBody(e.target.value)} style={textareaStyle} /></div>
            <div style={fieldWrapStyle}><label style={fieldLabelStyle}>Libellé du bouton</label><input value={btnlabel} onChange={e => setBtnlabel(e.target.value)} style={inputStyle} /></div>
          </>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 11, marginBottom: 13 }}>
          <div><label style={fieldLabelStyle}>Slide</label><input value={cur} onChange={e => setCur(e.target.value)} style={inputStyle} /></div>
          <div><label style={fieldLabelStyle}>Total</label><input value={tot} onChange={e => setTot(e.target.value)} style={inputStyle} /></div>
        </div>

        <div style={sectionHeadStyle}>Photo de fond</div>
        <div style={{ border: '1px dashed var(--border-editor)', borderRadius: 10, padding: '18px 14px', textAlign: 'center', background: 'var(--surface-editor-panel)', marginBottom: 6 }}>
          <div style={{ fontFamily: 'var(--font-label)', fontWeight: 700, fontSize: 13, letterSpacing: '0.03em', color: '#9a9588' }}>CLIQUE OU GLISSE UNE PHOTO</div>
          <div style={{ fontSize: 11, color: '#776f60', marginTop: 5 }}>aucune image — dégradé par défaut</div>
        </div>
        <RangeRow label="Zoom" value={zoom} min={100} max={260} onChange={setZoom} display={(zoom / 100).toFixed(1)} />
        <RangeRow label="Assombrir" value={dark} min={20} max={95} onChange={setDark} />
        <ToggleSwitch label="Zone sûre Instagram" on={safeOn} onChange={setSafeOn} />

        <div style={{ display: 'flex', gap: 10, marginTop: 22 }}>
          <StudioButton>Exporter PNG</StudioButton>
          <StudioButton variant="ghost" onClick={() => { setZoom(100); setDark(78); }}>Réinit.</StudioButton>
        </div>
      </div>

      {/* ===== stage / preview ===== */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '28px 22px', gap: 16 }}>
        <div style={{ width: '100%', maxWidth: 420, display: 'flex', justifyContent: 'space-between', fontFamily: 'var(--font-label)', fontWeight: 700, fontSize: 13, letterSpacing: '0.06em', color: '#8b8678' }}>
          <span>APERÇU — {s.name.toUpperCase()}</span>
          <span>{s.ratio}</span>
        </div>
        <div style={{ maxWidth: 420, width: '100%', borderRadius: 10, overflow: 'hidden', background: '#1a1714' }}>
          {tpl === 'citation' ? (
            <QuoteSlide quote={quote} quoteAccent={quoteAccent} quoteAuthor={quoteAuthor} caption={caption} cur={cur} tot={tot} />
          ) : tpl === 'cta' ? (
            <CTASlide title={title} greenWord={greenWord} body={body} btnlabel={btnlabel} sig={s.swatch} onSig={s.onSig} />
          ) : (
            <CoverSlide serie={serie} variant={tpl} title={title} greenWord={greenWord} body={body} cur={cur} tot={tot} />
          )}
        </div>
        <div style={{ width: '100%', maxWidth: 420, fontSize: '11.5px', color: '#776f60', lineHeight: 1.5, textAlign: 'center' }}>
          Recreation for design reference only — not wired to real export/upload.
        </div>
      </div>
    </div>
  );
}

const fieldLabelStyle = { display: 'block', fontFamily: 'var(--font-label)', fontWeight: 700, fontSize: 12, letterSpacing: '0.02em', color: '#9a968c', marginBottom: 6, textTransform: 'uppercase' };
const sectionHeadStyle = { fontFamily: 'var(--font-label)', fontWeight: 700, fontSize: 12, letterSpacing: '0.1em', color: 'var(--sig-cejourla)', margin: '22px 0 12px', textTransform: 'uppercase' };
const fieldWrapStyle = { marginBottom: 13 };
const inputStyle = { width: '100%', background: 'var(--surface-editor-panel)', border: '1px solid var(--border-editor)', borderRadius: 8, color: 'var(--cream)', fontFamily: 'var(--font-body)', fontSize: 15, padding: '11px 13px', outline: 'none', boxSizing: 'border-box' };
const textareaStyle = { ...inputStyle, resize: 'vertical', minHeight: 60, lineHeight: 1.4 };

window.StudioApp = StudioApp;
