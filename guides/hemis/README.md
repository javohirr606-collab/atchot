# HEMIS bo‘yicha video qo‘llanma (AIFU talabalari uchun)

`AIFU_HEMIS_qollanma.mp4` — 1920×1080, 1:38, 30 kadr/s, −14 LUFS. `cover.jpg` — muqova. Ovoz matni: `ssenariy.md`.

- HEMIS sahifalari (kirish, bosh sahifa, Profil, menyular) qayta chizilgan, soxta maʼlumot bilan: hech kimning shaxsiy maʼlumoti chiqmaydi. Ogohlantirish matni («Sizning parolingiz xavfsizlik talablariga mos emas…») tizimdagidek.
- Kamera har qadamda kerakli joyga yaqinlashadi, kursor harakatlanadi, bosish va yozish ko‘rsatiladi; tepada 5 qadamli yo‘l-yo‘riq, pastda subtitr.
- Ovoz: Davronbek (ElevenLabs). OneID haqidagi gap yozuvda yo‘q, uning o‘rnida 3 soniyalik pauza: ekranda tugma yoritiladi va izoh chiqadi.
- Musiqa: perkussiya trek, diktor ostida −15 dB. Effektlar (bosish, klaviatura, whoosh, bildirishnoma) sintez qilingan.

## Qayta yig‘ish
```bash
node tools/events.mjs     # build/events.json (effektlar vaqti)
python3 tools/mix.py      # build/mix.wav
node tools/render.mjs     # build/AIFU_HEMIS_qollanma.mp4
```
