# AIFU · 2026–2027 qabul mavsumi · Marketing boʻlimi hisoboti (2-video)

1920×1080, 3:34, diktor ovozi bilan sinxron. Raqamlar «marketing report 26-27» faylidan, 12.10.2026 holati.

| Fayl | Nima uchun |
|---|---|
| `dist/AIFU_2026-2027_marketing_hisoboti_v2.html` | Asosiy fayl. Shriftlar, logo, ovoz va musiqa ichida, internet kerak emas. Chrome yoki Edge’da oching va «Boshlash»ni bosing. |
| `dist/AIFU_2026-2027_marketing_hisoboti_v2.mp4` | Videofayl (H.264 + AAC, 30 kadr/s): Telegram yoki proyektor uchun. |
| `ssenariy.md` | Diktor uchun yozilgan matn va raqamlar manbasi. |

Boshqaruv 1-video bilan bir xil: probel — pauza, ← → — sahnalar, F — toʻliq ekran, M — ovoz.

## Ovoz

- **Diktor (`src/assets/vo.mp3`).** Yuborilgan ElevenLabs fayli oʻzgarishsiz (−16,6 LUFS), 1-soniyadan boshlanadi.
- **Sinxron.** Ovoz pauzalar boʻyicha 53 boʻlakka ajratildi va har biri nutqni aniqlash modeli bilan matnga solishtirildi. Har bir raqam diktor uni aytayotgan paytda chiqadi.
- **Musiqa (`src/assets/music.mp3`).** 1-videodagi trek («Corporate Documentary», AShamaluevMusic). Ovoz 3:26 boʻlgani uchun trek 1:19–1:36 oraligʻidagi 8 taktli boʻlakni bir marta takrorlab uzaytirildi (ulanish joyi takt chegarasida). Trekning tabiiy yakuni final kadrga toʻgʻri keladi. Diktor gapirganda musiqa past, pauzalarda biroz koʻtariladi.

## Sahnalar

| # | Vaqt | Sahna |
|---|---|---|
| 1 | 0:00 | Ochilish |
| 2 | 0:12 | Mavsum natijasi: 2 166 talaba, +80%, reja 72% |
| 3 | 0:28 | Qabul voronkasi: lid → ariza → shartnoma → toʻlov, grant 1 022 |
| 4 | 0:57 | Taʼlim shakllari: kunduzgi ×3,3, kechki +21%, magistratura −12% |
| 5 | 1:20 | Kampuslar: Qorasaroy 1 640, Chirchiq 529 |
| 6 | 1:36 | Kanallar va soʻrovnoma: Meta 25 929 lid, Instagram 31%, grant 68% |
| 7 | 2:07 | Xarajatlar: $176 856, 1 lid $4,91, 1 talaba $81,65, jami 3 743 mln soʻm |
| 8 | 2:33 | 1 talaba narxi: $52,90 · $77,75 · $160,29 |
| 9 | 2:58 | 2027 vazifalari |
| 10 | 3:22 | Final |

## Qayta yigʻish

```bash
node tools/build.mjs v2          # v2/dist/…html
node tools/render-video.mjs v2   # v2/dist/…mp4 (ffmpeg va Playwright kerak)
```

Matn yoki vaqtni oʻzgartirish uchun `src/index.html` ni tahrirlang (`data-in`, `data-count`, `data-at` atributlari).
