# AIFU brend xotirasi

Manba: «AIFU Brand guideline», 2024 (muallif: Jahongir Shukurof, 30 bet, rus tilida). PDF repoga qoʻshilmagan (28 MB); bu fayl undagi qoidalarning qisqa, tekshirilgan nusxasi. Har bir yangi AIFU dizayni shu qoidalardan boshlanadi.

Vizual doska (brend varagʻi + 4 ta stil yoʻnalishi): https://claude.ai/artifact/5Yb5zGnbEUiGU3nD2wRng5

## Ranglar

| Nom | HEX | RGB | Qayerda |
|---|---|---|---|
| Pushti (asosiy) | `#FF0158` | 255 · 1 · 88 | fon, aksent, logo harflari |
| Koʻk (asosiy) | `#002E60` | 0 · 46 · 96 | fon, matn, logo harflari |
| Oq | `#FFFFFF` | 255 · 255 · 255 | fon, toʻq fondagi matn |
| Kulrang | `#7B7B7B` | 123 · 123 · 123 | faqat logo yozuvi («Aniq va ijtimoiy fanlar universiteti») |
| Kulrang fon | `#A6A6A6` | 166 · 166 · 166 | 1 rangli bosma uchun logo foni; ikkinchi darajali qiymatlar |

- PDF 11-betidagi HEX yozuvlari (`ff0000`, `1a1a1a`) shablondan qolgan xato. Yuqoridagi qiymatlar logo fayllarining oʻzidan oʻlchangan va repodagi oldingi ishlar (`src/`, `v2/`, `reels/`) bilan bir xil.
- Pushti va koʻk teng huquqli. Ijtimoiy tarmoq postlari koʻpincha juft chiqadi: bir xil maket koʻk fonda va pushti fonda.
- Kontrast (WCAG): oq↔koʻk 13,5:1 — istalgan matn; oq↔pushti 3,9:1 — faqat 24 px+ yoki qalin sarlavha; pushti↔koʻk 3,5:1 — faqat yirik element; `#7B7B7B` oq ustida 4,2:1 — mayda matnga yaramaydi.
- Gradient, soya, glow ishlatilmaydi.

## Tipografika

- Asosiy shrift: **Helvetica** (Bold, Regular, Light). Zaxira tartibi: `'Helvetica Neue', Helvetica, Inter, Arial, sans-serif` — Inter repoda bor (`src/assets/fonts/`).
- Sarlavha: Bold, zich (letter-spacing ≈ −0,02…−0,05em, line-height 0,85–1,0).
- Ikkinchi qator: Light yoki Light Italic («Ingliz tili», «Bakalavriat · Magistratura»).
- Matn: Regular.
- Logodagi slab-serif harflar — maxsus chizilgan logotip, shrift sifatida terilmaydi.

## Logotip

Fayllar: `brand/logos/` (fon shaffof, chetlari kesilgan, rang va proporsiya asl holida).

| Fayl | Nima | Qayerda |
|---|---|---|
| `aifu-horizontal.png` | AIFU + «Aniq va ijtimoiy fanlar universiteti» | asosiy, oq fon |
| `aifu-horizontal-white.png` | oq/pushti harflar + oq yozuv | faqat koʻk fon (pushti fonda I va U yoʻqoladi) |
| `aifu-shield.png` | qalqon: tepasi koʻk «AI», pasti pushti «FU», EST 2022 | avatar, postlar, osilgan yorliq |
| `aifu-stacked.png` | AI / FU monogramma | ixcham joylar |
| `aifu-circle.png` | doira chizigʻi ichida AI/FU, EST 2022 | muhr, merch |

- Himoya maydoni: logo atrofida kamida 1x (AIFU harflari balandligi) boʻsh joy.
- Mumkin emas: proporsiyani choʻzish/siqish, rangni almashtirish, past sifat, soya/glow/effekt, rastr logoga effekt, qiyshaytirish.
- Pushti fonda logo oq plashka (masalan, oq qalqon-yorliq) ustiga qoʻyiladi.

## Stil elementi va modul

- Stil elementi — **qalqon/ark shakli**: tepasi tekis, pasti yarim doira (`border-radius: 0 0 50% 50%` yoki `0 0 W/2 W/2`). Foto ramkasi, plashka, yuqoridan osilgan logo yorligʻi sifatida.
- Modul: maket 2 qismdan — foto yoki illyustratsiya (≈50%) + matn bloki. Logo doim matn blokining ustida.
- Postlardagi kuzatilgan naqshlar: koʻk/pushti gorizontal tasma ustida matn; qalqon logo pastki oʻng burchakda; yuqorida `@aifu.uz` va `qabul.aifu.uz` (oq ramkali pill).

## Foto uslubi

Yorugʻ, tabiiy, baʼzan rangsizlantirilgan foto yoki realistik render. Sariq va yashil ohanglar kamaytiriladi. Odamlar: talabalar, bitiruvchilar, darsda, kampusda.

## Ikonografika

Oddiy, qatʼiy, standart piktogrammalarga oʻxshash chiziqli ikonalar; bitta toʻplamda 6 uslub (chiziqli, qalin, ikki rangli, toʻldirilgan…).

## Matn va kontaktlar

- Shior (paketlarda): «Kelajak quramiz».
- Qabul: `qabul.aifu.uz` · 78 555-21-21. Instagram: `@aifu.uz`. Sayt: `www.aifu.uz`.
- Imlo — **yangi oʻzbek alifbosi** (dizayndagi barcha matnlar uchun):

  | Eski | Yangi | Misol |
  |---|---|---|
  | Oʻ oʻ | Ö ö | yoʻnalish → yönaliş |
  | Gʻ gʻ | Ğ ğ | gʻoya → ğoya |
  | Sh sh | Ş ş | ishlab → işlab |
  | Ch ch | Ç ç | uchun → uçun |

  Tutuq belgisi ʼ (U+02BC) va «ng» oʻzgarmaydi («maʼlumot», «sönggi»). Logolardagi va xorijiy nomlar (TÜBİTAK, Balıkesir Üniversitesi) asl yozuvida qoladi. Kirill harfi yoʻq. Helvetica va Inter (latin-ext) bu harflarni qoʻllaydi.
- Dasturlar haqida maʼlum faktlar: 1+2+1 xalqaro dastur (1 yil Toshkent, 2 yil Xitoy, 1 yil AIFU), «25 ta grant» va «Xitoyda 1 yilgacha taʼlim» (2024 gid namunalaridan — ishlatishdan oldin dolzarbligini tekshiring).

## Stil yoʻnalishlari (2026 tadqiqoti, doskada)

| | Yoʻnalish | Gʻoya |
|---|---|---|
| A | Swiss Bold | Juda katta Helvetica sarlavha, qatʼiy setka, rang bloklari, chetdan chiqib ketgan raqamlar |
| B | Qalqon tizimi | Ark shakli foto ramkasi, naqsh va osilgan yorliq sifatida — brend elementi tizimga aylanadi |
| C | Bento | Yumaloq burchakli modulli kartochkalar: foto, raqam, dastur, CTA bitta setkada |
| D | Infografika | Maʼlumotni hikoya qilish: 1+2+1 dasturi 4 ta ark-ustun koʻrinishida |
