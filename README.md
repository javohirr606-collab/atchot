# AIFU · 2026–2027 qabul mavsumi · Marketing boʻlimi hisoboti

Rektorat va rahbariyat uchun hisobot-animatsiya: 1920×1080, 2:25, diktor ovozi bilan sinxron.

## Qaysi faylni ochish kerak

| Fayl | Nima uchun |
|---|---|
| `dist/AIFU_2026-2027_marketing_hisoboti.html` | **Asosiy fayl.** Bitta mustaqil fayl: shriftlar, logo, diktor ovozi va musiqa ichida. Internet kerak emas. Ikki marta bosib Chrome yoki Edge’da oching. |
| `dist/AIFU_2026-2027_marketing_hisoboti.mp4` | Zaxira nusxa (H.264 + AAC, 30 kadr/s). Brauzer ishlatib boʻlmaydigan joyda yoki Telegram orqali yuborish uchun. |
| `src/index.html` | Manba fayl (resurslar `src/assets/` dan olinadi). Faqat lokal server orqali ishlaydi: `cd src && python3 -m http.server`. |

## Koʻrsatish tartibi

1. Faylni oching — birinchi kadrda **«Boshlash»** tugmasi turadi (brauzer avtomatik ovozni bloklaydi).
2. «Boshlash» bosilganda animatsiya va ovoz birga boshlanadi, brauzer imkon bersa toʻliq ekranga oʻtadi.
3. Boshqaruv paneli yashirin: sichqonchani ekranning eng pastiga olib borilganda chiqadi, 2 soniyadan keyin yana yashirinadi. Kursor ham harakatsiz qolganda yoʻqoladi.

| Tugma | Amal |
|---|---|
| Probel / K | Ijro / pauza |
| → / ← | Keyingi / oldingi sahna |
| Home | Boshiga |
| F | Toʻliq ekran |
| M | Ovozni oʻchirish / yoqish |
| H | Panelni doimiy koʻrsatish / yashirish |

Panelda: play/pauza, vaqt shkalasi (sahna chegaralari belgilangan, ustiga olib borilsa sahna nomi chiqadi), 12 ta sahna tugmasi, ovoz va toʻliq ekran.

## Ovoz

- **Diktor (`vo.mp3`).** Yuklangan faylning dastlabki ~13,5 soniyasida ssenariyga kirmagan boshqa matn bor edi («Assalomu alaykum. Kuzda Toshkent koʻchalari… Bozorlarda esa yangi hosil…»). Ssenariy matni 13,82-soniyadan boshlanadi, shuning uchun fayl 13,40-soniyadan kesildi. Ovoz −16 LUFS ga tenglashtirildi, boshqa oʻzgartirilmadi.
- **Sinxron.** Diktor nutqi 42 ta boʻlakka ajratilib, har biri nutqni aniqlash modeli bilan matnga solishtirildi. Har bir raqam diktor uni aytayotgan paytda sanala boshlaydi (masalan: «oʻttiz olti ming…» — 0:10,9; «bir ming olti yuz oʻttiz bir» — 0:19,5; «oʻttiz yetti dollar yetmish olti sent» — 1:37,1).
- **Musiqa (`music.mp3`).** Trek 50-soniyadan boshlanadi — shunda uning tabiiy yakuni final kadrga toʻgʻri keladi. Diktor gapirganda musiqa diktordan ≈18 dB past, 0,6 soniyadan uzun pauzalarda 5 dB koʻtariladi, finalda toʻliq ochiladi va oʻz-oʻzidan tugaydi.
- **Effektlar** Web Audio API orqali sintez qilinadi, tashqi fayl yoʻq: sahna almashuvida whoosh, sanash paytida juda past tick, asosiy raqam joyiga tushganda past bass hit (7 marta), final logoda toza chime.
- Umumiy aralashma: −13 LUFS, peak −1,2 dBFS.
- Musiqa fayl metamaʼlumotiga koʻra: «Corporate Documentary» — AShamaluevMusic. Ommaviy foydalanishdan oldin litsenziya shartlarini (muallifni koʻrsatish talabi) tekshiring.

## Sahnalar

| # | Vaqt | Sahna | Oʻtish |
|---|---|---|---|
| 1 | 0:00 | Ochilish | brend moduli ochiladi, qizil chiziq chiziladi |
| 2 | 0:09,6 | Mavsum natijasi | chiziq tepaga koʻtarilib sarlavha chizigʻiga aylanadi |
| 3 | 0:23,5 | Oʻtgan yil bilan taqqoslash | chiziq yigʻilib, qayta chiziladi |
| 4 | 0:35,5 | Oʻsish drayveri | chiziq |
| 5 | 0:43,4 | Qanday ishladik | chiziq markazga tushib, uch nuqtali yoʻlga aylanadi |
| 6 | 0:46,4 | 1-bosqich: Tanitish | yoʻl yuqori oʻng burchakdagi bosqichlar paneliga aylanadi |
| 7 | 0:59,0 | 2-bosqich: Ishonch | chiziq |
| 8 | 1:15,3 | 3-bosqich: Qaror | chiziq |
| 9 | 1:27,6 | Kanallar va narx | brend moduli (qizil diagonal blok) wipe |
| 10 | 1:40,0 | Chirchiq | chiziq |
| 11 | 1:55,0 | Keyingi mavsum vazifalari | brend moduli wipe |
| 12 | 2:14,8 | Final | brend moduli ekranni yopadi, logo, chime |

Umumiy davomiylik 2:25. Bu diktor ovozi bilan belgilanadi: ssenariy oʻqilishi 2:13,6 davom etadi, ustiga ochilishdagi 1 soniya va ≈10 soniyalik final qoʻshiladi. Ssenariydagi sahna vaqtlari (0:00–2:24) bilan deyarli bir xil.

## Sifat tekshiruvi

**Raqamlar** — hammasi promptdagidek, yaxlitlanmagan. Ming ajratuvchisi probel (uzilmaydigan), oʻnlik ajratuvchisi vergul:
36 003 · 17 218 · 8 336 · 1 631 · 31 711 · 15 506 · 6 027 · 1 200 · +13,5% · +11,0% · +38,3% · +35,9% · 3,8% → 4,5% · +53% · ×2 · +104% · 119 · 11-oʻrin · 8-oʻrin · 1-oʻrin · 1+3 · 9 mamlakat · 15 avgust · 25–26 avgust · 28 avgust · 70 · 100 · 180 ball · 254 ariza · $2,93 · $61 594 · 25 809 · 2 782 · 1 614 · $1,71 · $3,58 · $7,39 · $37,76 · 198 → 430 · +117% · 26 foizi · $39,0 · $37,3 · 15 214 · 23 foizi.
Narx zinapoyasi ichki jihatdan ham mos: $61 594 / 36 003 = $1,71; / 17 218 = $3,58; / 8 336 = $7,39; / 1 631 = $37,76.

**Bir kadrda 4 tadan ortiq asosiy raqam yoʻq.** Yangi raqamlar guruhi kirganda oldingisi xiralashadi (8-sahnada grant kartasi, 9-sahnada chap ustun, 10-sahnada birinchi ikki qator, 7-sahnada ikkinchi darajali oʻrinlar). Istisno: 3-sahnada ssenariy talab qilgan toʻrt juft ustun ustida 2025/2026 qiymatlari kichik yorliq sifatida turadi; katta raqamlar faqat toʻrtta oʻsish foizi.

**Grafiklar masshtabda chizilgan:** voronka eni lid soniga mutanosib, har bir juft ustun oʻz ichida mutanosib, narx zinapoyasidagi chiziqlar dollar qiymatiga mutanosib. Chirchiq xaritasida faqat Toshkent–Chirchiq yoʻnalishi haqiqiy (≈33° shimoli-sharq), masofa yoki chegara oʻylab topilmagan.

**Imlo:** oʻ, gʻ uchun ʻ (U+02BB), tutuq belgisi uchun ʼ (U+02BC) ishlatilgan («Taʼlim sifatini taʼminlash», «taʼlim va abituriyent kanallari»). Kirill harfi yoʻq.

**Shrift:** avval kompyuterdagi Helvetica, keyin Helvetica Neue, ular boʻlmasa fayl ichidagi Inter (Windows’da shu ishlaydi). ʻ belgisi Helvetica’da boʻlmasa ham Inter’dan olinadi.

**Brend:** ranglar #FF0158, #002E60, oq; #A6A6A6 faqat 2025-yil qiymatlari uchun. Gradient, soya, glow yoʻq. Logo yuklangan PNG faylning oʻzi, proporsiyasi va rangi oʻzgartirilmagan; koʻk fonda koʻrinishi uchun oq plashka ustida, atrofida himoya maydoni bilan (ochilish va finalda — biznes-kartadagi kabi oq doira, sahnalarda — ijtimoiy tarmoq postlaridagi kabi yuqoridan osilgan oq yorliq). Odamlar fotosurati ishlatilmagan.

## Qayta yigʻish

```bash
node tools/build.mjs          # dist/…html — bitta mustaqil fayl
node tools/render-video.mjs   # dist/…mp4 — ffmpeg va Playwright (Chromium) kerak
```

Matn, raqam yoki vaqtni oʻzgartirish uchun `src/index.html` ni tahrirlang: har bir element `data-in` (kirish vaqti), raqamlar `data-count` / `data-at` (sanash qachon boshlanadi) atributlariga ega. Diktor nutqi boʻlaklari `SPEECH` massivida.

## Tuzilma

```
src/index.html            animatsiya (CSS, 12 sahna, vaqt dvigateli, Web Audio)
src/assets/logo.png       yuklangan logo (oʻzgarishsiz)
src/assets/vo.mp3         diktor (13,40 s dan kesilgan, −16 LUFS)
src/assets/music.mp3      musiqa (50 s dan, −16 LUFS)
src/assets/fonts/         Inter (SIL Open Font License)
tools/build.mjs           bitta faylga yigʻish
tools/render-video.mjs    MP4 zaxira nusxa
dist/                     tayyor fayllar
```
