# Del 1 (ii): Analytisk løsning – forklart enkelt

Dette dokumentet forklarer hva koden i `Hedda.ipynb` gjør, i vanlig språk.

## Hva er problemet?

Vi har en stav av rent kobber (eller rent nikkel). I den ene halvdelen har vi
merket atomene med en "sporstoff"-variant (tracer), altså Cu\* i Cu og Ni\* i Ni.
Kjemisk er alt likt – det er bare merkingen som skiller de to halvdelene.

Ved start (t = 0) ser det slik ut:

- x < 0: konsentrasjon av merkede atomer = 0
- x > 0: konsentrasjon av merkede atomer = 1

Så varmer vi staven opp til 1000 °C og holder den der i 30 timer. Atomene bytter
plass med hverandre (selvdiffusjon), og det skarpe skillet i midten blir gradvis
utvisket. Spørsmålet er: hvordan ser konsentrasjonen ut etter 30 timer?

## Løsningen

Fra Ficks 2. lov, med de grensebetingelsene vi har, får vi:

$$C(x,t) = \frac{C_1 + C_2}{2} - \frac{C_1 - C_2}{2}\,\mathrm{erf}\!\left(\frac{x}{2\sqrt{Dt}}\right)$$

Enkelt sagt:

- **Første ledd** er middelverdien av de to startkonsentrasjonene. Det er der
  profilen ender opp hvis vi venter uendelig lenge – alt blandes til 0,5.
- **Andre ledd** er avviket fra middelverdien. `erf` (feilfunksjonen) er en
  S-formet kurve som går fra −1 til +1, og den gir den myke overgangen mellom de
  to halvdelene.
- **Nøkkelstørrelsen er `x / (2√(Dt))`.** Den sier hvor langt du er fra midten,
  målt i "diffusjonslengder". Kombinasjonen `√(Dt)` er altså den naturlige
  lengdeskalaen for hvor langt diffusjonen har rukket.

Merk konsekvensen: hvis du vil at profilen skal bli dobbelt så bred, må du
gløde **fire ganger** så lenge. Diffusjon går fort i starten og blir tregere.

## Diffusjonskoeffisienten D

Hvor fort dette går, styres av D, som er sterkt temperaturavhengig:

$$D(T) = D_0 \exp\!\left(-\frac{Q}{RT}\right)$$

Verdiene i koden er hentet fra Tabell 2.2 i Porter & Easterling:

| Element | $D_0$ (m²/s) | $Q$ (kJ/mol) |
|---------|--------------|--------------|
| Cu\* i Cu | 31 · 10⁻⁶ | 200,3 |
| Ni\* i Ni | 150 · 10⁻⁶ | 279,7 |

Nikkel har både høyere $D_0$ og høyere $Q$. Ved 1000 °C er det den høye
aktiveringsenergien som dominerer: **Ni diffunderer klart tregere enn Cu.**
Det er grunnen til at Ni-kurven i plottet er brattere – den har ikke rukket å
spre seg like langt på 30 timer.

Fysisk henger dette sammen med smeltepunktet. Ni smelter ved ~1455 °C og Cu ved
~1085 °C, så 1000 °C er "varmere" for kobber relativt sett, og atomene der er
mer bevegelige.

## Konsentrasjonsgradienten

Gradienten er den deriverte av profilen, altså hvor bratt kurven er:

$$\frac{\partial C}{\partial x} = -\frac{C_1 - C_2}{2\sqrt{\pi D t}}\,
\exp\!\left(-\frac{x^2}{4Dt}\right)$$

Dette er en gaussisk klokkekurve:

- Den er **størst i midten** (x = 0), der profilen er brattest.
- Den **flater ut mot endene**, der konsentrasjonen er nesten konstant.
- Toppverdien er $1/(2\sqrt{\pi D t})$, som **minker med tiden**. Etter hvert som
  profilen slakes ut, blir gradienten mindre – og dermed avtar også drivkraften
  for videre diffusjon (Ficks 1. lov: $J = -D\,\partial C/\partial x$).

Cu får en lavere og bredere klokkekurve, Ni en høyere og smalere – samme
observasjon som over, bare sett fra en annen vinkel.

## Antakelser vi gjør

- **Uendelig lang stav.** Løsningen forutsetter at endene er så langt unna at de
  ikke merker noe. Her er $2\sqrt{Dt}$ langt mindre enn 1 mm, så det holder fint.
- **D er konstant.** Gyldig her fordi det er selvdiffusjon: staven er kjemisk
  homogen, så D avhenger ikke av posisjon eller konsentrasjon. (I Del 2, med et
  Cu/Ni-par, holder ikke dette lenger – der må vi bruke Darkens likninger.)
- **1D-diffusjon.** Vi ser bare på transport langs staven.
- **Konstant temperatur.** Det endrer seg i oppgave (iv), der D må regnes ut på
  nytt for hvert tidssteg.

## Om koden

- `Diff_coeff(T, D0, Q)` regner ut D. Legg merke til `Q*1000` – Q er oppgitt i
  kJ/mol, mens R er i J/(mol·K), så enhetene må gjøres like.
- `Concentration_profile` kalles med `C1 = 0` og `C2 = 1`, som gir den ønskede
  startbetingelsen (0 til venstre, 1 til høyre).
- Gradienten ganges med `1e-3` fordi x er i meter. Resultatet blir per mm, som
  passer med x-aksen i plottet.
- Fordi `math.erf` bare tar ett tall om gangen, brukes en for-løkke over x.
  `scipy.special.erf` ville tatt hele arrayet i én operasjon.

## Hva vi bruker dette til videre

Denne analytiske løsningen er **fasiten** for oppgave (iii). Der løser vi samme
problem numerisk med finite difference, og de to kurvene skal ligge oppå
hverandre. Gjør de ikke det, er det noe galt med steglengdene eller
grensebetingelsene i den numeriske koden.
