# UI/UX Design Brief
## NetworkOps — Porsche Identity (Precision / Engineering)

Porsche-inspired design: networking is about precision, telemetry, and clean function.
The design feels like a Porsche instrument cluster — minimal, exact, restrained color with one decisive red accent.

---

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Graphite Black | `#131516` | Primary background |
| Carbon Panel | `#1D2022` | Card / panel surfaces |
| Brushed Silver | `#C9CDCE` | Primary text / gauge rings |
| Cool Ash | `#8A9196` | Secondary text |
| Guards Red | `#D5001C` | The single accent — active nav, CTAs, streak |
| Chalk White | `#F2F3F3` | Headings / high-emphasis text |
| Status: Up | `#3CB371` | Green status dot |
| Status: Warn | `#E0A100` | Warning indicator |
| Status: Down | `#D5001C` | Error/offline indicator |

---

## Typography

- **UI:** Inter (system-ui fallback — no CDN, offline compatible)
- **Code/Metrics:** JetBrains Mono (monospace fallback)
- **Style:** Tight 4/8px grid, thin silver rules, flat panels, 2px radii near-square cards

---

## Signature Components

### Tachometer Progress Ring
- Classic Porsche rev-counter styling for topic/course completion
- Red SVG arc needle on dark background
- Gauge ticks and percentage readout in center
- Silver ring on dark face

### Interface-Status Rows
- Monospace layout with colored status dot (🟢 up / 🟡 warn / 🔴 down)
- Clean metric readouts like a switch port table
- Used on Dashboard for topic count, accuracy, domains, best streak

### Streak Badge
- Small red tick-counter with flame icon
- Odometer feel with monospace digits
- Shows current streak, level, and total XP
- Auto-refreshes every 30 seconds

### Week Strip
- 7-dot strip showing daily XP
- Filled dot (goal met), half dot (some XP), empty dot (none)
- Day labels in monospace

---

## Component States

### Buttons
- **Primary:** Guards Red fill, white text, dark red hover (`#B80018`)
- **Ghost:** Carbon border, Brushed Silver text, Ash hover border

### Cards
- Carbon Panel background, thin Carbon border, 2px radius
- No shadows — flat design
- Hover: border tint to Guards Red on interactive cards

### Navigation
- Active item: small red left border accent, subtle red background tint
- Inactive: Cool Ash text, Chalk White on hover

### Quiz Feedback
- **Correct:** Green border + checkmark, green background tint
- **Incorrect:** Red border + X, red background tint, shows expected answer
- **Hint:** Red italic text with 💡 icon
