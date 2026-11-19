// Edit decision lists for both cuts of the SIMO day-1 video, shared by reel.html, wide.html and tools/mix.py
// (mix.py reads this file through node). All `s`/`a`/`b` values are times in src/assets/source.mp4; speech is
// taken from the same times of the separated vocal stem (src/assets/audio/speech.m4a).
(() => {
  const BEAT = 0.4644; // music_percussion.mp3, ~129 bpm

  // ── soundbites: "time word · time word / time word …" (source times from ASR, words checked by ear-of-model
  //    and corrected by hand). "/" starts a new caption chunk, a leading * highlights the word.
  const BITES = {
    q:    [42.08, '39.84 Olimpiadalarda · 40.74 masalalar / 41.22 qanaqa · 41.64 *tuziladi?'],
    org1: [33.20, '28.84 Matematika · 29.40 instituti / 30.00 yetakchi · 30.36 ilmiy · 30.68 xodimi, / 31.24 *SIMO · 31.54 olimpiadasi / 32.06 tashkilotchilaridan · 32.84 biriman.'],
    org2: [53.62, "42.16 O'sha · 42.42 bir · 42.58 kun, · 42.74 ikki · 42.90 kun / 43.08 oldin · 43.32 tuzilmaydi. / 44.22 *Oylab · 44.68 *oldin · 45.68 yig'iladi, / 46.26 har · 46.46 xil · 46.68 mutaxassislarda. / 47.60 Va · 47.94 masalalar / 48.38 *original · 48.84 masala, / 49.36 ya'ni · 50.06 qaysidir · 50.38 olimpiadada / 50.88 tushgan · 51.38 masala · 52.20 emas, / 52.70 ya'ni · 52.86 *yangi · 53.16 *masala."],
    n540: [23.68, "19.28 …oliy · 19.52 ta'lim · 19.78 muassasasidan / 21.28 *540 · 21.96 nafar · 22.34 talaba / 22.88 ro'yxatdan · 23.26 o'tdi."],
    t45:  [234.82, "231.68 Bu · 231.84 yerda / 232.26 *to'rt · 232.50 *yarim · 232.78 *soatda / 233.26 *beshta · 233.64 *masala · 233.92 ustida / 234.22 bosh · 234.50 qotiradi."],
    nost: [241.26, "234.92 Ular · 235.28 juda · 235.76 ko'p · 236.16 fikrlash · 236.90 va / 237.56 aynan · 238.08 *nostandart · 238.86 *fikrlash / 239.68 jihatlarini · 240.74 oshiradi."],
    shah: [87.16, '82.94 Men · 83.16 Abdurahimova · 83.80 Shahnoza, / 84.28 Namangan · 84.72 davlat · 85.00 universiteti / 85.82 4-bosqich · 86.58 talabasiman.'],
    sam:  [194.22, '187.42 Samarqand · 187.80 davlat / 188.04 pedagogika · 188.56 institutining / 189.20 4-bosqich · 189.84 talabasiman. / 190.46 Talabalarning · 191.42 *fikrlashini / 192.08 ancha · 192.74 *ochadigan · 193.16 savollar / 193.48 tushgan · 193.74 ekan · 193.96 bugun.'],
    jidu: [150.46, "140.30 Men · 140.48 Jahon · 140.76 iqtisodiyoti / 141.26 va · 141.38 diplomatiya · 141.92 universiteti / 142.36 2-bosqich · 142.94 talabasiman. / 143.68 Keyingi · 143.95 yil · 144.18 ushbu · 144.44 olimpiadada / 144.86 qatnashmoqchi · 145.46 bo'lgan / 145.80 talabalarga · 146.44 *tavsiyam: / 147.48 ko'proq · 147.94 *oliy · 148.18 *matematikadagi / 149.06 nazariy · 149.40 bilimlaringizni / 149.98 *kuchaytiring."],
    und:  [206.92, "200.30 Olimpiada · 200.70 masalalari / 201.34 talabalarni · 201.98 yana · 202.20 ham / 202.48 *kengroq · 202.92 *fikrlashga / 203.72 va · 204.26 ko'proq · 205.02 *g'oyalar / 205.66 bilan · 205.98 ishlashga · 206.56 undaydi."],
    sav:  [187.02, "172.02 Savollar · 172.56 darajasi / 173.24 juda · 173.50 ham · 173.96 yaxshi. / 174.76 Ham · 175.06 elementar, / 175.54 ham · 175.80 oliy · 175.98 matematika / 176.82 integratsiya · 177.34 qilib · 177.56 tuzilgan / 178.36 xalqaro · 178.86 olimpiadalarda / 180.10 *yuksak · 180.50 *o'rinlarni · 180.98 *olamiz, / 181.40 va · 182.40 xudo · 182.68 xohlasa, / 183.38 *Fields, · 183.88 *Abel / 184.14 mukofotlariga · 185.30 sazovor / 185.70 matematiklar · 186.14 chiqadi / 186.38 degan · 186.56 umiddamiz."],
  };
  const ap = s => s.replace(/([oOgG])'/g, '$1ʻ').replace(/'/g, 'ʼ');
  const CHUNKS = [];  // { s, e, words: [{ s, w, hi }] } in source time, sorted
  for (const [end, str] of Object.values(BITES)) {
    const chunks = str.split(' / ').map(c => ({ words: c.split(' · ').map(x => {
      const i = x.indexOf(' '); let w = ap(x.slice(i + 1)); const hi = w.startsWith('*'); if (hi) w = w.slice(1);
      return { s: +x.slice(0, i), w, hi };
    }) }));
    chunks.forEach(c => { c.s = c.words[0].s; });
    chunks.forEach((c, k) => { c.e = k + 1 < chunks.length ? chunks[k + 1].s : end; c.last = k + 1 === chunks.length; });
    CHUNKS.push(...chunks);
  }
  CHUNKS.sort((x, y) => x.s - y.s);

  // ── 9:16 reel (1080×1920) ──
  const RD = 2.55, RB = k => +(RD + k * BEAT).toFixed(3);
  const reel = {
    DUR: 49.5, DROP: RD, EG_BAND: 41.58,
    // speech placements: t = timeline start, a..b = source range; video follows the source unless a B-roll covers it
    speech: [
      { id: 'q', t: 0.14, a: 39.80, b: 42.14, style: 'hook', video: false },
      { id: 'org1', t: 4.45, a: 31.18, b: 33.28 },
      { id: 'org2a', t: 6.68, a: 42.12, b: 47.45 },
      { id: 'org2c', t: 12.13, a: 49.98, b: 53.70 },
      { id: 'n540', t: 16.10, a: 19.20, b: 23.75, subTo: 21.2 },
      { id: 't45', t: 21.95, a: 231.62, b: 234.88, video: false },
      { id: 'shah', t: 25.45, a: 84.22, b: 85.52, subFrom: 999 },
      { id: 'jidu', t: 26.90, a: 140.24, b: 142.40, subFrom: 999 },
      { id: 'sam', t: 29.22, a: 187.42, b: 194.32, subFrom: 190.40 },
      { id: 'sav', t: 36.50, a: 178.30, b: 187.08, video: false },
    ],
    // B-roll / montage shots: [t0, t1, source in-point, zoom from, zoom to]
    broll: [
      [0, RB(-4), 88.25, 1.1, 1.0], [RB(-4), RB(-3), 170.32, 1.12, 1.0], [RB(-3), RB(-2), 165.70, 1.12, 1.0],
      [RB(-2), RB(-1), 138.00, 1.12, 1.0], [RB(-1), RD, 144.45, 1.15, 1.0],
      [RD, 4.45, 11.82, 1.16, 1.02],
      [20.65, 21.30, 155.40, 1.1, 1.0], [21.30, 21.95, 93.22, 1.1, 1.0],
      [21.95, 22.65, 216.12, 1.08, 1.0], [22.65, 23.35, 163.62, 1.1, 1.0], [23.35, 24.05, 207.02, 1.08, 1.0],
      [24.05, 25.45, 233.72, 1.0, 1.05],
      [36.25, 37.75, 178.25, 1.0, 1.08], [37.75, 38.60, 165.62, 1.06, 1.0], [38.60, 39.85, 137.62, 1.0, 1.07],
      [39.85, 41.25, 155.35, 1.07, 1.0], [41.25, 41.70, 170.32, 1.1, 1.0], [41.70, 42.75, 166.52, 1.0, 1.06],
      [42.75, 44.05, 243.62, 1.06, 1.0], [44.05, 45.30, 58.55, 1.0, 1.06],
    ],
    lower: [
      { t0: 4.65, t1: 9.6, name: 'SIMO tashkilotchisi', role: 'Matematika instituti yetakchi ilmiy xodimi' },
      { t0: 16.25, t1: 18.0, name: 'Ochilish marosimi', role: null },
      { t0: 25.50, t1: 26.85, name: 'Shahnoza Abdurahimova', role: 'Namangan davlat universiteti' },
      { t0: 26.95, t1: 29.15, name: 'Jahon iqtisodiyoti va diplomatiya universiteti', role: '2-bosqich talabasi' },
      { t0: 29.30, t1: 33.4, name: 'Samarqand davlat pedagogika instituti', role: '4-bosqich talabasi' },
    ],
    cities: [[25.45, 26.90, 'NAMANGAN'], [26.90, 29.22, 'TOSHKENT'], [29.22, 31.2, 'SAMARQAND']],
  };

  // ── 16:9 film (1920×1080) ──
  const WD = 2.55, WB = k => +(WD + k * BEAT).toFixed(3);
  const wide = {
    DUR: 93.5, DROP: WD, EG_BAND: 83.43,
    speech: [
      { id: 'q', t: 0.14, a: 39.80, b: 42.14, style: 'hook', video: false },
      { id: 'n540', t: 5.30, a: 19.20, b: 23.75, subTo: 21.2 },
      { id: 'org1', t: 10.20, a: 28.80, b: 33.28 },
      { id: 'org2', t: 14.85, a: 42.12, b: 53.70 },
      { id: 't45', t: 30.30, a: 231.62, b: 241.35 },
      { id: 'shah', t: 40.40, a: 82.88, b: 87.25 },
      { id: 'sam', t: 45.00, a: 187.42, b: 194.32 },
      { id: 'jidu', t: 52.15, a: 140.24, b: 150.56 },
      { id: 'und', t: 65.00, a: 200.24, b: 207.00 },
      { id: 'sav', t: 72.00, a: 171.95, b: 187.08 },
    ],
    // layout scenes: tri = three vertical panels (each a list of [t0, t1, source]); th = talking-head panel + transcript
    scenes: [
      { kind: 'tri', t0: 0, t1: WD, cuts: [0, WB(-4), WB(-3), WB(-2), WB(-1)],
        L: [88.25, 165.70, 144.45, 210.05, 163.65], C: [170.32, 138.00, 94.92, 207.02, 93.22], R: [166.55, 145.05, 155.35, 168.15, 229.65] },
      { kind: 'tri', t0: WD, t1: 5.30, title: true, cuts: [WD], L: [58.55], C: [11.82], R: [68.85] },
      { kind: 'tri', t0: 5.30, t1: 10.20, chapter: [1, 'Ochilish'], cuts: [5.30, 7.45], L: [44.02, 75.02], C: ['sync', 'sync'], R: [58.55, 7.30] },
      { kind: 'th', t0: 10.20, t1: 26.62, chapter: [2, 'Tashkilotchi'],
        who: [[10.2, 26.62, 'SIMO tashkilotchisi', 'Matematika instituti yetakchi ilmiy xodimi']] },
      { kind: 'tri', t0: 26.62, t1: 30.30, chapter: [3, 'Olimpiada'], cuts: [26.62, 27.55, 28.47, 29.40],
        L: [78.95, 87.25, 216.12, 207.05], C: [88.25, 165.62, 170.32, 210.05], R: [93.22, 144.45, 163.62, 145.05] },
      { kind: 'th', t0: 30.30, t1: 40.40, chapter: [3, 'Olimpiada'], who: [], stats: [[232.26, '4,5', 'soat'], [233.26, '5', 'ta masala']] },
      { kind: 'th', t0: 40.40, t1: 62.60, chapter: [4, 'Ishtirokchilar'],
        who: [[40.4, 44.95, 'Shahnoza Abdurahimova', 'Namangan davlat universiteti, 4-bosqich talabasi'],
              [44.95, 52.1, 'Samarqand davlat pedagogika instituti', '4-bosqich talabasi'],
              [52.1, 62.6, 'Jahon iqtisodiyoti va diplomatiya universiteti', '2-bosqich talabasi']] },
      { kind: 'tri', t0: 62.60, t1: 65.00, chapter: [5, 'Kelajak'], cuts: [62.60, 63.80],
        L: [243.62, 246.02], C: [178.25, 181.85], R: [252.25, 155.35] },
      { kind: 'th', t0: 65.00, t1: 87.30, chapter: [5, 'Kelajak'], who: [] },
      { kind: 'end', t0: 87.30, t1: 93.5 },
    ],
  };

  window.EDIT = { BEAT, CHUNKS, reel, wide };
})();
