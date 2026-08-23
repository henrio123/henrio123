# GitHubi profiili seadistamine (henrio123)

Terminali-stiilis profiili-README, mis uuendab statistikat iga päev automaatselt.
Paigutus on inspireeritud [Andrew6rant](https://github.com/Andrew6rant/Andrew6rant) profiilist.

## Failid

| Fail | Mis see on |
|---|---|
| `README.md` | Profiilil kuvatav fail — näitab õiget SVG-d vastavalt vaataja teemale |
| `dark_mode.svg` / `light_mode.svg` | Profiilipilt (tume/hele) |
| `profile_config.json` | **Sinu andmed** — muuda siit teksti, keeli, kontakte |
| `gen_svg.py` | Genereerib mõlemad SVG-d config-failist: `python3 gen_svg.py` |
| `today.py` | Uuendab SVG-des statistikat (commitid, tähed, koodiread) GitHub API kaudu |
| `.github/workflows/build.yaml` | Käivitab `today.py` iga päev kell 03:17 UTC ja igal pushil |
| `cache/` | Vahemälu, et koodiridade loendus oleks kiire |

## Paigaldus (u 10 min)

### 1. Loo profiili-repo
GitHubis: **New repository** → nimi täpselt **`henrio123`** (sama mis kasutajanimi — see ongi GitHubi "salajane" profiili-repo), **Public**, ära lisa README-t.

### 2. Laadi failid üles
```bash
cd henrio123-profile   # lahtipakitud kaust
git init -b main
git add .
git commit -m "Add profile README"
git remote add origin https://github.com/henrio123/henrio123.git
git push -u origin main
```
(Võib ka veebis: *uploading an existing file* — aga siis lohista kindlasti kaasa ka peidetud `.github` kaust.)

### 3. Loo access token
GitHub → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**

- **Token name:** `profile-readme`
- **Expiration:** 1 aasta (pane kalendrisse meeldetuletus uuendamiseks)
- **Repository access:** All repositories
- **Repository permissions (Read-only):** Contents, Metadata, Commit statuses, Issues, Pull requests
- **Account permissions (Read-only):** Followers, Starring, Watching

Kopeeri token (näidatakse ainult üks kord).

### 4. Lisa token repo secretiks
Repo `henrio123/henrio123` → **Settings → Secrets and variables → Actions → New repository secret**

- Name: `ACCESS_TOKEN`
- Secret: (kleebi token)

### 5. Käivita
**Actions** → vali **Profile README build** → **Run workflow** (või lihtsalt tee uus push).
Paari minutiga asenduvad nullid päris numbritega. Edaspidi uueneb iga öö ise.

## Hilisem muutmine

1. Muuda `profile_config.json` (tekstid, keeled, kontaktid, hobid)
2. `python3 gen_svg.py`
3. commit + push

Statistika (`Uptime`, `Repos`, `Stars`, `Commits`, `Followers`, `Lines of Code`) kirjutatakse alati automaatselt üle — neid käsitsi muuta pole vaja.

Uue ASCII-portree jaoks küsi Claude'ilt või kasuta suvalist image-to-ascii tööriista (38 veergu × 24 rida, laadi read `profile_config.json` → `"ascii"` massiivi).

## Privaatsus

- Sünnikuupäev on `.github/workflows/build.yaml` failis (`BIRTHDAY`) ja profiil näitab sinu vanust. Kui ei soovi, kustuta see rida — siis näitab `Uptime` GitHubi konto vanust.
- E-posti aadressid ja LinkedIn on avalikult nähtavad — eemalda `profile_config.json`-ist, mida ei taha näidata.
